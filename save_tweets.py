import sys
import requests
import requests_oauthlib
import json
import os

def get_tweets(my_auth):
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    response = requests.get(query_url, auth=my_auth, stream=True)
    return response

def main():
    ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
    CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    f = open("tweets.txt","a")
    resp = get_tweets(my_auth)
    for line in resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            f.write(tweet_text)
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)
    f.close()

if __name__ == "__main__":
    main()