#!/bin/bash
export $(dbus-launch)
export XDG_RUNTIME_DIR=/run/user/1000
export SHELL=/bin/bash
export HOME=/home/deck
export DISPLAY=$1
sudo -u deck -E /usr/lib/kdeconnectd --replace