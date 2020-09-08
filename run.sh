#!/bin/bash

source ~/.anaconda3/etc/profile.d/conda.sh
conda activate desmonte_bot

if [ "$1" == "test" ]; then
    python -m unittest discover
else
    python -m bot_desmonte_neolib
fi