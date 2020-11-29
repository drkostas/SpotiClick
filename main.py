import os
from time import sleep
import argparse
import logging
import traceback
import requests.exceptions

from spotipy.spotipy import Spotipy
from configuration.configuration import Configuration

logger = logging.getLogger('SpotiClick')

scope = 'user-read-playback-state'


def _setup_log(log_path: str = 'logs/output.log', debug: bool = False) -> None:
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
    parser = argparse.ArgumentParser(
        description='A software designed to click a button when music starts playing.',
        add_help=False)
    # Required Args
    required_arguments = parser.add_argument_group('Required Arguments')
    config_file_params = {
        'type': argparse.FileType('r'),
        'required': True,
        'help': "The configuration yml file"
    }
    required_arguments.add_argument('-m', '--run-mode', choices=['press_on_start', 'skip_first_press'],
                                    required=True,
                                    default='skip_first_press',
                                    help='Whether to press button when starting.')
    required_arguments.add_argument('-c', '--config-file', **config_file_params)
    required_arguments.add_argument('-l', '--log', help="Name of the output log file")
    # Optional args
    optional = parser.add_argument_group('Optional Arguments')
    optional.add_argument('-d', '--debug', action='store_true', help='Enables the debug log messages')
    optional.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()


def main():
    """
    :Example:
    python main.py -m skip_first_press
                   -c confs/default_conf.yml
                   -l logs/spoticlick.log
    """

    # Initializing
    args = _argparser()
    _setup_log(args.log, args.debug)
    logger.info("Starting in run mode: {0}".format(args.run_mode))
    # Load the configuration
    configuration = Configuration(config_src=args.config_file)
    # Get Switchbot config
    switch_conf = configuration.get_switchbots()[0]
    # Init Spotipy
    spot = Spotipy(config=configuration.get_spotifies()[0])
    ras_was_active = False
    skip = (args.run_mode == 'skip_first_press')
    while True:
        try:
            ras_active = spot.is_raspotify_active()
            if ras_active != ras_was_active:
                if skip:
                    skip = False
                else:
                    os.popen("python %s %s Press" % (switch_conf['src_path'], switch_conf['max_address']), 'w')\
                        .write('')
                    print("switchbot clicked!")
                    print("Raspotify active status changed to: " + str(ras_active))
                ras_was_active = ras_active
        except Spotipy.spotipy.client.SpotifyException as e:
            print("Token expired.\nSpotifyException: %s \nRefreshing.." % e)
            spot.refresh_token()
        except requests.exceptions.ReadTimeout as e:
            print("Read timeout: %s\nRetrying.." % e)
        sleep(2)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(str(e) + '\n' + str(traceback.format_exc()))
        raise e
