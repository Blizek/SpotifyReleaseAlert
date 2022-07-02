import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

uri = 'spotify:artist:0MIG6gMcQTSvFbKvUwK0id'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

albums = spotify.artist_albums(uri, 'album', limit=50)['items']
songs = spotify.artist_albums(uri, 'single', limit=50)['items']
appears_on = spotify.artist_albums(uri, 'appears_on', limit=50)['items']

uri_bialas = "spotify:artist:7CJgLPEqiIRuneZSolpawQ"
album = spotify.artist_albums(uri_bialas, 'album', limit=50)['items']
song = spotify.artist_albums(uri_bialas, 'single', limit=50)['items']
appear_on = spotify.artist_albums(uri_bialas, 'appears_on', limit=50)['items']

if album[0]['uri'] != albums[0]['uri']:
    for plyta in album[::-1]:
        if plyta not in albums:
            artysci = ", ".join(artysta['name'] for artysta in plyta['artists'])
            if len(plyta['artists']) > 1:
                print("{0} wydali płytę {1}, który już możesz odsłuchać na Spotify!".format(artysci, plyta['name']))
            else:
                print("{0} wydał(a) płytę {1}, który już możesz odsłuchać na Spotify!".format(artysci, plyta['name']))

print()

if song[0]['uri'] != songs[0]['uri']:
    for piosenka in song[::-1]:
        if piosenka not in songs:
            artysci = ", ".join(artysta['name'] for artysta in piosenka['artists'])
            if len(piosenka['artists']) > 1:
                print("{0} wydali numer {1}, który już możesz odsłuchać na Spotify!".format(artysci, piosenka['name']))
            else:
                print("{0} wydał(a) numer {1}, który już możesz odsłuchać na Spotify!".format(artysci, piosenka['name']))

print()

if appear_on[0]['uri'] != appears_on[0]['uri']:
    for wystep in appear_on[::-1]:
        if wystep not in appears_on:
            artysci = ", ".join(artysta['name'] for artysta in wystep['artists'])
            if wystep['album_type'] == 'single':
                if len(wystep['artists']) > 1:
                    print("{0} wydali numer {1} z gościnnym udziałem artysty Białas, który już możesz odsłuchać na Spotify!".format(artysci, wystep['name']))
                else:
                    print("{0} wydał(a) numer {1} z gościnnym udziałem artysty Białas, który już możesz odsłuchać na Spotify!".format(artysci, wystep['name']))
            elif wystep['album_type'] == 'album':
                if len(wystep['artists']) > 1:
                    print("{0} wydali płytę {1} z gościnnym udziałem artysty Białas, który już możesz odsłuchać na Spotify!".format(artysci, wystep['name']))
                else:
                    print("{0} wydał(a) płytę {1} z gościnnym udziałem artysty Białas, który już możesz odsłuchać na Spotify!".format(artysci, wystep['name']))
            else:
                print("Białas wziął udział w kompilacji {}, którą możesz odsłuchać na Spotify!".format(wystep['name']))