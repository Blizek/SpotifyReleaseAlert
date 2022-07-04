"""
    File with function to convert data to form which is in file data.json
"""


def convert(uri, name, discography):
    """
        Function to convert data to ready to load to json file artist's data object
        :param uri: artist's Spotify URI
        :param name: artist's name
        :param discography: list in which are 3 lists (1) albums (2) songs (3) appears on
        :return new_artist_data: ready to load to json file artist's data object
    """

    # discography argument divides on list of the albums, songs and appears on
    albums = discography[0]
    songs = discography[1]
    appears_on = discography[2]

    # empty lists for artist's discography
    converted_albums = []
    converted_songs = []
    converted_appears_on = []

    # create list of artist's last 5 albums
    for album in albums:
        new_album_data = album['uri']

        converted_albums.append(new_album_data)

    # create list of the last 5 artist's own songs
    for song in songs:
        new_song_data = song['uri']

        converted_songs.append(new_song_data)

    # create list of the artist's last 5 songs where he/she appeared on
    for appear_on in appears_on:
        new_appear_on_data = appear_on['uri']

        converted_appears_on.append(new_appear_on_data)

    # create new json object with artist's data
    new_artist_data = {
        'artist_uri': uri,
        'artist_name': name,
        'artist_albums': converted_albums,
        'artist_songs': converted_songs,
        'artist_appears_on': converted_appears_on
    }

    return new_artist_data
