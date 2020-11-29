import re
import spotipy.oauth2 as oauth
import spotipy_lib
import logging

logger = logging.getLogger('Spotipy')


class Spotipy:
    _auth_finder = re.compile("code=(.*?)$", re.MULTILINE)

    def __init__(self, config):
        """ Class that communicates with the Spotify API. """

        self._spoti_auth = oauth.SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=config['redirect_uri'],
            scope=config['scope'],
            cache_path="./tokens/cache-{}".format(config['username']))

        self._target_device = config['target_device']
        self._spoti_handler = spotipy_lib.Spotify(auth=self.get_token())

    def refresh_token(self):
        """ Refresh the spotify token. """

        cached_token = self._spoti_auth.get_cached_token()
        refreshed_token = cached_token['refresh_token']
        new_token = self._spoti_auth.refresh_access_token(refreshed_token)
        self._spoti_handler = spotipy_lib.Spotify(auth=new_token['access_token'])
        return new_token

    def get_token(self):
        """ Retrieves or generates spotify token. """

        token_info = self._spoti_auth.get_cached_token()
        if token_info:
            access_token = token_info['access_token']
            return access_token
        else:
            auth = self._spoti_auth.get_authorize_url()
            logger.info(auth)
            auth_url = input('Click the link above and copy and paste the url here: ')
            _re_auth = re.findall(self._auth_finder, auth_url)
            access_token = self._spoti_auth.get_access_token(_re_auth[0])
            return access_token

    def is_target_device_active(self):
        """ Checks if music is playing in target device. """

        devices = self._spoti_handler.devices()
        target_device_active = False
        for device in devices['devices']:
            if self._target_device in device['name'] and device['is_active'] is True:
                target_device_active = True
        return target_device_active
