#!/bin/bash

if [ "$1" == "test" ]; then
    python -m unittest discover
else
    python -m bot_desmonte_neolib
fi