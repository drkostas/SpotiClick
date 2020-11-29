# shows tracks for the given artist

# usage: python tracks.py [artist name]

from spotipy_lib.oauth2 import SpotifyClientCredentials
import spotipy_lib

username = ""
scope = "user-read-currently-playing"

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy_lib.Spotify(client_credentials_manager=client_credentials_manager)

print(sp.current_user_playing_track())
