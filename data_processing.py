import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import logging

import json
import sys

logging.basicConfig(format='%(asctime)s %(message)s')

class TwitterDataExtraction(object):

    def __init__(self, start_date=None):
        self.start_date = start_date
        self.authorization = {
            'apikey': 'XXXXXXXXXXXXXXXXXXXXXXXXX',
            'apisecret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            'accesstoken': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx',
            'accesssecret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxxx'
        }
        auth = OAuthHandler(self.authorization['apikey'],
                            self.authorization['apisecret'])
        auth.set_access_token(self.authorization['accesstoken'],
                              self.authorization['accesssecret'])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)


        # Possible hashtags for General elections in Pakistan obtained from twitter manually
        self.possible_hashtags = ['#PakistanElections2018',
                             '#PakElections2018',
                             '#Elections2018',
                             '#GeneralElections2018',
                             '#PakVotes2018',
                             '#pakistanelections',
                             '#Pakelections',
                             '#VoteForPakistan',
                             '#Election2k18',
                             '#GE2018']


    def extract(self):
        # Collecting Twitter Data for hashtag
        data = []
        for tag in self.possible_hashtags:
            logging.warning('Collecting data for Hashtag {}'.format(tag))
            try:
                tweets_response = tweepy.Cursor(self.api.search,q=tag,count=100,
                                           lang="en",
                                           since=self.start_date).items()
            except ValueError:
                logging.warning('The date "{}" is not correct format. '
                                'The format is "YYYY-MM-DD" '.format(self.start_date))
                sys.exit(0)

            for tweet in tweets_response:
                data.append(tweet._json)
            print(len(data))

        final_data = json.dumps(data, indent=4, sort_keys=True) # make json data pretty
        return final_data

    def remove_duplicate_tweets(self, tweets_data):
        return [i for n, i in enumerate(tweets_data) if i not in tweets_data[n + 1:]]


    def clean(self, data):
            tweets_data = json.load(data)
            unique_tweets = self.remove_duplicate_tweets(tweets_data)
            del tweets_data # deleting to save some memory

            # few possible hashtag tokens in post related to pakistan elections
            imp_tokens = ['pakistan', 'pti', 'ptiofficial', 'ppp', 'pti', 'pmln', 'mqm',
                          'imrankhan', 'nawazshareef', 'zardari',
                          'bilawal', 'maryamnawaz', 'bhutto']

            cleaned_data = []
            for tweet in unique_tweets:
                text = tweet['text'].lower()
                hashtags = [tag['text'] for tag in tweet['entities']['hashtags']]
                location = tweet['user']['location'].lower()
                for token in imp_tokens:
                    if (token in text or
                        token in hashtags or
                        token in location):
                        cleaned_data.append(tweet)
                        break

            final_data = json.dumps(cleaned_data, indent=4, sort_keys=True)
            return final_data





