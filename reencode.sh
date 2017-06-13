#!/bin/bash
vspipe --y4m svp.py -a "I=${1}" - | ffmpeg -i "${1}" -i pipe: -map 0:1 -map 1:0 "${2}"
