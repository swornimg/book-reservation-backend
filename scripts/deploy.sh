#!/bin/bash
# Stop the existing docker containers
docker-compose -f docker-compose.prod.yml down
# Pull the latest changes from the repository
git pull origin develop
# Build and run the docker containers
docker-compose -f docker-compose.prod.yml up -d --build

