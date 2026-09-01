#!/bin/bash

apt-get update -y
apt-get install -y docker.io

systemctl enable docker
systemctl start docker

docker pull yahiaouiraouf/northstar-app:latest

docker run -d \
  --name northstar-app \
  -p 80:5000 \
  yahiaouiraouf/northstar-app:latest