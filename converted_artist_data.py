"""
    File with function to convert data to form which is in file data.json
"""


def convert(uri, name, discography):
    """
        Function to convert data to ready to load to json file artist's data object
        :param uri: artist's Spotify URI
        :param name: artist's name
        :param discography: list in which are 3 lists (1) albums (2) songs
        :return new_artist_data: ready to load to json file artist's data object
    """

    # discography argument divides on list of the albums, songs and appears on
    albums = discography[0]
    songs = discography[1]

    # empty lists for artist's discography
    converted_albums = []
    converted_songs = []

    # create list of artist's last 5 albums
    for album in albums:
        new_album_data = album['uri']

        converted_albums.append(new_album_data)

    # create list of the last 5 artist's own songs
    for song in songs:
        new_song_data = song['uri']

        converted_songs.append(new_song_data)

    # create new json object with artist's data
    new_artist_data = {
        'artist_uri': uri,
        'artist_name': name,
        'artist_albums': converted_albums,
        'artist_songs': converted_songs,
    }

    return new_artist_data
