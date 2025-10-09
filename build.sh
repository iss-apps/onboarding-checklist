#!/bin/bash

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")

source $SCRIPT_DIR/venv/bin/activate

python $SCRIPT_DIR/tools/build.py