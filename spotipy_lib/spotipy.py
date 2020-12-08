import re
import spotipy.oauth2 as oauth
from  spotipy.client import SpotifyException
import spotipy
import logging

logger = logging.getLogger('Spotipy')


class Spotipy:
    _auth_finder = re.compile("code=(.*?)$", re.MULTILINE)

    def __init__(self, config, token_id='default'):
        """ Class that communicates with the Spotify API. """

        self._spoti_auth = oauth.SpotifyOAuth(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=config['redirect_uri'],
            scope=config['scope'],
            cache_path="./tokens/cache-{}-{}".format(config['username'], token_id))

        self._target_device = config['target_device']
        self._spoti_handler = spotipy.Spotify(auth=self.get_token())

    def refresh_token(self):
        """ Refresh the spotify token. """

        cached_token = self._spoti_auth.get_cached_token()
        refreshed_token = cached_token['refresh_token']
        new_token = self._spoti_auth.refresh_access_token(refreshed_token)
        self._spoti_handler = spotipy.Spotify(auth=new_token['access_token'])
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

    def get_playback_info(self):
        context = song = progress_ms = None
        current_playback = dict(self._spoti_handler.current_playback())
        if isinstance(current_playback, dict):
            if "context" in current_playback:
                if isinstance(current_playback["context"], dict):
                    if "uri" in current_playback["context"]:
                        context = current_playback["context"]["uri"]
            if "item" in current_playback:
                if isinstance(current_playback["item"], dict):
                    if "uri" in current_playback["item"]:
                        song = current_playback["item"]["uri"]
            if "progress_ms" in current_playback:
                progress_ms = current_playback["progress_ms"]
        return (context, song, progress_ms)

    def play_on_device(self, target_device_id, session_info):
        if session_info[0] is not None:
            self._spoti_handler.start_playback(device_id=target_device_id, context_uri=session_info[0],
                                               offset={"uri": session_info[1]}, position_ms=session_info[2])
        else:
            self._spoti_handler.start_playback(device_id=target_device_id, uris=[session_info[1]],
                                               position_ms=session_info[2])

