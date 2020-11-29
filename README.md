# SpotiClick
[![GitHub license](https://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/drkostas/SpotiCLick/master/LICENSE)

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
    + [Prerequisites](#prerequisites)

## About <a name = "about"></a>
An app that clicks a physical button whenever Spotify starts playing on a target device.

Real case: I have Raspberry Pi connected to a Stereo Receiver and a Spotify Client installed. The Stereo Receiver has a
 physical button that needs to be pressed in order to power on. I want this button to be pressed whenever music starts
 or stops playing on this device.

The app consists of 3 parts:
- A spotify client installed on a raspberry pi 3 (or any device with spotify) capable of playing music to a stereo speaker device (which needs to be switched on/off by pressing a button)
- A [switchbot device](https://www.switch-bot.com/products/switchbot-bot) that can be triggered (via bluetooth) to click a button
- The spotify API that is capable of checking on which device the music is playing for a user

If the project is setup correctly the flow is the following:
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
    
