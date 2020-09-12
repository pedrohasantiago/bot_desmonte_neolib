#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh
conda activate desmonte_bot

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$THIS_DIR" # Else, the bot_demsonte_neolib module won't be found

if [ "$1" == "test" ]; then
    python3 -m unittest discover
else
    python3 -m bot_desmonte_neolib &> logs/log.txt  
fi
