import json

import tweepy
from tweepy import OAuthHandler
from tweepy import  TweepError


def formatTweet(api, tweet):
    json_format = {
                    'message' : api.get_status(tweet.in_reply_to_status_id).text,
                   'response' : tweet.text,
                    'date' : str(tweet.created_at.year) +"-" + str(tweet.created_at.month)+ "-" + str(tweet.created_at.day)
                            + " " + str(tweet.created_at.hour) + ":" + str(tweet.created_at.minute) + ":" + str(tweet.created_at.second),
                    'response_id' : tweet.id }
    return  ((json_format))

def saveToFile(tweet_outputs,  file):
    with open(file, 'w') as f:
        json.dump(tweet_outputs, f, ensure_ascii=True)
        print 'saved filename: ' + file


#Provide Twitter API credentials
#Link --> https://www.gabfirethemes.com/create-twitter-api-key/

#Replace  existing keys with yours
consumer_key = 'IojbOsgVAodzCjEReOIvbrHAZ'
consumer_secret = 'jKaksFPVzPC2pvUFSmPDBzBxjYtS33Q5OsKERODm7bJuPj0p25'
access_token = '711884071572414464-Tarn6siyCOt4N0CIhjBtVBqxHKrfIQy'
access_secret = 'LH2X0ZDjDYQn0Yg3Zv5GUOrmzuSZRgAvmaOhOOKYsEqgI'

screen_name = '@BurgerKingUK'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)


#Twitter account page to extract
screen_name = 'TripAdvisorUK'

#Get latest tweet
tweet_outputs = []
page =  api.user_timeline(screen_name = screen_name, count=1)

ctr = 1
tweet_outputs.append(formatTweet(api, page[0])) #get initial tweet
last_tweet = page[0].id #retrieve first tweet

number_of_tweets = 2000 #number of tweets to be retrieved

while(len(tweet_outputs) <= number_of_tweets):
    page =  api.user_timeline(screen_name = screen_name, count=500, max_id = last_tweet)
    for  tweet in page[1:]:
        try:
                if tweet.in_reply_to_status_id != None and tweet.text != None:
                             tweet_outputs.append(formatTweet(api, tweet))
                             print  "Tweet: " + str(len(tweet_outputs))
                             last_tweet = tweet.id
        except TweepError as te:
            print "Error encountered. - " + te.reason



file_name = screen_name+"-dump-"+ str(len(tweet_outputs)) + " tweets-sample.json"
saveToFile(tweet_outputs, file_name)

################################################################################
