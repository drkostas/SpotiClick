# shows tracks for the given artist

# usage: python tracks.py [artist name]

from spotipy_lib.oauth2 import SpotifyClientCredentials
import spotipy_lib
import sys

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy_lib.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
    results = sp.search(q=artist_name, limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])
