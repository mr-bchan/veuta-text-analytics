
#Import the necessary methods from tweepy library
import  json

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


def saveToFile(tweet_outputs,  file):
    with open(file, 'w') as f:
        json.dump(tweet_outputs, f, ensure_ascii=True)



#Provide Twitter API credentials
#Link --> https://www.gabfirethemes.com/create-twitter-api-key/

#Replace  existing keys with yours
access_token = "711884071572414464-XIyHKXn5spCJuPfe4stCO8VvZ9WZkVV"
access_token_secret = "Sp3yYx3yLVGEj2lfmLb84ZQ4UtHinVyNtWw7FrTkLrc21"
consumer_key = "HawSfq2HCfUdx2k7bDIPc1e5A"
consumer_secret = "Z2UlJX2mv58qHXIZAR0VB1fIsDx9Gd4gUskLYS8seGQGzyJdDf"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    tweet_data = []
    tweet_size = 100

    def on_data(self, data):

        tweet =  json.loads(data)['text'].replace('\n', '\\n')
        self.tweet_data.append(tweet)

        print("Tweet: " + str(len(self.tweet_data)) )
        if len(self.tweet_data) <= self.tweet_size:
            return True
        else:
            return False

    def on_error(self, status):
        print status


if __name__ == '__main__':

  # This handles Twitter authetitication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'

    watchwords = { 'burger','spaghetti','french fries','mcdonalds'}
    stream.filter(track=watchwords)

    file = "twiiter-stream-output-" + str(l.tweet_size) + ".txt"
    saveToFile(l.tweet_data, file)
