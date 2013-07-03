# -*- encoding: utf-8 -*-
#
#  Twoblivion
#  
#  Author: Jean-Philippe Teissier ( @Jipe_ ) 
#    
#  This work is licensed under the GNU General Public License
#

import optparse
import os
import twitter
from dateutil.parser import *
from dateutil.relativedelta import *
from datetime import *

TWOBLIVION_CONSUMER_KEY = ""
TWOBLIVION_CONSUMER_SECRET = ""					# Well… not really a secret…

YOUR_ACCESS_TOKEN = ""
YOUR_ACCESS_TOKEN_SECRET = ""

TEST_USER_ID = ""
TEST_DATE = "2011 01 01"

Debug = False

def DestroyTweets(TwApi, TweetsToDestroy):
	""" Destroy the tweets """

	for Tweet in TweetsToDestroy:
		if Debug: print "TweetID" + str(Tweet) + " destroyed"
		try:
			TwApi.DestroyStatus(Tweet)	
		except twitter.TwitterError as e:
			print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
			exit(-1)

def DestroyDM(TwApi, DMToDestroy):
	""" Destroy the DMs """

	for DM in DMToDestroy:
		if Debug: print "Direct MessageID" + str(DM) + " destroyed"
		try:
			TwApi.DestroyDirectMessage(DM)	
		except twitter.TwitterError as e:
			print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
			exit(-1)

def GetDirectMessagesToDestroy(TwApi, Date):
	""" Get the list of DM to destroy"""

	TotalDirectMessages = 0
	DirectMessagesToDestroy = []
	
	try:
		DirectMessages = TwApi.GetDirectMessages(count=200)									#Can't request more than 200 DM
	except twitter.TwitterError as e:
		print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
		exit(-1)

	while len(DirectMessages) > 1:
		TotalDirectMessages += len(DirectMessages)
		if Debug: print "Got " + str(TotalDirectMessages) + " Direct Messages"
		MaxId = DirectMessages[-1].id
		for DM in DirectMessages:
			Delta = str(parse(DM.created_at, ignoretz=True) - parse(Date))
			if Debug: print "ID: " + str(DM.id) + " - Date: " + DM.created_at + " R: " + Delta
			if Delta[0] == "-":
				DirectMessagesToDestroy.append(DM.id)
				if Debug: print str(DM.id) + " (" + DM.created_at + ") will be deleted"
		try:
			DirectMessages = TwApi.GetDirectMessages(count=200, max_id=MaxId)
		except twitter.TwitterError as e:
			print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
			exit(-1)

	print "Got " + str(len(DirectMessagesToDestroy)) + " DM to detroy"

	return DirectMessagesToDestroy


def GetTweetsToDestroy(TwApi, UserId, Date):
	""" Get the list of tweets to destroy"""
	
	TotalTweets = 0
	StatusesToDestroy = []
	
	try:
		Statuses = TwApi.GetUserTimeline(user_id=UserId, count=200)						#Can't request more than 200 tweets
	except twitter.TwitterError as e:
		print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
		exit(-1)
		
	while len(Statuses) > 1:
		TotalTweets += len(Statuses)
		if Debug: print "Got " + str(TotalTweets) + " tweets"
		MaxId = Statuses[-1].id
		for S in Statuses:
			Delta = str(parse(S.created_at, ignoretz=True) - parse(Date))
			if Debug: print "ID: " + str(S.id) + " - Date: " + S.created_at + " R: " + Delta
			if Delta[0] == "-":
				StatusesToDestroy.append(S.id)
				if Debug: print str(S.id) + " (" + S.created_at + ") will be deleted"
		try:
			Statuses = TwApi.GetUserTimeline(user_id=UserId, count=200, max_id=MaxId)
		except twitter.TwitterError as e:
			print "ERROR: (" + str(e[0][0]['code'])+") " + e[0][0]['message']
			exit(-1)
	
	print "Got " + str(len(StatusesToDestroy)) + " tweets to detroy"
	
	return StatusesToDestroy
	
def main():
	""" Here we go """
	
	global Debug
	TweetsToDestroy = []
	DirectMessagesToDestroy = []
	
	Parser = optparse.OptionParser(usage='usage: %prog [options]')
	Parser.add_option('-k', '--accesstokenkey', default=False, dest="AccessTokenKey", help='access_token_key')
	Parser.add_option('-s', '--accesstokensecret', default=False, dest="AccessTokenSecret", help='access_token_secret')
	Parser.add_option('-u', '--userid', default=False, dest="UserId", help='user_id')
	Parser.add_option('-d', '--date', default=False, dest="Date", help='date')
	Parser.add_option('-D', '--debug', action="store_true", default=False, help='debug mode')
	
	(options, args) = Parser.parse_args()

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
		UserId = TEST_USER_ID
	
	if options.Date:
		Date = options.Date
	else:
		Date = TEST_DATE
	
	TwApi = twitter.Api(consumer_key=TWOBLIVION_CONSUMER_KEY,
						consumer_secret=TWOBLIVION_CONSUMER_SECRET,
						access_token_key=AcsTokenKey,
	 					access_token_secret=AcsTokenSecret)
	
	print "Screen Name:" + TwApi.GetUser(UserId).GetScreenName() + " #tweets: " + str(TwApi.GetUser(UserId).statuses_count)
	
	TweetsToDestroy = GetTweetsToDestroy(TwApi, UserId, Date)
	DestroyTweets(TweetsToDestroy)
	
	DirectMessagesToDestroy = GetDirectMessagesToDestroy(TwApi, Date)
	DestroyDM(DirectMessagesToDestroy)
	
if __name__ == '__main__':
	main()