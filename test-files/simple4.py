import spotipy_lib
from pprint import pprint


def main():
    spotify = spotipy_lib.Spotify(auth_manager=spotipy_lib.SpotifyOAuth())
    me = spotify.me()
    pprint(me)


if __name__ == "__main__":
    main()
