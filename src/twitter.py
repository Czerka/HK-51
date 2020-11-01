import tweepy
from datetime import datetime, timedelta
from os import getenv


class Twitter():
    def __init__(self, follows: list, tweets: list):
        self.__key = getenv('TWITTER_KEY')
        self.__secret = getenv('TWITTER_SECRET')
        self.__bearer = getenv('TWITTER_BEARER')
        self.__access_token = getenv('TWITTER_ACCESS_TOKEN')
        self.__access_secret = getenv('TWITTER_ACCESS_SECRET')

        self.__auth = tweepy.OAuthHandler(self.__key, self.__secret)
        self.__auth.set_access_token(self.__access_token, self.__access_secret)
        self.api = tweepy.API(self.__auth)
        self.follows = follows
        self.tweets = tweets

    def fetch(self):
        # date = datetime.strptime(ARGS[1], '%Y-%m-%d %H:%M:%S')

        array = []
        for follow in self.follows:
            latest = next(
                (t for t in self.tweets if t['_id'] == follow['account']), None)

            if latest:
                date = latest['created_at']
            else:
                date = datetime.now() - timedelta(days=1)

            user = self.api.get_user(follow['account'])
            for item in user.timeline():
                if item.author.screen_name != follow['account']:
                    continue
                if item.in_reply_to_status_id or item.in_reply_to_user_id:
                    continue
                if item.created_at <= date:
                    continue
                array.append({
                    'twitter_id': str(item.id),
                    'author': item.author.screen_name,
                    'created_at': item.created_at
                })
        return array
