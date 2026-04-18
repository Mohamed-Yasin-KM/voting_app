# Docker Setup Guide

This application is optimized for containerization with Docker. Follow the instructions below to build and run the application.

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)

## Quick Start

1. **Clone and navigate to the project**
   ```bash
   cd gitops
   ```

2. **Create a `.env` file** (copy from `.env.example` and customize if needed)
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your desired configuration:
   ```
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=voting_app
   DB_USER=postgres
   DB_PASSWORD=secure_password_change_me
   FLASK_ENV=production
   FLASK_PORT=5000
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Navigate to `http://localhost:5000` in your browser

5. **View logs**
   ```bash
   docker-compose logs -f web  # Flask app logs
   docker-compose logs -f db   # PostgreSQL logs
   ```

## Docker Optimizations Applied

### 1. Multi-Stage Build
- **Builder stage**: Installs all build dependencies (gcc, build-essential) and compiles packages
- **Production stage**: Uses only runtime dependencies, reducing image size by ~60%

### 2. Image Optimization
- Uses `python:3.12-slim` as base (minimal image ~150MB vs 400MB+ for full image)
- Uses `postgres:16-alpine` for database (~80MB vs 300MB+ for full image)
- Removes apt cache after installation to reduce layer size

### 3. Security Best Practices
- Non-root user (`appuser` with UID 1000) runs the application
- No sensitive files in the image
- `.dockerignore` excludes unnecessary files
- Virtual environment for dependency isolation

### 4. Performance Enhancements
- **Gunicorn WSGI server** instead of Flask development server
  - 4 worker processes for concurrent request handling
  - 2 threads per worker for better resource utilization
  - Timeout: 60 seconds for request processing
- **Health checks** to detect and auto-restart unhealthy containers
- **Proper logging** with JSON format for centralized monitoring

### 5. Production-Ready Configuration
- `PYTHONUNBUFFERED=1` for real-time log output
- `PYTHONDONTWRITEBYTECODE=1` to avoid .pyc file generation
- Environment-based configuration (no hardcoded values)
- Volume mounting for logs persistence

## Image Sizes

After optimization:
- **Flask app image**: ~400MB (includes all dependencies)
- **PostgreSQL image**: ~80MB
- **Total**: ~480MB

## Docker Compose Services

### web (Flask Application)
- **Port**: 5000 (configurable via `FLASK_PORT`)
- **Service**: Gunicorn WSGI server with 4 workers
- **Health check**: Every 30 seconds, 40-second startup grace period
- **Restart policy**: Unless stopped
- **Logs**: JSON format with 10MB max per file, 3 files rotation

### db (PostgreSQL)
- **Port**: 5432 (configurable via `DB_PORT`)
- **Storage**: Named volume `db_data` for persistence
- **Health check**: PostgreSQL readiness check every 10 seconds
- **Restart policy**: Unless stopped
- **Logs**: JSON format with log rotation

## Management Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes database!)
docker-compose down -v

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec web python -c "import voting_app; print('App loaded')"

# Rebuild images
docker-compose build --no-cache

# View service logs
docker-compose logs -f web

# Scale workers (if needed)
docker-compose up -d --scale web=2
```

## Environment Variables

All variables from `.env` are available:
- `DB_HOST`: PostgreSQL hostname (default: db)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: voting_app)
- `DB_USER`: PostgreSQL user (default: postgres)
- `DB_PASSWORD`: PostgreSQL password
- `FLASK_ENV`: Flask environment (production/development)
- `FLASK_PORT`: Application port (default: 5000)

## Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution**: Ensure the database is healthy:
```bash
docker-compose logs db
```

### Port Already in Use
```
Error: bind: address already in use
```
**Solution**: Change port in `.env`:
```bash
FLASK_PORT=5001  # Use different port
```

### Memory Issues
Increase Docker memory limit in Docker Desktop settings or via docker run:
```bash
docker run -m 2g ...
```

## Production Deployment

### For Kubernetes
1. Build and push image to registry:
   ```bash
   docker build -t myregistry/voting-app:latest .
   docker push myregistry/voting-app:latest
   ```

2. Use the image in your Kubernetes manifests

### For Cloud Platforms (AWS ECS, GCP Cloud Run, Azure Container Instances)
1. Push image to container registry
2. Deploy using platform-specific tools

### For Standalone Docker Host
```bash
docker-compose -f docker-compose.yml up -d
```

## Monitoring

Health checks are configured for both services:
- **web**: HTTP health check every 30 seconds
- **db**: PostgreSQL readiness check every 10 seconds

Monitor container status:
```bash
docker-compose ps
```

## Security Notes

⚠️ **Important**: 
- Change `DB_PASSWORD` in `.env` files before deploying to production
- Don't commit `.env` files to version control
- Use Docker secrets for production deployments
- Implement reverse proxy (nginx) for SSL/TLS in production
