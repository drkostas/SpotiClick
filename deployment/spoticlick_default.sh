#!/bin/bash
cd ..
source venv/bin/activate
set -o allexport
source .env
set +o allexport
spoticlick_run -m skip_first_press -c confs/raspotify_conf.yml -l logs/raspotify.log &
tail -f logs/raspotify.log