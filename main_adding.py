"""
    Main file of the algorithm for adding artists to the database
"""

import add_artist

if __name__ == "__main__":
    uri = input("Pass artist's Spotify URI: ")
    add_artist.add(uri)
