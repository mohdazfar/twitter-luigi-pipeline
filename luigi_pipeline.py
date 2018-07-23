from bson.json_util import dumps
import luigi
import json

from data_processing import TwitterDataExtraction
from data_analysis import TwitterAnalysis
from mongo_dump import MongoDBClient

class DataExtraction(luigi.Task):

    def run(self):
        twitter = TwitterDataExtraction("2018-07-15")
        data = twitter.extract()
        with self.output().open('w') as resultfile:
            resultfile.write(data)

    def output(self):
        return luigi.LocalTarget('./twitter_elections_data.json')


class DataPreprocessing(luigi.Task):

    def requires(self):
        return DataExtraction()

    def run(self):
        with self.input().open('r') as data:
            twitter = TwitterDataExtraction()
            cleaned_data = twitter.clean(data)

            with self.output().open('w') as outfile_cleaned:
                outfile_cleaned.write(cleaned_data)

    def output(self):
        return luigi.LocalTarget('./cleaned_twitter_data.json')


class DumpToDB(luigi.Task):

    def requires(self):
        return DataPreprocessing()

    def run(self):
        data = self.input().open('r')
        json_data = json.load(data)
        mongoclient = MongoDBClient()
        mongoclient.insert_data(json_data)


class DataAnalysis(luigi.Task):

    def requires(self):
        return DumpToDB()

    def run(self):
        mongoclient = MongoDBClient()
        data = mongoclient.get_data()
        analysis = TwitterAnalysis(data)
        results = analysis.run()
        with self.output().open('w') as resultfile:
            resultfile.write(results)

    def output(self):
        return luigi.LocalTarget('./results_twitter.json')


if __name__ == '__main__':
    luigi.run()
