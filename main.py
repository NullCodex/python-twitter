import socket
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

def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line)
            tweet_text = full_tweet['text']
            tcp_connection.send(tweet_text + '\n')
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)


def main():
    ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
    ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
    CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
    my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)
    TCP_IP = "localhost"
    TCP_PORT = 9009
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    conn, addr = s.accept()
    print("Connected... Starting getting tweets.")
    resp = get_tweets(my_auth)
    send_tweets_to_spark(resp, conn)


if __name__ == "__main__":
    main()