#!/bin/bash

set -e

ls $1 > /dev/null

wal -c
wal -n -i $1

echo "Wallpaper changed, reload qtile to apply."
