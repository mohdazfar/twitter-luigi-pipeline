from pymongo import MongoClient


class MongoDBClient(object):
    def __init__(self):
        '''Creates connection to MongoDB.'''
        client = MongoClient('localhost', 27017)
        self.db = client.luigipipeline

    def insert_data(self, json_data):
        '''Insert bulk data to twitter collection'''
        self.db.twitter.insert_many(json_data)

    def get_data(self):
        '''Get all data from twitter collection'''
        data = self.db.twitter.find()
        return list(data)

