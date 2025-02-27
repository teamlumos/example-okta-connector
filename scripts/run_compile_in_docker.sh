#!/bin/bash

# compile for linux/amd64
docker build . --progress=plain --platform linux/amd64 -t compile-custom-connector

docker run --name compile-custom-connector compile-custom-connector

docker cp compile-custom-connector:/build/build/compiled/ ./compiled

docker rm compile-custom-connector  

