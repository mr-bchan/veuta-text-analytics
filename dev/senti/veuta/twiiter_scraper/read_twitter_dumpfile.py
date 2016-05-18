import json

import pandas as pd


def loadJson(file_name):
    with open(file_name, 'r') as f:
        input_tweets = json.load(f)
        return input_tweets


filename = "@KFC_UKI-dump-1033 tweets-sample.json"

input_tweets = loadJson(filename)

tweets = pd.DataFrame()

tweets['message'] = map(lambda tweet: tweet['message'], input_tweets)
tweets['response'] = map(lambda tweet: tweet['response'], input_tweets)
tweets['response_id'] = map(lambda tweet: tweet['response_id'], input_tweets)
tweets['date'] = map(lambda tweet: tweet['date'], input_tweets)

print tweets['message'][1020]
print tweets['response'][1019]

print tweets[1:100]
print tweets.head()
