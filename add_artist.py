import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def add(uri):
    with open("data.json") as data:
        data_list = json.load(data)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    artist_name = spotify.artist(uri)['name']
    albums = spotify.artist_albums(uri, 'album', limit=5)['items']
    songs = spotify.artist_albums(uri, 'single', limit=5)['items']
    appears_on = spotify.artist_albums(uri, 'appears_on', limit=5)['items']

    converted_albums = []
    converted_songs = []
    converted_appears_on = []

    for album in albums:
        new_album_data = {
            'artists': [
                artist['name'] for artist in album['artists']
            ],
            'name': album['name'],
            'uri': album['uri']
        }

        converted_albums.append(new_album_data)

    for song in songs:
        new_song_data = {
            'artists': [
                artist['name'] for artist in song['artists']
            ],
            'name': song['name'],
            'uri': song['uri']
        }

        converted_songs.append(new_song_data)

    for appear_on in appears_on:
        new_appear_on_data = {
            'appear_type': appear_on['album_type'],
            'artists': [
                artist['name'] for artist in appear_on['artists']
            ],
            'name': appear_on['name'],
            'uri': appear_on['uri']
        }

        converted_appears_on.append(new_appear_on_data)

    x = {
        'artist_uri': uri,
        'artist_name': artist_name,
        'artist_album': converted_albums,
        'artist_songs': converted_songs,
        'artist_appears_on': converted_appears_on
    }

    data_list.append(x)

    with open("data.json", 'w') as json_file:
        json.dump(data_list, json_file,
                  indent=4,
                  separators=(',', ': '))
