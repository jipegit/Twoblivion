#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#  Twoblivion
#
#  Author: Jean-Philippe Teissier ( @Jipe_ )
#
#  This work is licensed under the GNU General Public License
#
__version__ = "0.4.3"

import optparse
import sys
import twitter
from dateutil.parser import *
from dateutil.relativedelta import *
from datetime import *

YOUR_APP_CONSUMER_KEY = ""
YOUR_APP_CONSUMER_SECRET = ""                    # Well… not really a secret…

YOUR_ACCESS_TOKEN = ""
YOUR_ACCESS_TOKEN_SECRET = ""

YOUR_USER_ID = ""

Debug = False


def DeleteItems(TwApi, ItemsToDelete, ItemType):
    """ Delete a bunch of Tweets or DMs """

    TotalItems = len(ItemsToDelete)
    i = 1

    print("[*] Deleting your old " + ItemType + "s")
    for Item in ItemsToDelete:
        try:
            if ItemType == "Tweet":
                TwApi.DestroyStatus(Item)
            elif ItemType == "Direct Message":
                TwApi.DestroyDirectMessage(Item)
            if Debug:
                print("[D] [" + str(i) + "/" + str(TotalItems) + "] " + ItemType + " ID " + str(Item) + " has been deleted")
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            i += 1
        except twitter.TwitterError as e:
            print(u"[-] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
            pass
    print("")


def GetItemsToDelete(TwApi, UserId, Date, ItemType):
    """ Get the list of Tweets or Direct Messages to delete"""

    TotalItems = 0
    ItemsToDelete = []
    Items = None

    print("[*] Retrieving the list of " + ItemType + "s to delete (it might take a while...)")

    try:
        if ItemType == "Tweet":
            Items = TwApi.GetUserTimeline(user_id=UserId, count=200)                                        #Can't request more than 200 Items at a time
        elif ItemType == "Direct Message":
            Items = TwApi.GetDirectMessages(count=200)
            Items = Items + TwApi.GetSentDirectMessages(count=200)
    except twitter.TwitterError as e:
        print(u"[—] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
        exit(-1)

    while len(Items) > 1:
        TotalItems += len(Items)
        if Debug: print("[D] Got " + str(TotalItems) + " " + ItemType)
        MaxId = Items[-1].id
        for Item in Items:
            if parse(Item.created_at, ignoretz=True).date() < parse(Date).date():
                ItemsToDelete.append(Item.id)
                if Debug: print("[D] " + str(Item.id) + " (" + Item.created_at + ") will be deleted")
        try:
            if ItemType == "Tweet":
                Items = TwApi.GetUserTimeline(user_id=UserId, count=200, max_id=MaxId)                        #Can't request more than 200 Items at a time
            elif ItemType == "Direct Message":
                Items = TwApi.GetDirectMessages(count=200, max_id=MaxId)
        except twitter.TwitterError as e:
            print(u"[-] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
            exit(-1)

    print("[*] Got " + str(len(ItemsToDelete)) + " " + ItemType + "(s) to delete")

    return ItemsToDelete


def main():
    """ Here we go """

    global Debug
    Tweets = True
    DM = True

    Parser = optparse.OptionParser(usage='usage: %prog [options]')
    Parser.add_option('-k', '--accesstokenkey', default=False, dest="AccessTokenKey", help='Your Access Token')
    Parser.add_option('-s', '--accesstokensecret', default=False, dest="AccessTokenSecret", help='Your Access Token Secret')
    Parser.add_option('-u', '--userid', default=False, dest="UserId", help='Your User ID')
    Parser.add_option('-d', '--date', default=False, dest="Date", help='The date from which you want to delete Tweets or DM')
    Parser.add_option('-m', '--dmsonly', action="store_true", default=False, help='Only delete Direct Messages')
    Parser.add_option('-t', '--tweetsonly', action="store_true", default=False, help='Only delete Tweets')
    Parser.add_option('-g', '--debug', action="store_true", default=False, help='Debug mode')

    (options, args) = Parser.parse_args()

    if options.tweetsonly and options.dmsonly:
        Parser.error("[-] Options -m and -t are mutually exclusive")

    if options.tweetsonly:
        DM = False
    if options.dmsonly:
        Tweets = False

    if options.debug:
        Debug = True

    if options.AccessTokenKey:
        AcsTokenKey = options.AccessTokenKey
    else:
        AcsTokenKey = YOUR_ACCESS_TOKEN

    if options.AccessTokenSecret:
        AcsTokenSecret = options.AccessTokenSecret
    else:
        AcsTokenSecret = YOUR_ACCESS_TOKEN_SECRET

    if options.UserId:
        UserId = options.UserId
    else:
        UserId = YOUR_USER_ID

    if options.Date:
        Date = options.Date
    else:
        d = datetime.today() - timedelta(days=30)
        Date = d.strftime('%Y-%m-%d')

    if AcsTokenKey == "" or AcsTokenSecret == "" or UserId == "" or Date == "":
        print("[-] ERROR: A mandatory parameter is missing")
        exit(1)

    print("Twoblivion v" + __version__)

    TwApi = twitter.Api(consumer_key=YOUR_APP_CONSUMER_KEY,
                        consumer_secret=YOUR_APP_CONSUMER_SECRET,
                        access_token_key=AcsTokenKey,
                        access_token_secret=AcsTokenSecret)

    print("[*] Screen Name: " + TwApi.GetUser(UserId).GetScreenName() + " - Number of tweets: " + str(TwApi.GetUser(UserId).statuses_count))

    if Tweets:
        DeleteItems(TwApi, GetItemsToDelete(TwApi, UserId, Date, "Tweet"), "Tweet")

    if DM:
        DeleteItems(TwApi, GetItemsToDelete(TwApi, UserId, Date, "Direct Message"), "Direct Message")


if __name__ == '__main__':
    main()
