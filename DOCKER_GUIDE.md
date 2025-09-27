# 🐳 Docker Guide for Personal Resume Website

## Mục Lục
1. [Giới Thiệu về Docker](#giới-thiệu-về-docker)
2. [Cài Đặt Docker](#cài-đặt-docker)
3. [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
4. [Các Lệnh Docker Cơ Bản](#các-lệnh-docker-cơ-bản)
5. [Docker Compose](#docker-compose)
6. [Production Deployment](#production-deployment)
7. [Monitoring và Troubleshooting](#monitoring-và-troubleshooting)
8. [Best Practices](#best-practices)
9. [Câu Hỏi Phỏng Vấn về Docker](#câu-hỏi-phỏng-vấn-về-docker)

---

## Giới Thiệu về Docker

### Docker là gì?
Docker là một platform container hóa cho phép bạn đóng gói ứng dụng và dependencies vào một container có thể chạy trên bất kỳ môi trường nào.

### Lợi ích của Docker:
- ✅ **Consistency**: "Works on my machine" → "Works everywhere"
- ✅ **Isolation**: Ứng dụng chạy độc lập không ảnh hưởng hệ thống
- ✅ **Portability**: Chạy được trên mọi platform có Docker
- ✅ **Scalability**: Dễ dàng scale up/down
- ✅ **Version Control**: Image versioning như Git

### Các khái niệm cơ bản:
- **Image**: Template chứa OS, runtime, code
- **Container**: Instance đang chạy của image
- **Dockerfile**: Script để build image
- **Registry**: Nơi lưu trữ images (Docker Hub, GitHub Container Registry)

---

## Cài Đặt Docker

### Windows:
1. Download Docker Desktop từ https://docker.com
2. Cài đặt và restart máy
3. Kiểm tra: `docker --version`

### Linux (Ubuntu):
```bash
# Update system
sudo apt update

# Install dependencies
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

---

## Cấu Trúc Dự Án

```
personal-resume/
├── Dockerfile                    # Định nghĩa cách build image
├── .dockerignore                 # Files/folders bị ignore
├── docker-compose.yml            # Multi-container setup (dev)
├── docker-compose.prod.yml       # Production configuration
├── Makefile                      # Automation commands
├── requirements.txt              # Python dependencies
├── nginx/
│   └── nginx.conf               # Nginx configuration
├── scripts/
│   ├── deploy.sh               # Linux deployment script
│   └── deploy.bat              # Windows deployment script
└── .github/workflows/
    └── docker-deploy.yml       # CI/CD pipeline
```

---

## Các Lệnh Docker Cơ Bản

### 1. Build Image
```bash
# Build image với tag
docker build -t personal-resume:latest .

# Build với specific tag
docker build -t personal-resume:v1.0.0 .

# Build với build args
docker build --build-arg ENV=production -t personal-resume:prod .
```

### 2. Run Container
```bash
# Chạy container cơ bản
docker run -d --name my-resume -p 8080:8080 personal-resume:latest

# Chạy với environment variables
docker run -d --name my-resume -p 8080:8080 -e ENV=production personal-resume:latest

# Chạy với volume mount
docker run -d --name my-resume -p 8080:8080 -v $(pwd)/logs:/app/logs personal-resume:latest

# Chạy interactive mode để debug
docker run -it --name my-resume personal-resume:latest /bin/bash
```

### 3. Management Commands
```bash
# Xem containers đang chạy
docker ps

# Xem tất cả containers
docker ps -a

# Xem logs
docker logs my-resume
docker logs -f my-resume  # Follow logs

# Stop container
docker stop my-resume

# Start lại container
docker start my-resume

# Restart container
docker restart my-resume

# Remove container
docker rm my-resume

# Remove image
docker rmi personal-resume:latest
```

### 4. Debug Commands
```bash
# Vào trong container
docker exec -it my-resume /bin/bash

# Copy file từ container
docker cp my-resume:/app/logs/app.log ./

# Xem thông tin container
docker inspect my-resume

# Xem resource usage
docker stats my-resume
```

---

## Docker Compose

### Development Environment
```bash
# Start all services
docker-compose up -d

# Start và rebuild
docker-compose up --build

# Xem logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop và remove volumes
docker-compose down -v
```

### Production Environment
```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Scale web service
docker-compose -f docker-compose.prod.yml up -d --scale web=3

# Update service
docker-compose -f docker-compose.prod.yml up -d --no-deps web
```

---

## Production Deployment

### 1. Sử dụng Makefile
```bash
# Build và test
make build-test

# Deploy production
make deploy

# Xem status
make status

# Clean up
make clean
```

### 2. Sử dụng Scripts

**Linux/Mac:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**Windows:**
```cmd
scripts\deploy.bat
```

### 3. Manual Deployment
```bash
# 1. Build production image
docker build -t personal-resume:prod .

# 2. Stop old container
docker stop personal-resume-web || true
docker rm personal-resume-web || true

# 3. Run new container
docker run -d \
  --name personal-resume-web \
  -p 8080:8080 \
  --restart unless-stopped \
  -e ENV=production \
  personal-resume:prod

# 4. Health check
curl -f http://localhost:8080/
```

---

## Monitoring và Troubleshooting

### 1. Health Checks
```bash
# Container health status
docker ps --filter name=my-resume

# Custom health check
curl -f http://localhost:8080/ || echo "Service down"

# Container stats
docker stats my-resume
```

### 2. Logging
```bash
# View logs
docker logs my-resume

# Follow logs
docker logs -f my-resume

# Last 100 lines
docker logs --tail 100 my-resume

# Logs from specific time
docker logs --since "2025-01-01" my-resume
```

### 3. Common Issues & Solutions

**Issue: Container không start**
```bash
# Check logs
docker logs my-resume

# Check if port is already in use
netstat -tulpn | grep 8080

# Check container resources
docker inspect my-resume
```

**Issue: Application không accessible**
```bash
# Check container is running
docker ps | grep my-resume

# Check port mapping
docker port my-resume

# Test from inside container
docker exec -it my-resume curl http://localhost:8080
```

**Issue: Out of disk space**
```bash
# Clean up unused containers
docker container prune

# Clean up unused images
docker image prune

# Clean up everything
docker system prune -a
```

---

## Best Practices

### 1. Dockerfile Best Practices
```dockerfile
# ✅ Use multi-stage builds
FROM python:3.11-slim as builder
# Build steps...

FROM python:3.11-slim as production
COPY --from=builder /app /app

# ✅ Use specific versions
FROM python:3.11.5-slim

# ✅ Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# ✅ Use .dockerignore
# Exclude unnecessary files

# ✅ Minimize layers
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 2. Security Best Practices
```bash
# ✅ Scan images for vulnerabilities
docker scan personal-resume:latest

# ✅ Use non-root user
USER appuser

# ✅ Use minimal base images
FROM python:3.11-alpine

# ✅ Keep images updated
docker pull python:3.11-slim
```

### 3. Performance Best Practices
```bash
# ✅ Use build cache
docker build --cache-from personal-resume:latest .

# ✅ Multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 .

# ✅ Optimize image size
docker images | grep personal-resume
```

---

## Câu Hỏi Phỏng Vấn về Docker

### Câu hỏi cơ bản:

**1. Docker là gì và tại sao sử dụng Docker?**
- Container platform cho phép đóng gói ứng dụng
- Giải quyết vấn đề "works on my machine"
- Portable, scalable, isolated

**2. Sự khác biệt giữa Image và Container?**
- Image: Template read-only chứa code + dependencies
- Container: Instance đang chạy của image

**3. Dockerfile là gì?**
- Script chứa instructions để build Docker image
- Mỗi instruction tạo một layer trong image

### Câu hỏi nâng cao:

**4. Multi-stage builds là gì?**
```dockerfile
FROM node:16 as builder
# Build steps...

FROM nginx:alpine as production
COPY --from=builder /app/dist /usr/share/nginx/html
```

**5. Docker networking modes?**
- bridge: Default, containers có thể communicate
- host: Container sử dụng host network
- none: No network access

**6. Volume vs Bind mount?**
- Volume: Docker quản lý storage
- Bind mount: Mount file/folder từ host

### Kinh nghiệm thực tế:

**"Tôi đã dockerize một website personal resume với:**
- ✅ Multi-stage Dockerfile optimization
- ✅ Docker Compose cho development/production
- ✅ Nginx reverse proxy với load balancing
- ✅ Health checks và monitoring
- ✅ CI/CD pipeline với GitHub Actions
- ✅ Security scanning với Trivy
- ✅ Production deployment với proper logging"

---

## Quick Reference

### Essential Commands
```bash
# Development workflow
docker build -t app:dev .
docker run -d --name app-dev -p 8080:8080 app:dev
docker logs -f app-dev

# Production workflow
docker-compose -f docker-compose.prod.yml up -d
make deploy

# Cleanup
docker system prune -a
```

### Useful Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dps='docker ps'
alias dlog='docker logs -f'
alias dexec='docker exec -it'
alias dclean='docker system prune -a'
```

---

## Kết Luận

Sau khi hoàn thành guide này, bạn đã có:
- ✅ Kiến thức vững về Docker concepts
- ✅ Kinh nghiệm hands-on với containerization
- ✅ Production-ready deployment setup
- ✅ CI/CD pipeline với GitHub Actions
- ✅ Monitoring và troubleshooting skills
- ✅ Kiến thức để trả lời phỏng vấn về Docker

**Pro tip:** Practice bằng cách deploy dự án lên cloud platforms như AWS ECS, Google Cloud Run, hoặc DigitalOcean để có thêm kinh nghiệm cloud deployment!

🎉 **Congratulations! Bạn đã thành công dockerize personal resume website!**