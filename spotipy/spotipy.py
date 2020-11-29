import re
import spotipy.oauth2 as oauth
import spotipy

class Spotipy:
    _auth_finder = re.compile("code=(.*?)$", re.MULTILINE)

    def __init__(self, config):
        self._spoti_auth = oauth.SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=config['redirect_uri'],
            scope=config['scope'],
            cache_path="./tokens/cache-{}".format(config['username']))

        self._spoti_handler = spotipy.Spotify(auth=self.get_token())

    def refresh_token(self):
        cached_token = self._spoti_auth.get_cached_token()
        refreshed_token = cached_token['refresh_token']
        new_token = self._spoti_auth.refresh_access_token(refreshed_token)
        print(new_token['access_token'])  # <--
        # also we need to specifically pass `auth=new_token['access_token']`
        self._spoti_handler = spotipy.Spotify(auth=new_token['access_token'])
        return new_token

    def get_token(self):
        token_info = self._spoti_auth.get_cached_token()
        if token_info:
            access_token = token_info['access_token']
            return access_token
        else:
            auth = self._spoti_auth.get_authorize_url()
            print(auth)
            auth_url = input('Click the link above and copy and paste the url here: ')
            _re_auth = re.findall(self._auth_finder, auth_url)
            access_token = self._spoti_auth.get_access_token(_re_auth[0])
            return access_token

    def is_raspotify_active(self):
        devices = self._spoti_handler.devices()
        ras_active = False
        for device in devices['devices']:
            if 'raspotify' in device['name'] and device['is_active'] is True:
                ras_active = True
        return ras_active
