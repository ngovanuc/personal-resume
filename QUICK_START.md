# 🚀 Quick Start với Docker

## Bước 1: Cài đặt Docker

### Windows:
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Install và restart máy
3. Start Docker Desktop
4. Kiểm tra: `docker --version`

### Linux:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

## Bước 2: Build và Run

### Cách 1: Sử dụng Docker Commands
```bash
# Build image
docker build -t personal-resume:latest .

# Run container
docker run -d --name my-resume -p 8080:8080 personal-resume:latest

# Xem logs
docker logs -f my-resume

# Access website: http://localhost:8080
```

### Cách 2: Sử dụng Docker Compose (Recommended)
```bash
# Start development environment
docker-compose up -d

# Xem logs
docker-compose logs -f

# Stop
docker-compose down
```

### Cách 3: Sử dụng Makefile (Easiest)
```bash
# Build và test
make build-test

# Development
make dev

# Production
make deploy
```

## Bước 3: Verify

1. **Check container:** `docker ps`
2. **Check logs:** `docker logs my-resume`
3. **Access website:** http://localhost:8080
4. **Health check:** `curl http://localhost:8080`

## Troubleshooting

**Docker không start:**
- Windows: Start Docker Desktop
- Linux: `sudo systemctl start docker`

**Port 8080 đã sử dụng:**
```bash
# Tìm process đang dùng port
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Linux/Mac

# Kill process
taskkill /F /PID <PID>        # Windows
kill -9 <PID>                # Linux/Mac
```

**Container không build:**
```bash
# Check Dockerfile syntax
docker build --no-cache -t personal-resume:latest .

# Check logs
docker logs my-resume
```

## Production Deployment

```bash
# Build production image
docker build -t personal-resume:prod .

# Run production container
docker run -d \
  --name personal-resume-prod \
  -p 8080:8080 \
  --restart always \
  -e ENV=production \
  personal-resume:prod
```

## Cloud Deployment

### Deploy to DigitalOcean:
```bash
# Build và push to registry
docker build -t registry.digitalocean.com/your-registry/personal-resume .
docker push registry.digitalocean.com/your-registry/personal-resume

# Deploy on droplet
docker run -d -p 80:8080 --restart always your-registry/personal-resume
```

### Deploy to AWS ECS:
1. Push image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure load balancer

## Next Steps

1. ✅ **Complete Docker setup**
2. ✅ **Test locally**
3. 🚀 **Deploy to cloud**
4. 📊 **Add monitoring**
5. 🔐 **Add SSL certificate**

**Chúc mừng! Bạn đã có kinh nghiệm Docker để chia sẻ với nhà tuyển dụng! 🎉**