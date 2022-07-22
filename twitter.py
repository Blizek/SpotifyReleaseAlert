"""
    File with function to send Tweet with release information
"""


import os

import requests
from datetime import date, datetime

from api_twitter import get_access


def send_tweet(title, artists, message, image, link, release_date):
    """
        Function to send Tweet
        :param title: track / album title
        :param artists: list of track / album artists
        :param message: Tweet text
        :param image: track / album cover photo url
        :param link: link to Spotify
        :param release_date: song/album release date
        :return: None
    """

    # creating artists hashtags
    hashtags = " ".join(["#" + artist['name'].replace(" ", "_") for artist in artists])
    hashtags = '#Spotify #' + title.replace(" ", "_").replace("(", "").replace(")", "") + " " + hashtags

    # adding hashtags on the bottom of the text
    message += f"\n\n{hashtags}"

    if len(message) >= 280:
        message = f"{artists[0]['name']} has just released something new on Spotify!\n\n{link}\n\n#Spotify #{artists[0]['name'].replace(' ', '_')}"

    # check if this song/album has been realised more than 7 days ago
    release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
    today = date.today()
    delta = today - release_date
    if delta.days <= 7:
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
    else:
        print("That was released earlier than one week ago")
