# -*- encoding: utf-8 -*-
#
#  Twoblivion
#  
#  Author: Jean-Philippe Teissier ( @Jipe_ ) 
#    
#  This work is licensed under the GNU General Public License
#
#  version 0.2

import optparse
import os
import twitter
from dateutil.parser import *
from dateutil.relativedelta import *
from datetime import *

YOUR_APP_CONSUMER_KEY = ""
YOUR_APP_CONSUMER_SECRET = ""					# Well… not really a secret…

YOUR_ACCESS_TOKEN = ""
YOUR_ACCESS_TOKEN_SECRET = ""

YOUR_USER_ID = ""
TEST_DATE = "2012 01 01"

Debug = False

def DeleteTweets(TwApi, TweetsToDelete):
	""" Delete the tweets """

	for Tweet in TweetsToDelete:
		if Debug: print("[D] TweetID " + str(Tweet) + " deleted")
		try:
			TwApi.DestroyStatus(Tweet)	
		except twitter.TwitterError as e:
			print(u"[–] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
			pass

def DeleteDM(TwApi, DMToDelete):
	""" Delete the DMs """

	for DM in DMToDelete:
		if Debug: print("[D] Direct MessageID " + str(DM) + " deleted")
		try:
			TwApi.DestroyDirectMessage(DM)	
		except twitter.TwitterError as e:
			print(u"[-] ERROR: (" + str(e[0][0]['code'])+ u") " + e[0][0]['message'].decode('utf-8'))
			pass

def GetDirectMessagesToDelete(TwApi, Date):
	""" Get the list of DM to delete"""

	TotalDirectMessages = 0
	DirectMessagesToDelete = []

	print("[*] Retrieving the list of DM to delete (it might take a while...)")

	try:
		DirectMessages = TwApi.GetDirectMessages(count=200)									#Can't request more than 200 DM
	except twitter.TwitterError as e:
		print(u"[-] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
		exit(-1)

	while len(DirectMessages) > 1:
		TotalDirectMessages += len(DirectMessages)
		if Debug: print("[D] Got " + str(TotalDirectMessages) + " Direct Messages")
		MaxId = DirectMessages[-1].id
		for DM in DirectMessages:
			Delta = str(parse(DM.created_at, ignoretz=True) - parse(Date))
			if Debug: print("[D] ID: " + str(DM.id) + " - Date: " + DM.created_at + " R: " + Delta)
			if Delta[0] == "-":
				DirectMessagesToDelete.append(DM.id)
				if Debug: print("[D] " + str(DM.id) + " (" + DM.created_at + ") will be deleted")
		try:
			DirectMessages = TwApi.GetDirectMessages(count=200, max_id=MaxId)
		except twitter.TwitterError as e:
			print(u"[-] ERROR: (" + str(e[0][0]['code'])+ u") " + e[0][0]['message'].decode('utf-8'))
			exit(-1)

	print("[*] Got " + str(len(DirectMessagesToDelete)) + " DM to delete")

	return DirectMessagesToDelete


def GetTweetsToDelete(TwApi, UserId, Date):
	""" Get the list of tweets to delete"""
	
	TotalTweets = 0
	StatusesToDelete = []
	
	print("[*] Retrieving the list of tweets to delete (it might take a while...)")

	try:
		Statuses = TwApi.GetUserTimeline(user_id=UserId, count=200)						#Can't request more than 200 tweets
	except twitter.TwitterError as e:
		print(u"[—] ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
		exit(-1)
		
	while len(Statuses) > 1:
		TotalTweets += len(Statuses)
		if Debug: print("[D] Got " + str(TotalTweets) + " tweets")
		MaxId = Statuses[-1].id
		for S in Statuses:
			Delta = str(parse(S.created_at, ignoretz=True) - parse(Date))
			if Debug: print("[D] ID: " + str(S.id) + " - Date: " + S.created_at + " R: " + Delta)
			if Delta[0] == "-":
				StatusesToDelete.append(S.id)
				if Debug: print("[D] " + str(S.id) + " (" + S.created_at + ") will be deleted")
		try:
			Statuses = TwApi.GetUserTimeline(user_id=UserId, count=200, max_id=MaxId)
		except twitter.TwitterError as e:
			print(u"[-]ERROR: (" + str(e[0][0]['code']) + u") " + e[0][0]['message'].decode('utf-8'))
			exit(-1)
	
	print("[*] Got " + str(len(StatusesToDelete)) + " tweets to delete")
	
	return StatusesToDelete
	
def main():
	""" Here we go """
	
	global Debug
	TweetsToDelete = []
	DirectMessagesToDelete = []
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
		Date = TEST_DATE

	TwApi = twitter.Api(consumer_key=YOUR_APP_CONSUMER_KEY,
						consumer_secret=YOUR_APP_CONSUMER_SECRET,
						access_token_key=AcsTokenKey,
	 					access_token_secret=AcsTokenSecret)
	
	print("[*] Screen Name:" + TwApi.GetUser(UserId).GetScreenName() + " #tweets: " + str(TwApi.GetUser(UserId).statuses_count))
	
	if Tweets:
		TweetsToDelete = GetTweetsToDelete(TwApi, UserId, Date)
		DeleteTweets(TwApi, TweetsToDelete)
	
	if DM:
		DirectMessagesToDelete = GetDirectMessagesToDelete(TwApi, Date)
		DeleteDM(TwApi, DirectMessagesToDelete)
	
if __name__ == '__main__':
	main()