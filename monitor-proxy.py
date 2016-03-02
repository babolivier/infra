#!/bin/sh

docker ps | grep proxy > /dev/null

if [ $? -eq 1 ]; then
    docker rm proxy
    start-proxy
fi
