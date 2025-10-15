#!/bin/bash

SCRIPT_DIR=$(realpath "$(dirname "$0")")

source $SCRIPT_DIR/venv/bin/activate

python $SCRIPT_DIR/tools/build.py

[[ $1 == "full" ]] && $SCRIPT_DIR/tools/url-handler/toolkit default
