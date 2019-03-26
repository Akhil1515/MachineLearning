import tweepy
from tweepy import OAuthHandler
import re
from collections import OrderedDict

consumer_key = 'SxlXMfpNtBNglE4cR3H0gWj5v'
consumer_secret = 'Qm94AlXGvcs4Z0jH3tC3zVLWPqxskLpJmLyh7mrhVddvooZCds'
access_token = '966224948-xzlXTwYyJvrYaTMKoy7OJeQD2Rz9V24OUJSKqmZN'
access_secret = 'BHXdUUhuUsbpFWJnocfSOTKlXs7p7NVsb1ETHEiYvJjJK'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def get_tweets(query, count):
    tweets = []

    try:
        #fetched_tweets = api.search(q=query, count=count)
        for tweet in tweepy.Cursor(api.search,
                                   q=query,
                                   count=count,
                                   result_type="recent",
                                   include_entities=True,
                                   lang="en").items():
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets

    except tweepy.TweepError as e:
        print("Error : " + str(e))
tweets = get_tweets(query = '#Trump', count = 2000)
tweets0= get_tweets(query = '#2018Midterm', count = 2000)
tweets1= get_tweets(query = '#election', count = 2000)

def clean_tweet (tweet):
    tweets1= ' '.join(re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',r' ' , str (tweet)).split())
    list1=['text','RT']
    for x in list1:
        tweets1 = tweets1.replace(x, '\n')
    return tweets1


def create_file (tweet):
    if tweet==tweets:
        file = open("tweet0" + "Data.txt", "w")
        file.write(clean_tweet(tweet))
        file.close()
    elif tweet==tweets1:
        file = open("tweet1" + "Data.txt", "w")
        file.write(clean_tweet(tweet))
        file.close()
    else:
        file = open("tweet" + "Data.txt", "w")
        file.write(clean_tweet(tweet))
        file.close()


create_file(tweets)
create_file(tweets0)
create_file(tweets1)


filenames = ['tweetData.txt', 'tweet0Data.txt', 'tweet1Data.txt']
with open('combinedData.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)


with open("combinedData.txt","r") as f, open("combinedData1.txt","w") as outfile:
    for i in f.readlines():
           if not i.strip():
               continue
           if i:
               outfile.write(i)

fin1=open("combinedData2.txt","w")
with open('combinedData1.txt',"r") as fin:
    lines = (line for line in fin)
    unique_lines = OrderedDict.fromkeys( (line for line in lines if line) )
for i in unique_lines.keys():
    fin1.write(i)
