"""
    File with algorithm to check if artist has added new track/album
"""
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from converted_artist_data import convert
from twitter import send_tweet


def get_artists():
    """
        Getting all artists' data
        :return artists_data: list of all artists' data
    """

    with open("data.json", "r") as data:
        artists_data = json.load(data)

    return artists_data


def main():
    """
        Main function to pass artist to check releasing and passing checked data to save
        :return: None
    """
    # list for refreshed artist's data
    refreshed_artists = []

    artists_data = get_artists()
    for artist in artists_data:
        refreshed_data = check(artist)
        refreshed_artists.append(refreshed_data)

    # save refreshed data to data.json file
    with open("data.json", 'w') as json_file:
        json.dump(refreshed_artists, json_file,
                  indent=4,
                  separators=(',', ': '))

    print("Refreshed data saved!")


def check(artist):
    """
        Function to check the newest tracks and albums
        :param artist: artist's data json object
        :return refreshed_artist_data: artist's data json object with refreshed data
    """

    # get access to artist's data from Spotify API by artist's Spotify URI
    actual_uri = artist['artist_uri']
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # get artist's the newest tracks, albums and songs on which appeared on
    albums = spotify.artist_albums(actual_uri, 'album', limit=5)['items']
    songs = spotify.artist_albums(actual_uri, 'single', limit=5)['items']

    # check if the newest album's uri is different as the newest in database
    # albums in lists are from the newest to the oldest
    if len(artist['artist_albums']) == 0 or albums[0]['uri'] != artist['artist_albums'][0]:
        # check from the oldest to the newest response albums if album is in app database
        for album in albums[::-1]:
            if album['uri'] not in artist['artist_albums']:
                # get all album's artists
                artists = ", ".join(album_artist['name'] for album_artist in album['artists'])
                if len(album['artists']) > 1:
                    message = "{0} have just released new album \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                        format(artists, album['name'], album['external_urls']['spotify'])
                else:
                    message = "{0} has just released new album \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                          format(artists, album['name'], album['external_urls']['spotify'])
                print(message)
                send_tweet(album['name'], album['artists'], message, album['images'][0]['url'])

    # check if the newest song's uri is different as the newest in database
    # songs in lists are from the newest to the oldest
    if len(artist['artist_songs']) == 0 or songs[0]['uri'] != artist['artist_songs'][0]:
        # check from the oldest ot the newest response songs if song is in app database
        for song in songs[::-1]:
            if song['uri'] not in artist['artist_songs']:
                # get all song's artists
                artists = ", ".join(song_artist['name'] for song_artist in song['artists'])
                if song['total_tracks'] == 1:
                    if len(song['artists']) > 1:
                        message = "{0} have just released new song \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                              format(artists, song['name'], song['external_urls']['spotify'])
                    else:
                        message = "{0} has just released new song \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                              format(artists, song['name'], song['external_urls']['spotify'])
                else:
                    if len(song['artists']) > 1:
                        message = "{0} have just released new EP \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                              format(artists, song['name'], song['external_urls']['spotify'])
                    else:
                        message = "{0} has just released new EP \"{1}\", which you can listen to on Spotify!\n\n{2}".\
                              format(artists, song['name'], song['external_urls']['spotify'])
                print(message)
                send_tweet(song['name'], song['artists'], message, song['images'][0]['url'])

    print("{0}'s data refreshed!".format(artist['artist_name']))

    refreshed_artist_data = convert(actual_uri, artist['artist_name'], [albums, songs])

    return refreshed_artist_data
