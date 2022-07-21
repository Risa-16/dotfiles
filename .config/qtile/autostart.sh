#!/usr/bin/env bash
set -euo pipefail

redshift
playerctld daemon
blueman &
greenclip daemon &

#default_startup.sh &
