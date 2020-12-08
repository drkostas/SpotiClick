#!/bin/bash
cd "$(dirname "$0")"
cd ..
source venv/bin/activate
set -o allexport
source .env
set +o allexport
python spotify_connect.py -c confs/raspotify_connect_conf.yml -l logs/raspotify_connect.log