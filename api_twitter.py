"""
    File with function to get connection to Twitter API
"""


import tweepy

from twitter_api_keys import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def get_access():
    """
        Function to connect with Twitter API
        :return tweeter: object to access Twitter API
    """
    twitter_auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    twitter_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    tweeter = tweepy.API(twitter_auth, wait_on_rate_limit=True)

    return tweeter
