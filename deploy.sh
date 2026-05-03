#!/bin/bash

# Configuration
IMAGE_NAME="skin-disease-ai"
DOCKERHUB_USERNAME="your_dockerhub_username" # Update with actual username
TAG="latest"

echo "Starting deployment process..."

# 1. Build the Docker image
echo "Building Docker image..."
docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG} .

if [ $? -eq 0 ]; then
    echo "Docker build successful."
else
    echo "Docker build failed."
    exit 1
fi

# 2. Push to DockerHub
echo "Pushing image to DockerHub..."
docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}

if [ $? -eq 0 ]; then
    echo "Image pushed to DockerHub successfully."
else
    echo "Failed to push image to DockerHub. Are you logged in?"
    exit 1
fi

# 3. Push to GitHub
echo "Pushing to GitHub..."
git add .
git commit -m "Add Flask API, GenAI integration, and Dockerization"
git push origin main

if [ $? -eq 0 ]; then
    echo "Code pushed to GitHub successfully."
else
    echo "Failed to push code to GitHub."
    exit 1
fi

echo "Deployment complete!"
