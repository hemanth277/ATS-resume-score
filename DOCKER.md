# ATS Resume Score - Docker Setup

## Quick Start with Docker

### Prerequisites
- Docker Desktop installed
- Docker Compose installed (included with Docker Desktop)

### Running the Application

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Stop the services:**
   ```bash
   docker-compose down
   ```

### Docker Commands

**Build images:**
```bash
docker-compose build
```

**Start services in background:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Restart services:**
```bash
docker-compose restart
```

**Remove containers and volumes:**
```bash
docker-compose down -v
```

### Individual Service Commands

**Backend only:**
```bash
cd backend
docker build -t ats-backend .
docker run -p 8000:8000 ats-backend
```

**Frontend only:**
```bash
cd frontend
docker build -t ats-frontend .
docker run -p 80:80 ats-frontend
```

### Development Mode

For development with hot-reload, the docker-compose.yml includes volume mounts:
- Backend code changes will be reflected automatically
- Frontend changes require rebuilding the image

### Health Checks

Both services include health checks:
- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost`

### Troubleshooting

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "8080:8000"  # Backend
  - "8081:80"    # Frontend
```

**Clear everything and rebuild:**
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

**View container logs:**
```bash
docker logs ats-backend
docker logs ats-frontend
```

### Production Deployment

For production, consider:
1. Using environment variables for configuration
2. Setting up proper logging
3. Using a reverse proxy (nginx) for SSL
4. Implementing container orchestration (Kubernetes, Docker Swarm)
5. Setting up monitoring and alerting

### Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ http://localhost
       │
┌──────▼──────────┐
│  Frontend       │
│  (nginx:80)     │
└──────┬──────────┘
       │
       │ /api/* → http://backend:8000
       │
┌──────▼──────────┐
│  Backend        │
│  (FastAPI:8000) │
└─────────────────┘
```

### Notes

- Backend uses Python 3.11 for better ML package compatibility
- Frontend uses nginx alpine for lightweight serving
- Services communicate via Docker network
- Health checks ensure services are ready before accepting traffic
