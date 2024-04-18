#!/bin/bash

cd /root/book-reservation-backend

# Set script to exit on any errors.
set -e

# Optional: Add a logging statement to track script execution.
echo "Starting deployment script."

# Stop the existing docker containers
echo "Stopping existing Docker containers..."
docker-compose -f docker-compose.prod.yml down || { echo "Failed to stop containers."; exit 1; }

# Pull the latest changes from the repository
echo "Pulling latest changes from Git repository..."
git pull origin develop || { echo "Git pull failed."; exit 1; }

# Build and run the docker containers
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml up -d --build || { echo "Docker Compose up failed."; exit 1; }

echo "Deployment completed successfully."