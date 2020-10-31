#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#  Twoblivion
#
#  Author: Jean-Philippe Teissier ( @Jipe_ )
#
#  This work is licensed under the GNU General Public License
#
"""Twoblivion wipes tweets from history."""
__version__ = "0.6"

import argparse
import re
import sys
import twitter
from config import *
from datetime import datetime, timedelta
from dateutil.parser import parse


def delete_items(twitter_api, items_to_delete, item_type):
    """Delete a bunch of Tweets or DMs."""

    global DEBUG # pylint: disable=global-statement
    global DRYRUN # pylint: disable=global-statement

    total_items = len(items_to_delete)
    i = 1

    print(f'🔥 Deleting your old {item_type}s')
    for item in items_to_delete:
        try:
            if not DRYRUN:
                if item_type == 'Tweet':
                    twitter_api.DestroyStatus(item)
                elif item_type == 'Direct Message':
                    twitter_api.DestroyDirectMessage(item)
            if DEBUG:
                print('🔗 [{0:d}/{1:d}] {2:s} ID {3:s} has been '
                      'deleted'.format(i, total_items, item_type, str(item)))
            else:
                sys.stdout.write('🔥')
                sys.stdout.flush()
            i += 1
        except twitter.TwitterError as error:
            print(f"❌ ERROR: {error.message[0]['message']}")
    print(f'✅ {item_type}s have been delete. Bye!')


def fetch_items(twitter_api, userid, item_type, max_id):
    """Fetches Tweets or DMs from a users' account."""
    
    global DEBUG # pylint: disable=global-statement

    try:
        if DEBUG:
            print(f'🔗 Fetching {item_type} with max id {max_id}')
        if item_type == 'Tweet':
            return twitter_api.GetUserTimeline(user_id=userid, max_id=max_id)
        else:
            # return twitter_api.GetDirectMessages(max_id=max_id) + \
            #    twitter_api.GetSentDirectMessages(max_id=max_id)
            # TODO: remove the madness below when python-twitter is fixed
            dms = []
            dm_dict = twitter_api.GetDirectMessages(max_id=max_id, return_json=True)
            if 'events' in dm_dict:
                for dm in dm_dict['events']:
                    dms.append(twitter.models.DirectMessage(**{'id': int(dm['id']), 
                                                               'created_at': datetime.fromtimestamp(int(float(dm['created_timestamp'])/1000)).strftime('%a %b %d %H:%M:%S %z %Y'),
                                                               'text': dm['message_create']['message_data']['text']}))
            return dms
    except twitter.error.TwitterError as error:
        print(f"❌ ERROR: {error.message[0]['message']}")

def fetch_and_delete(twitter_api, user_id, date, item_type):
    """Get the list of Tweets or Direct Messages to delete"""

    global DEBUG # pylint: disable=global-statement

    print(f'⏳ Retrieving the list of {item_type}s to delete '
          '(it might take a while due to rate limits...)')

    items_to_delete = []
    max_id = 0
    while True:
        items = fetch_items(twitter_api, user_id, item_type, max_id)
        if DEBUG:
            if items:
                print(f'🔗 {items}')
        if not items:
            break
        if item_type == "Tweet":
            max_id = items[-1].id - 1
        for item in items:
            if parse(item.created_at, ignoretz=True).date() < parse(date).date():
                for whitelist_item in WHITELIST:
                    if whitelist_item.match(item.text):
                        continue
                items_to_delete.append(item.id)
                if DEBUG:
                    print(f"🔗 [{item.created_at}] {item.id} {item.text[:60].encode('utf-8', errors='ignore')}")

    if len(items_to_delete) > 0:
        print(f'💬 Got {len(items_to_delete)} {item_type}(s) to delete')
        delete_items(twitter_api, items_to_delete, item_type)
    else:
        print('✅ Nothing to delete. Bye!')

def main():
    """Here we go!"""

    if not sys.version_info.major >= 3:
        print('☠️ ERROR: Python 2 is deprecated. Move on...')
        sys.exit(-2)

    print(f'🧹 Twoblivion v{__version__}')

    global DEBUG # pylint: disable=global-statement
    global DRYRUN # pylint: disable=global-statement

    parser = argparse.ArgumentParser(
        description='Wipe your tweets from history.')
    parser.add_argument('-k', '--access_token',
                        default=YOUR_ACCESS_TOKEN,
                        help='Your Access Token')
    parser.add_argument('-s', '--access_token_secret',
                        default=YOUR_ACCESS_TOKEN_SECRET,
                        help='Your Access Token Secret')
    parser.add_argument('-u', '--user_id',
                        default=YOUR_USER_ID, help='Your User ID')
    parser.add_argument('-d', '--date',
                        help='The date from which you want to '
                             'delete Tweets or DMs')
    parser.add_argument('-m', '--dms', action="store_true",
                        default=False, help='Delete Direct Messages')
    parser.add_argument('-t', '--tweets', action="store_true",
                        default=False, help='Delete Tweets')
    parser.add_argument('-g', '--debug', action="store_true",
                        default=False, help='Debug mode')
    parser.add_argument('-r', '--dryrun', action="store_true",
                        default=False, help='Dry run mode')

    args = parser.parse_args()

    DEBUG = args.debug
    DRYRUN = args.dryrun
    
    if DEBUG:
        print('🔗 Running in DEBUG mode')
    if DRYRUN:    
        print('🚲 Running in DRYRUN mode')

    if args.user_id:
        user_id = args.user_id
    else:
        user_id = YOUR_USER_ID

    if args.date:
        date = args.date
    else:
        last_montth = datetime.today() - timedelta(days=30)
        date = last_montth.strftime('%Y-%m-%d')

    if '' in [args.access_token, args.access_token_secret, user_id, date]:
        print("❌ ERROR: A mandatory parameter is missing")
        sys.exit(-1)

    twitter_api = twitter.Api(consumer_key=YOUR_APP_CONSUMER_KEY,
                              consumer_secret=YOUR_APP_CONSUMER_SECRET,
                              access_token_key=args.access_token,
                              access_token_secret=args.access_token_secret,
                              sleep_on_rate_limit=True)
    try:
        screen_name = twitter_api.GetUser(user_id).screen_name
        status_count = twitter_api.GetUser(user_id).statuses_count
    except twitter.TwitterError as error:
        print(f"❌ ERROR: {error.message[0]['message']}")
        sys.exit(-1)

    print(f'🐥 Screen Name: {screen_name} - Number of tweets: {status_count}')

    if args.tweets:
        fetch_and_delete(twitter_api, user_id, date, 'Tweet')
    if args.dms:
        fetch_and_delete(twitter_api, user_id, date, 'Direct Message')

if __name__ == '__main__':
    main()
