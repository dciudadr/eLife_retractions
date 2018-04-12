#!/bin/bash
set -e

IMAGE_NAME=elifesciences/retractions

CONTAINER_PROJECT_HOME=/srv/elife_retractions
HOST_PROJECT_HOME=$(pwd)
HOST_PORT=8889

start() {
  docker run \
    -d -p $HOST_PORT:8888 \
    -v $HOST_PROJECT_HOME:$CONTAINER_PROJECT_HOME \
    $IMAGE_NAME \
    start-notebook.sh \
    --NotebookApp.token=''
  url="http://localhost:$HOST_PORT"
  echo "container should now be available via $url"
}

stop() {
  container_id=$(docker ps -q --filter "ancestor=$IMAGE_NAME")
  if [ -z $container_id ]; then
    echo 'no running container not found'
    exit 2
  fi
  docker rm $(docker stop $container_id)
}

build() {
  docker build -t $IMAGE_NAME .
}

case "$1" in 
    start)   start ;;
    stop)    stop ;;
    restart) stop; start ;;
    build) build ;;
    *) echo "usage: $0 start|stop|restart|build" >&2
       exit 1
       ;;
esac
