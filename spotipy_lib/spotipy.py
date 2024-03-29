import re
import spotipy.oauth2 as oauth
from spotipy.client import SpotifyException
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
            if self._target_device in device['name'] and device['is_active'] and self.is_music_playing():
                target_device_active = True
        return target_device_active

    def is_music_playing(self):
        is_playing = False
        current_playback = self._spoti_handler.current_playback()
        if current_playback is not None:
            if isinstance(current_playback, dict):
                if "is_playing" in current_playback:
                    is_playing = current_playback["is_playing"]
        return is_playing

    def get_playback_info(self):
        context = song = progress_ms = None
        current_playback = self._spoti_handler.current_playback()
        if current_playback is not None:
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
        return context, song, progress_ms

    def play_on_device(self, target_device_id, session_info):
        found_track = True
        if session_info[0] is not None:
            self._spoti_handler.start_playback(device_id=target_device_id, context_uri=session_info[0],
                                               offset={"uri": session_info[1]}, position_ms=session_info[2])
        elif session_info[1] is not None:
            self._spoti_handler.start_playback(device_id=target_device_id, uris=[session_info[1]],
                                               position_ms=session_info[2])
        else:
            found_track = False
            self._spoti_handler.start_playback(device_id=target_device_id,
                                               context_uri='spotify:user:spotify:playlist:37i9dQZEVXcMGTqe35pFgb',
                                               position_ms=None)

        self._spoti_handler.shuffle(True, device_id=target_device_id)
        self._spoti_handler.repeat("context", device_id=target_device_id)

        if not found_track:
            self._spoti_handler.next_track(device_id=target_device_id)

    def get_current_volume(self):
        current_volume = None
        current_playback = self._spoti_handler.current_playback()
        if current_playback is not None:
            if isinstance(current_playback, dict):
                if "device" in current_playback:
                    if isinstance(current_playback["device"], dict):
                        if "volume_percent" in current_playback["device"]:
                            current_volume = current_playback["device"]["volume_percent"]
        return current_volume

    def volume_update(self, direction, current_volume, offset=5):
        if current_volume is None:
            new_volume = 50
        elif direction == 'increase':
            new_volume = int(current_volume) + offset
        elif direction == 'decrease':
            new_volume = int(current_volume) - offset
        else:
            logger.warning("Direction should be either increase or decrease. Skipping..")
        self._spoti_handler.volume(new_volume)
