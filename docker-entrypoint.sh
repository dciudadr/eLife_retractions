#!/bin/bash
set -e

TARGET_USER=$NB_USER
TARGET_GID=$(stat -c "%g" .)
EXISTS=$(cat /etc/group | grep $TARGET_GID | wc -l)

# Create new group using target GID and add nobody user
if [ $EXISTS == "0" ]; then
  TEMPGROUP=tempgroup_$TARGET_GID
  groupadd -g $TARGET_GID $TEMPGROUP
  usermod -a -G $TEMPGROUP $TARGET_USER
else
  # GID exists, find group name and add
  GROUP=$(getent group $TARGET_GID | cut -d: -f1)
  usermod -a -G $GROUP $TARGET_USER
fi

# start.sh will change the user for us
exec "$@"
