#!/bin/bash

# Build and Deploy Script for Personal Resume Website

set -e  # Exit on any error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
IMAGE_NAME="personal-resume"
CONTAINER_NAME="personal-resume-web"
TAG=${1:-latest}

echo -e "${BLUE}=== Personal Resume Website Deployment ===${NC}"
echo -e "${BLUE}Image: ${IMAGE_NAME}:${TAG}${NC}"
echo -e "${BLUE}Container: ${CONTAINER_NAME}${NC}"
echo ""

# Function to print step
print_step() {
    echo -e "${YELLOW}[STEP] $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Check if Docker is running
print_step "Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi
print_success "Docker is running"

# Stop and remove existing container
print_step "Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true
print_success "Existing container cleaned up"

# Build new image
print_step "Building Docker image..."
if docker build -t $IMAGE_NAME:$TAG .; then
    print_success "Image built successfully"
else
    print_error "Failed to build image"
    exit 1
fi

# Run container
print_step "Starting new container..."
if docker run -d \
    --name $CONTAINER_NAME \
    -p 8080:8080 \
    --restart unless-stopped \
    $IMAGE_NAME:$TAG; then
    print_success "Container started successfully"
else
    print_error "Failed to start container"
    exit 1
fi

# Wait for container to be ready
print_step "Waiting for application to start..."
sleep 10

# Health check
print_step "Performing health check..."
if curl -f http://localhost:8080/ > /dev/null 2>&1; then
    print_success "Health check passed"
else
    print_error "Health check failed"
    echo -e "${YELLOW}Container logs:${NC}"
    docker logs $CONTAINER_NAME
    exit 1
fi

# Display status
echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo -e "${GREEN}✓ Application is running at: http://localhost:8080${NC}"
echo -e "${GREEN}✓ Container name: $CONTAINER_NAME${NC}"
echo -e "${GREEN}✓ Image: $IMAGE_NAME:$TAG${NC}"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo -e "  View logs: ${YELLOW}docker logs -f $CONTAINER_NAME${NC}"
echo -e "  Stop: ${YELLOW}docker stop $CONTAINER_NAME${NC}"
echo -e "  Shell access: ${YELLOW}docker exec -it $CONTAINER_NAME /bin/bash${NC}"