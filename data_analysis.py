import json
from datetime import datetime
from collections import Counter, defaultdict

class TwitterAnalysis(object):

    def __init__(self, data):
        self.unique_tweets = []
        self.daily_tweets = {}
        self.hashtags = {}
        self.comparison_tags = {}
        self.retweets_count = 0
        self.locations = 0
        self.tweets_data = json.load(data)

    def get_unique_users(self, tweet):
        '''Get user id from twitter resposne data'''
        self.unique_tweets.append(tweet['user']['id'])

    def get_retweets(self, tweet):
        '''If the tweet is retweeted then we add to list for count'''
        if tweet['retweeted']:
            self.retweets_count += 1

    def get_daily_tweets(self, tweet):
        '''Get count of daily tweets'''
        date = tweet['created_at']
        date = datetime.strptime(date,  '%a %b %d %H:%M:%S %z %Y').strftime('%d-%m-%y')
        if date in self.daily_tweets:
            self.daily_tweets[date] += 1
        else:
            self.daily_tweets[date] = 0
            self.daily_tweets[date] += 1



    def get_top_hashtags(self, tweet, comprison_tags=[]):
        '''
        Get each hashtag count. Comparison_tags must contain
        exactly 2 hashtags for comparison. Otherwise empty []
        '''
        hashtags_list = [tag['text'] for tag in tweet['entities']['hashtags']]

        for tag in hashtags_list:
            if tag in self.hashtags:
                self.hashtags[tag] += 1
                self.compare_tags(tag, hashtags_list, comprison_tags)
            else:
                self.hashtags[tag] = []
                self.hashtags[tag] += 1
                self.compare_tags(tag, hashtags_list, comprison_tags)

    def get_tweet_location(self, tweet):
        '''
        Get location for each tweet. If location is "Pakistan"
        then seperate those tweets.
        '''
        location = tweet['user']['location']
        if 'pakistan' not in location.lower():
            self.locations += 1


    def compare_tags(self, tag, hashtags_list, comparison_tags):
        '''
        Compare the tags. Provides information of other tags used
        with the comparison tags to understand why there the counts
        are high or low.
        '''
        list_len = len(comparison_tags)
        if list_len == 2:
            tag = tag.lower()
            if tag == comparison_tags[0] or tag == comparison_tags[1]:
                if tag in self.comparison_tags:
                    self.comparison_tags[tag].extend(hashtags_list)
                else:
                    self.comparison_tags[tag] = []
                    self.comparison_tags[tag].extend(hashtags_list)
        elif list_len > 2 or list_len == 1:
            raise ValueError('Comprison list must contain exactly 2'
                             ' elements to compare')


    def get_compare_tags_results(self, comparison_tags):
        tag0 = self.comparison_tags[comparison_tags[0]]
        unique_tag0 = list(set(tag0))
        count_tag0 = defaultdict(int)

        for t in tag0:
            count_tag0[t] += 1

        tag1 = self.comparison_tags[comparison_tags[1]]
        unique_tags_tag1 = list(set(tag1))
        count_tag1 = defaultdict(int)

        for t in tag1:
            count_tag1[t] += 1

        tag0_sorted_by_value = sorted(count_tag0.items(), key=lambda kv: kv[1])
        tag1_sorted_by_value = sorted(count_tag1.items(), key=lambda kv: kv[1])

        return [tag0_sorted_by_value, tag1_sorted_by_value]


    def run(self):
        comparison_tags = ['nawazsharif', 'imrankhan'] # Exactly 2 tags need for comparison
        for tweet in self.tweets_data:
            self.get_unique_users(tweet)
            self.get_daily_tweets(tweet)
            self.get_top_hashtags(tweet, comparison_tags)
            self.get_retweets(tweet)
            self.get_tweet_location(tweet)


        unique_users =  len(list(set(self.unique_tweets)))
        retweets_count = self.retweets_count
        dailytweets = list(sorted([(i, self.daily_tweets[i]) for i in self.daily_tweets]))
        hashtags = list(sorted([[i, self.hashtags[i]] for i in self.hashtags], key=lambda x: x[1]))

        if comparison_tags != []:
            comparison_tags_result = self.get_compare_tags_results(comparison_tags)

        pct_tweets_pak = round((len(self.tweets_data)- self.locations)/len(self.tweets_data)*100, 2)
        pct_tweets_out = round(self.locations/len(self.tweets_data)*100, 2)
        pct_tweets_retweeted = round(retweets_count/len(self.tweets_data)*100, 2)

        results = {'tweets_count': len(self.tweets_data),
                   'tweets_pak': pct_tweets_pak,
                   'tweets_out': pct_tweets_out,
                   'unique_users': unique_users,
                   'pct_tweets_retweeted': pct_tweets_retweeted,
                   'daily_tweets_count': dailytweets,
                   'top_15_hashtags': hashtags[len(hashtags)-15:]}
        final_data = json.dumps(results, indent=4, sort_keys=True)
        return final_data
