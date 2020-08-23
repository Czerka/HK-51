from dotenv import load_dotenv
from os import getenv as ENV
from sys import argv as ARGS
import tweepy
from datetime import datetime
import GetOldTweets3 as got

load_dotenv()
TWITTER_KEY = ENV('TWITTER_KEY')
TWITTER_SECRET = ENV('TWITTER_SECRET')
TWITTER_BEARER = ENV('TWITTER_BEARER')
TWITTER_ACCESS_TOKEN = ENV('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = ENV('TWITTER_ACCESS_SECRET')

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)

# ARGS[1] is last created_at "yyyy-mm-dd H:i:s"
date = datetime.strptime(ARGS[1], '%Y-%m-%d %H:%M:%S')

file = open('ids.txt', 'w')

user = api.get_user("SWTOR")
for item in user.timeline():
    if item.author.screen_name != "SWTOR": continue
    if item.in_reply_to_status_id or item.in_reply_to_user_id: continue
    if item.created_at <= date: continue
    file.write(str(item.id) + '\t' + item.created_at.strftime('%Y-%m-%d %H:%M:%S') + '\n')

file.close()
