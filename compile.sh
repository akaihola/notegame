#!/bin/bash

ROOT=`cd $(dirname $0) ; pwd`
cd ${ROOT}
while true; do
    transcrypt -b -m -n -e 6 main
    inotifywait \
        -q -r -e modify,move,create,delete \
        main.py || exit 1
done
