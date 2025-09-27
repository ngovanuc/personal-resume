# Makefile for Personal Resume Website Docker Operations

# Variables
IMAGE_NAME = personal-resume
CONTAINER_NAME = personal-resume-web
TAG = latest
PORT = 8080

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# Help target
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Personal Resume Website - Docker Commands$(NC)"
	@echo "=========================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development commands
.PHONY: build
build: ## Build the Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(IMAGE_NAME):$(TAG) .
	@echo "$(GREEN)Build completed!$(NC)"

.PHONY: run
run: ## Run the container
	@echo "$(GREEN)Starting container...$(NC)"
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8080 $(IMAGE_NAME):$(TAG)
	@echo "$(GREEN)Container started! Access: http://localhost:$(PORT)$(NC)"

.PHONY: stop
stop: ## Stop the container
	@echo "$(YELLOW)Stopping container...$(NC)"
	docker stop $(CONTAINER_NAME) || true
	@echo "$(GREEN)Container stopped!$(NC)"

.PHONY: remove
remove: stop ## Remove the container
	@echo "$(YELLOW)Removing container...$(NC)"
	docker rm $(CONTAINER_NAME) || true
	@echo "$(GREEN)Container removed!$(NC)"

.PHONY: restart
restart: remove run ## Restart the container

# Docker Compose commands
.PHONY: up
up: ## Start services with docker-compose
	@echo "$(GREEN)Starting services with docker-compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Services started!$(NC)"

.PHONY: down
down: ## Stop and remove docker-compose services
	@echo "$(YELLOW)Stopping docker-compose services...$(NC)"
	docker-compose down
	@echo "$(GREEN)Services stopped!$(NC)"

.PHONY: up-prod
up-prod: ## Start production services
	@echo "$(GREEN)Starting production services...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)Production services started!$(NC)"

.PHONY: down-prod
down-prod: ## Stop production services
	@echo "$(YELLOW)Stopping production services...$(NC)"
	docker-compose -f docker-compose.prod.yml down
	@echo "$(GREEN)Production services stopped!$(NC)"

# Utility commands
.PHONY: logs
logs: ## Show container logs
	docker logs -f $(CONTAINER_NAME)

.PHONY: logs-compose
logs-compose: ## Show docker-compose logs
	docker-compose logs -f

.PHONY: shell
shell: ## Enter container shell
	docker exec -it $(CONTAINER_NAME) /bin/bash

.PHONY: clean
clean: ## Clean up all containers and images
	@echo "$(RED)Cleaning up...$(NC)"
	docker-compose down -v --remove-orphans || true
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME):$(TAG) || true
	docker system prune -f
	@echo "$(GREEN)Cleanup completed!$(NC)"

.PHONY: status
status: ## Show status of containers
	@echo "$(BLUE)Container Status:$(NC)"
	@docker ps -a --filter name=$(CONTAINER_NAME)
	@echo ""
	@echo "$(BLUE)Images:$(NC)"
	@docker images | grep $(IMAGE_NAME) || echo "No images found"

.PHONY: health
health: ## Check container health
	@echo "$(BLUE)Health Check:$(NC)"
	@curl -f http://localhost:$(PORT)/ && echo "$(GREEN)✓ Website is accessible$(NC)" || echo "$(RED)✗ Website is not accessible$(NC)"

# Build and test
.PHONY: build-test
build-test: build run health ## Build, run and test the application
	@echo "$(GREEN)Build and test completed!$(NC)"

# Production deployment
.PHONY: deploy
deploy: ## Deploy to production
	@echo "$(GREEN)Deploying to production...$(NC)"
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d
	@echo "$(GREEN)Production deployment completed!$(NC)"

# Development workflow
.PHONY: dev
dev: ## Start development environment
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose up --build
	@echo "$(GREEN)Development environment started!$(NC)"

.PHONY: tunnel
tunnel: ## Start LocalTunnel to expose website publicly
	@echo "$(GREEN)Starting LocalTunnel...$(NC)"
	@echo "$(BLUE)Make sure Docker container is running first!$(NC)"
	@docker ps | grep my-resume || (echo "$(RED)Container not running. Start with: make run$(NC)" && exit 1)
	@echo "$(YELLOW)Your website will be public at: https://random.loca.lt$(NC)"
	lt --port $(PORT)

.PHONY: tunnel-custom
tunnel-custom: ## Start LocalTunnel with custom subdomain
	@echo "$(GREEN)Starting LocalTunnel with custom subdomain...$(NC)"
	@docker ps | grep my-resume || (echo "$(RED)Container not running. Start with: make run$(NC)" && exit 1)
	@echo "$(YELLOW)Your website will be public at: https://ngovanuc-resume.loca.lt$(NC)"
	lt --port $(PORT) --subdomain ngovanuc-resume