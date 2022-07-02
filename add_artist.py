import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def add(uri):
    with open("data.json") as data:
        data_list = json.load(data)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    artist_name = spotify.artist(uri)['name']
    albums = spotify.artist_albums(uri, 'album', limit=50)['items']
    songs = spotify.artist_albums(uri, 'single', limit=50)['items']
    appears_on = spotify.artist_albums(uri, 'appears_on', limit=50)['items']

    x = {
        'artist_uri': uri,
        'artist_name': artist_name,
        'artist_album': albums,
        'artist_songs': songs,
        'artist_appears_on': appears_on
    }

    data_list.append(x)

    with open("data.json", 'w') as json_file:
        json.dump(data_list, json_file,
                  indent=4,
                  separators=(',', ': '))
