"""
    Adding artist to database algorithm
"""

import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from converted_artist_data import convert


def add(uri):
    """Adding algorithm"""

    # open file with data
    with open("data.json") as data:
        data_list = json.load(data)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # Try to get artist data if Spotify URI is invalid print that information and end algorithm
    try:
        artist_name = spotify.artist(uri)['name']
        albums = spotify.artist_albums(uri, 'album', limit=5)['items']
        songs = spotify.artist_albums(uri, 'single', limit=5)['items']
    except spotipy.SpotifyException:
        print("Invalid artist's Spotify URI")
        return None

    # list of every artist's uri
    uri_list = [artist['artist_uri'] for artist in data_list]

    # If that URI is in db print that information
    if uri in uri_list:
        print("{0} is already in our database".format(artist_name))
        return None

    # get ready artist's data json object
    new_artist_data = convert(uri, artist_name, [albums, songs])

    # add this data to list of all artists' data
    data_list.append(new_artist_data)

    # save that in file
    with open("data.json", 'w') as json_file:
        json.dump(data_list, json_file,
                  indent=4,
                  separators=(',', ': '))

    # print artist's Spotify URL
    print("https://open.spotify.com/artist/{0}".format(uri.split(":")[-1]))

    # print that artist was added correctly
    print("{0} added correctly".format(artist_name))
