#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e
# Print commands and their arguments as they are executed.
set -x

# docker compose has to be started from the root of the vsc workspace so that the 
# relative paths in the docker-compose.yml files are the same for both workflows 
# (native docker-compose and vsc devcontainer extension)
docker compose --env-file ./.env -f .devcontainer/docker-compose.yml up -d
