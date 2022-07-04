"""
    File with algorithm to check if artist has added new track/album
"""
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from converted_artist_data import convert


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
    appears_on = spotify.artist_albums(actual_uri, 'appears_on', limit=5)['items']

    # check if the newest album's uri is different as the newest in database
    # albums in lists are from the newest to the oldest
    if albums[0]['uri'] != artist['artist_albums'][0]:
        # check from the oldest to the newest response albums if album is in app database
        for album in albums[::-1]:
            if album['uri'] not in artist['artist_albums']:
                # get all album's artists
                artists = ", ".join(album_artist['name'] for album_artist in album['artists'])
                if len(album['artists']) > 1:
                    print("{0} have just released new album \"{1}\", which you can listen to on Spotify!\n\n{2}".
                          format(artists, album['name'], album['external_urls']['spotify']))
                else:
                    print("{0} has just released new album \"{1}\", which you can listen to on Spotify!\n\n{2}".
                          format(artists, album['name'], album['external_urls']['spotify']))

    # check if the newest song's uri is different as the newest in database
    # songs in lists are from the newest to the oldest
    if songs[0]['uri'] != artist['artist_songs'][0]:
        # check from the oldest ot the newest response songs if song is in app database
        for song in songs[::-1]:
            if song['uri'] not in artist['artist_songs']:
                # get all song's artists
                artists = ", ".join(song_artist['name'] for song_artist in song['artists'])
                if len(song['artists']) > 1:
                    print("{0} have just released new song \"{1}\", which you can listen to on Spotify!\n\n{2}".
                          format(artists, song['name'], song['external_urls']['spotify']))
                else:
                    print("{0} has just released new song \"{1}\", which you can listen to on Spotify!\n\n{2}".
                          format(artists, song['name'], song['external_urls']['spotify']))

    # check if the newest appear on uri is different as the newest in database
    # appears on in lists are from the newest to the oldest
    if appears_on[0]['uri'] != artist['artist_appears_on'][0]:
        # check from the oldest ot the newest response appears if appear is in app database
        for appear_on in appears_on[::-1]:
            if appear_on['uri'] not in artist['artist_appears_on']:
                # get all appear artists
                artists = ", ".join(appear_artist['name'] for appear_artist in appear_on['artists'])
                # if appear is on song
                if appear_on['album_type'] == 'single':
                    if len(appear_on['artists']) > 1:
                        print("{0} have just released new song \"{1}\" featuring {2}, which you can listen to on Spotify!\n\n{3}".
                              format(artists, appear_on['name'], artist["artist_name"], appear_on['external_urls']['spotify']))
                    else:
                        print("{0} has just released new song \"{1}\" featuring {2}, which you can listen to on Spotify!\n\n{3}".
                              format(artists, appear_on['name'], artist["artist_name"], appear_on['external_urls']['spotify']))
                # if appear is on album
                elif appear_on['album_type'] == 'album':
                    if len(appear_on['artists']) > 1:
                        print("{0} have just released new album \"{1}\" on which you can find song with {2}. "
                              "Listen to this album on Spotify!\n\n{3}".
                              format(artists, appear_on['name'], artist["artist_name"], appear_on['external_urls']['spotify']))
                    else:
                        print("{0} has just released new album \"{1}\" on which you can find song with {2}. "
                              "Listen to this album on Spotify!\n\n{3}".
                              format(artists, appear_on['name'], artist["artist_name"], appear_on['external_urls']['spotify']))
                # if appear is on compilation
                else:
                    print("{0} took part in compilation \"{1}\", which you can listen to on Spotify!\n\n{2}".
                          format(artist['artist_name'], appear_on['name'], appear_on['external_urls']['spotify']))

    print("{0}'s data refreshed!".format(artist['artist_name']))

    refreshed_artist_data = convert(actual_uri, artist['artist_name'], [albums, songs, appears_on])

    return refreshed_artist_data
