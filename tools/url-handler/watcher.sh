#!/bin/bash

# uses wtr.watcher to watch for changes in the src directory
# and run the toolkit script

wtr.watcher "$PWD/src/" | while read file; do
    "$PWD/toolkit" default
done