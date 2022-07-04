"""
    File with function to send Tweet with release information
"""


import os

import requests

from api_twitter import get_access


def send_tweet(title, artists, message, image):
    """
        Function to send Tweet
        :param title: track / album title
        :param artists: list of track / album artists
        :param message: Tweet text
        :param image: track / album cover photo url
        :return: None
    """

    # creating artists hashtags
    hashtags = " ".join(["#" + artist['name'].replace(" ", "_") for artist in artists])
    hashtags = '#Spotify #' + title.replace(" ", "_") + " " + hashtags

    # adding hashtags on the bottom of the text
    message += f"\n\n{hashtags}"

    # downloading cover photo
    img_data = requests.get(image).content
    with open("temp_photo.jpg", "wb") as handler:
        handler.write(img_data)

    # sending Tweet
    api = get_access()
    media = api.media_upload("temp_photo.jpg")
    os.remove("temp_photo.jpg")
    api.update_status(status=message, media_ids=[media.media_id])
    print("Tweet sent")
