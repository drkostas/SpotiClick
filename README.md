# SpotiClick
[![GitHub license](https://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/drkostas/SpotiCLick/master/LICENSE)

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
    + [Prerequisites](#prerequisites)
    + [Environment Variables](#env_variables)
+ [Installing, Testing, Building](#installing)
    + [Available Make Commands](#check_make_commamnds)
    + [Clean Previous Builds](#clean_previous)
    + [Venv and Requirements](#venv_requirements)
    + [Build Locally](#build_locally)
+ [Running locally](#run_locally)
	+ [Configuration](#configuration)
	+ [Execution Options](#execution_options)	
+ [Deployment](#deployment)
+ [Todo](#todo)
+ [Built With](#built_with)
+ [License](#license)
+ [Acknowledgments](#acknowledgments)

## About <a name = "about"></a>
<b>An app that clicks a physical button whenever Spotify starts playing on a target device.</b>

<b>Real case</b>: <i>I have Raspberry Pi connected to a Stereo Receiver and a Spotify Client installed. The Stereo Receiver has a
 physical button that needs to be pressed in order to power on. I want this button to be pressed whenever music starts
 or stops playing on this device.</i>

<b>The app consists of 3 parts</b>:
- A spotify client installed on a raspberry pi 3 (or any device with spotify) capable of playing music to a stereo speaker device (which needs to be switched on/off by pressing a button)
- A [switchbot device](https://www.switch-bot.com/products/switchbot-bot) that can be triggered (via bluetooth) to click a button
- The spotify API that is capable of checking on which device the music is playing for a user

<b>If the project is setup correctly the flow is the following</b>:
1. The user opens Spotify on any device and from the spotify connect menu, he selects the target device (for me is a raspberry client - raspotify)
1. The main.py which is checking (through Spotify API) every few seconds which device spotify is playing music on, is notified that music is now playing on the target device.
1. It calls the switchbot.py with the correct arguments which triggers the Switchbot to press the power-on button of the stereo device.
1. Whenever music stops playing on the target device, the same flow will cause the button to be pressed again and the stereo to get switched off.


## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development 
and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites <a name = "prerequisites"></a>
1. First of all you should have a [Premium Spotify](https://www.spotify.com/us/premium/) account.
1. You need to have a machine (tested on Ubuntu 18.04) with:
    - Both Python 2.7 and Python> 3.6 and any Bash based shell (e.g. zsh) installed
    
        ```bash
        $ sudo apt-get install -y python2-dev python3-dev 
      
        $ python3 -V
        Python 3.6.9
        
        python2 -V
        Python 2.7.17
        
        $ echo $SHELL
        /usr/bin/zsh
        ```
    - Bluetooth enabled and the following libraries installed:
        ```bash
        sudo apt-get install -y python-pexpect libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
        ```

1. You will also need to setup Spotify API 
([Reference 1](https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b), 
[Reference 2](https://developer.spotify.com/documentation/web-api/))

1. You should own a [Switchbot clicker](https://www.switch-bot.com/products/switchbot-bot).

1. (Optional) If you want to use a [Raspberry Pi](https://www.raspberrypi.org/products/) as your target Spotify client, you need to do the following:
    - Ensure your Raspberry Pi has bluetooth
    - Install the [raspotify client](https://github.com/dtcooper/raspotify) on your Raspberry (also connect to your Spotify account)
    - Connect your Raspberry to your speakers
    

### Set the required environment variables <a name = "env_variables"></a>

Before running the [main.py](main.py) you will need to set the following 
environmental variables in an .env file that you should load before running it:

```.env
SPOTIFY_USERNAME=<Value>
SPOTIFY_CLIENT_ID=<Value>
SPOTIFY_SECRET=<Value>
SWITCHBOT_MAC=<Value>
```

## Installing, Building <a name = "installing"></a>

All the installation steps are being handled by the [Makefile](Makefile).

<i>If you don't want to go through the setup steps and finish the installation at once,
execute the following command:</i>

```bash
$ make install
```

<i>If you executed the previous command, you can skip through to the [Running locally](#run_locally) section.</i>

### Check the available make commands <a name = "check_make_commamnds"></a>

```bash
$ make help

-----------------------------------------------------------------------------------------------------------
                                              DISPLAYING HELP                                              
-----------------------------------------------------------------------------------------------------------
make delete_venv
       Delete the current venv
make create_venv
       Create a new venv for the specified python version
make requirements
       Upgrade pip and install the requirements
make setup
       Call setup.py install
make clean_pyc
       Clean all the pyc files
make clean_build
       Clean all the build folders
make clean
       Call delete_venv clean_pyc clean_build
make install
       Call clean create_venv requirements setup
make help
       Display this message
-----------------------------------------------------------------------------------------------------------
```

### Clean any previous builds <a name = "clean_previous"></a>

```bash
$ make clean
make delete_venv
make[1]: Entering directory '/home/drkostas/Projects/SpotiClick'
Deleting venv..
rm -rf venv
make[1]: Leaving directory '/home/drkostas/Projects/SpotiClick'
make clean_pyc
make[1]: Entering directory '/home/drkostas/Projects/SpotiClick'
Cleaning pyc files..
find . -name '*.pyc' -delete
find . -name '*.pyo' -delete
find . -name '*~' -delete
make[1]: Leaving directory '/home/drkostas/Projects/SpotiClick'
make clean_build
make[1]: Entering directory '/home/drkostas/Projects/SpotiClick'
Cleaning build directories..
rm --force --recursive build/
rm --force --recursive dist/
rm --force --recursive *.egg-info
make[1]: Leaving directory '/home/drkostas/Projects/SpotiClick'

```

### Create a new venv and install the requirements <a name = "venv_requirements"></a>

```bash
$ make create_venv
Creating venv..
python3.6 -m venv ./venv

$ make requirements
Upgrading pip..
venv/bin/pip install --upgrade pip wheel setuptools
Collecting pip
.................
```

### Build the project locally <a name = "build_locally"></a>

To build the project locally using the setup.py command, execute the following command:

```bash
$ make setup
venv/bin/python setup.py install
running install
.................
```

## Running the code locally <a name = "run_locally"></a>

In order to run the code now, you will only need to change the yml file if you need to 
and run either the main or the created console script.

### Modifying the Configuration <a name = "configuration"></a>

There is an already configured yml file under [confs/template_conf.yml](confs/raspotify_conf.yml) with the following structure:

```yaml
spotify:
  - config:  # Spotify API credentials
      username: !ENV ${SPOTIFY_USERNAME}
      client_id: !ENV ${SPOTIFY_CLIENT_ID}
      client_secret: !ENV ${SPOTIFY_SECRET}
      scope: user-read-playback-state  # leave it as is
      redirect_uri: 'http://localhost:8081'  # leave it as is
      target_device: raspotify  # name of target device
    type: spotipy_lib  # leave it as is
switchbot:
  - config:
      src_path: ./switchbot/switchbot.py  # leave it as is
      mac_address: !ENV ${SWITCHBOT_MAC} # MAC address of switchbot (you can view it from the android app)
    type: spotipy_folder  # leave it as is
```

The `!ENV` flag indicates that a environmental value follows. 
You can change the values/environmental var names as you wish.
If a yaml variable name is changed/added/deleted, the corresponding changes should be reflected 
on the [Configuration class](configuration/configuration.py) and the [yml_schema.json](configuration/yml_schema.json) too.

### Execution Options <a name = "execution_options"></a>

First, make sure you are in the created virtual environment:

```bash
$ source venv/bin/activate
(venv) 
~/drkostas/Projects/SpotiClick  dev 

$ which python
~/drkostas/Projects/SpotiClick/venv/bin/python
(venv) 
```

Now, in order to run the code you can either call the `main.py` directly, or the `SpotiClick` console script.

```bash
$ python main.py --help
usage: main.py -m {press_on_start,skip_first_press} -c CONFIG_FILE [-l LOG]
               [-d] [-h]

A software designed to click a button when music starts playing.

Required Arguments:
  -m {press_on_start,skip_first_press}, --run-mode {press_on_start,skip_first_press}
                        Whether to press button when starting.
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        The configuration yml file
  -l LOG, --log LOG     Name of the output log file

Optional Arguments:
  -d, --debug           Enables the debug log messages
  -h, --help            Show this help message and exit
(venv) 


# Or

$ SpotiClick --help
usage: main.py -m {press_on_start,skip_first_press} -c CONFIG_FILE [-l LOG]
               [-d] [-h]

A software designed to click a button when music starts playing.

Required Arguments:
  -m {press_on_start,skip_first_press}, --run-mode {press_on_start,skip_first_press}
                        Whether to press button when starting.
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        The configuration yml file
  -l LOG, --log LOG     Name of the output log file

Optional Arguments:
  -d, --debug           Enables the debug log messages
  -h, --help            Show this help message and exit
(venv) 

```

## Deployment <a name = "deployment"></a>

The deployment is being done to a device with bluetooth and close proximity to the Switchbot.

Don't forget to set the [above-mentioned environmental variables](#env_variables).

## TODO <a name = "todo"></a>

Read the [TODO](TODO.md) to see the current task list.

## Built With <a name = "built_with"></a>

* [Spotify API](https://developer.spotify.com/documentation/web-api/) - Used in the spotipy_lib
* [Spotipy](https://github.com/plamere/spotipy) - Was wrapped by spotipy_lib
* [Switchbot](https://www.switch-bot.com/products/switchbot-bot) - Used to click the physical button
* [Raspberry Pi](https://www.raspberrypi.org/products/) - Used to play music and host this app
* [Python Host](https://github.com/OpenWonderLabs/python-host) - Used to trigger the Switchbot device


## License <a name = "license"></a>

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments <a name = "acknowledgments"></a>

* Thanks to PurpleBooth for the [README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)

