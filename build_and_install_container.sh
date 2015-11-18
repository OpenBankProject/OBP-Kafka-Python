#!/bin/bash

CONTAINER_NAME="OBP-SOFI-EXPLORER-KAFKA"

# Lowercase CONTAINER_NAME
REPOSITORY_NAME=$(echo ${CONTAINER_NAME} | tr '[:upper:]' '[:lower:]')

# Find the old image id using docker name
#
OLD_IMAGE_ID=$(docker images | grep "${CONTAINER_NAME}" | awk '{print $3}' | uniq)
echo -n '.'

#export DOCKER_HOST_NAME=$(ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | cut -d' ' -f1)
export DOCKER_HOST_NAME=$(hostname --ip-address)

# Stop old container 
#
docker stop ${CONTAINER_NAME} &> /dev/null
echo -n '.'

# Remove old container 
#
docker rm ${CONTAINER_NAME} &> /dev/null
echo -n '.'

# Remove old image
#
docker rmi -f ${OLD_IMAGE_ID} &> /dev/null
echo -n '.'

# Build Docker image
#
echo 'please wait...'
sed -i 's/ENV DOCKER_HOST_NAME=.*$/ENV DOCKER_HOST_NAME="'${DOCKER_HOST_NAME}'"/' Dockerfile
OUTPUT=$(docker build -t ${REPOSITORY_NAME} .)
IMAGE_ID=$(echo $OUTPUT | awk '{print $NF}')
echo "IMAGE_ID     "${IMAGE_ID}

# Start container
#
CONTAINER_ID=$(docker run --restart=always --detach=true --name=${CONTAINER_NAME} ${IMAGE_ID} | cut -b1-12)
echo "CONTAINER_ID "${CONTAINER_ID}

# Rename container for easier removal
#
#docker rename ${CONTAINER_ID} ${CONTAINER_NAME}

echo
echo 'Done ;-)'
echo
