#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Print commands and their arguments as they are executed.
set -x

export $(grep -v '^#' .devcontainer/.env | xargs)

docker stop ${COMPOSE_PROJECT_NAME}_container
docker rm ${COMPOSE_PROJECT_NAME}_container
