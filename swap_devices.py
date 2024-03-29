import os
from time import sleep
import argparse
import logging
import traceback
import requests.exceptions

from spotipy_lib.spotipy import Spotipy
from spotipy_lib.spotipy import SpotifyException
from configuration.configuration import Configuration

logger = logging.getLogger('Spotify Connect')


def _setup_log(log_path: str = 'logs/output.log', debug: bool = False) -> None:
    """ Sets up logger. """

    log_path = log_path.split(os.sep)
    if len(log_path) > 1:
        try:
            os.makedirs((os.sep.join(log_path[:-1])))
        except FileExistsError:
            pass
    log_filename = os.sep.join(log_path)
    # noinspection PyArgumentList
    logging.basicConfig(level=logging.INFO if debug is not True else logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_filename),
                            # logging.handlers.TimedRotatingFileHandler(log_filename, when='midnight', interval=1),
                            logging.StreamHandler()
                        ]
                        )


def _argparser() -> argparse.Namespace:
    """ Parses and returns the command line arguments. """

    parser = argparse.ArgumentParser(
        description='Script to trigger Spotify Connect to play on specific device.',
        add_help=False)
    # Required Args
    required_arguments = parser.add_argument_group('Required Arguments')
    config_file_params = {
        'type': argparse.FileType('r'),
        'required': True,
        'help': "The configuration yml file"
    }

    required_arguments.add_argument('-c', '--config-file', **config_file_params)
    required_arguments.add_argument('-l', '--log', help="Name of the output log file")
    # Optional args
    optional = parser.add_argument_group('Optional Arguments')
    optional.add_argument('-d', '--debug', action='store_true', help='Enables the debug log messages')
    optional.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


def main():
    """
    Handles the core flow of SpotiClick.

    :Example:
    python main.py -c confs/raspotify_conf.yml
                   -l logs/spoticlick.log
    """

    # Initializing
    args = _argparser()
    _setup_log(args.log, args.debug)
    # Load the configuration
    configuration = Configuration(config_src=args.config_file)
    # Init Spotipy
    spoti_read_config = configuration.get_spotifies()[0]
    print(spoti_read_config)
    spoti_modify_config = configuration.get_spotifies()[1]
    target_device_id_1 = spoti_read_config["target_device_id"]
    target_device_id_2 = spoti_modify_config["target_device_id"]
    spot_read = Spotipy(config=spoti_read_config, token_id='read')
    # Check active
    device_1_active = spot_read.is_target_device_active()
    if not device_1_active:
        target_device_id = target_device_id_1
    else:
        target_device_id = target_device_id_2

    spot_modify = Spotipy(config=spoti_modify_config, token_id='modify')
    # Change device
    logger.info("Transferring music to device id: %s" % target_device_id)
    spot_modify.play_on_device(target_device_id=target_device_id, session_info=spot_read.get_playback_info())
    logger.info("Music Transferred!")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
