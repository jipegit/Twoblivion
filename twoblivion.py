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
__version__ = "0.5.1"

import argparse
import re
import sys
from datetime import datetime, timedelta

import twitter
from dateutil.parser import parse

YOUR_APP_CONSUMER_KEY = "REPLACEME"
YOUR_APP_CONSUMER_SECRET = "REPLACEME"
YOUR_ACCESS_TOKEN = "REPLACEME"
YOUR_ACCESS_TOKEN_SECRET = "REPLACEME"
YOUR_USER_ID = "REPLACEME"

DEBUG = False

WHITELIST = [
    re.compile(r'Verifying myself: I am \w+ on http://Keybase.io')
]

def delete_items(twitter_api, items_to_delete, item_type):
    """Delete a bunch of Tweets or DMs."""

    total_items = len(items_to_delete)
    i = 1

    print('[*] Deleting your old {0:s}s'.format(item_type))
    for item in items_to_delete:
        try:
            if item_type == 'Tweet':
                twitter_api.DestroyStatus(item)
            elif item_type == 'Direct Message':
                twitter_api.DestroyDirectMessage(item)
            if DEBUG:
                print('[D] [{0:d}/{1:d}] {2:s} ID {3:s} has been '
                      'deleted'.format(i, total_items, item_type, str(item)))
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            i += 1
        except twitter.TwitterError as error:
            print('ERROR: {0:s}'.format(str(error)))

def fetch_items(twitter_api, userid, item_type, max_id):
    """Fetches Tweets or DMs from a users' account."""
    try:
        if item_type == 'Tweet':
            return twitter_api.GetUserTimeline(user_id=userid, max_id=max_id)
        return twitter_api.GetDirectMessages(max_id=max_id) + \
               twitter_api.GetSentDirectMessages(max_id=max_id)
    except twitter.TwitterError as error:
        print('[—] ERROR: {0:s}'.format(str(error)))
        sys.exit(-1)

def fetch_and_delete(twitter_api, user_id, date, item_type):
    """Get the list of Tweets or Direct Messages to delete"""

    global DEBUG # pylint: disable=global-statement

    print('[*] Retrieving the list of {0:s}s to delete '
          '(it might take a while...)'.format(item_type))

    items_to_delete = []
    max_id = 0
    while True:
        items = fetch_items(twitter_api, user_id, item_type, max_id)
        if not items:
            break
        max_id = items[-1].id-1
        for item in items:
            if parse(item.created_at, ignoretz=True).date() < parse(date).date():
                for whitelist_item in WHITELIST:
                    if whitelist_item.match(item.text):
                        continue
                items_to_delete.append(item.id)
                if DEBUG:
                    print("%d" % item.id)
                    print("[{0:s}] {1:d} {2:s}".format(
                        item.created_at, item.id, item.text[:60].encode('utf-8', errors='ignore')))

    print("[*] Got {0:d} {1:s} to delete".format(
        len(items_to_delete), item_type))
    delete_items(twitter_api, items_to_delete, item_type)

def main():
    """Here we go!"""

    global DEBUG # pylint: disable=global-statement

    parser = argparse.ArgumentParser(
        description='Wipe your tweets from history.')
    parser.add_argument('-k', '--access_token',
                        default=YOUR_ACCESS_TOKEN,
                        help='Your Access Token')
    parser.add_argument('-s', '--access_token_secret',
                        default=YOUR_ACCESS_TOKEN_SECRET,
                        help='Your Access Token Secret')
    parser.add_argument('-u', '--user_id',
                        default=False, help='Your User ID')
    parser.add_argument('-d', '--date',
                        default=False,
                        help='The date from which you want to '
                             'delete Tweets or DMs')
    parser.add_argument('-m', '--dms', action="store_true",
                        default=False, help='Delete Direct Messages')
    parser.add_argument('-t', '--tweets', action="store_true",
                        default=False, help='Delete Tweets')
    parser.add_argument('-g', '--debug', action="store_true",
                        default=DEBUG, help='Debug mode')

    args = parser.parse_args()

    if args.debug:
        DEBUG = True

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
        print("[-] ERROR: A mandatory parameter is missing")
        sys.exit(1)

    print('Twoblivion v' + __version__)

    twitter_api = twitter.Api(consumer_key=YOUR_APP_CONSUMER_KEY,
                              consumer_secret=YOUR_APP_CONSUMER_SECRET,
                              access_token_key=args.access_token,
                              access_token_secret=args.access_token_secret)
    try:
        screen_name = twitter_api.GetUser(user_id).screen_name
        status_count = twitter_api.GetUser(user_id).statuses_count
    except twitter.TwitterError as error:
        print('[—] ERROR: {0:s}'.format(str(error)))
        sys.exit(-1)


    print('[*] Screen Name: {0:s} - Number of tweets {1:d}'.format(
        screen_name, status_count))

    if args.tweets:
        fetch_and_delete(twitter_api, user_id, date, 'Tweet')
    if args.dms:
        fetch_and_delete(twitter_api, user_id, date, 'Direct Message')

if __name__ == '__main__':
    main()
