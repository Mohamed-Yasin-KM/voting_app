.PHONY: build up down logs clean stop restart help dev prod

help:
	@echo "Docker Management Commands"
	@echo "========================="
	@echo "make dev        - Start development environment"
	@echo "make prod       - Start production environment"
	@echo "make build      - Build Docker images"
	@echo "make up         - Start services (docker-compose up -d)"
	@echo "make down       - Stop services (docker-compose down)"
	@echo "make stop       - Stop services without removing (docker-compose stop)"
	@echo "make restart    - Restart services"
	@echo "make logs       - View live logs"
	@echo "make clean      - Remove containers, volumes, and images"
	@echo "make shell      - Open bash in web container"
	@echo "make db-shell   - Open psql in database container"
	@echo "make test       - Run tests in container"

dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "✓ Development environment ready at http://localhost:5000"

prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Production environment ready"
	@echo "  - Web: http://localhost"
	@echo "  - Database: Internal only"

build:
	@echo "Building Docker images..."
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

stop:
	docker-compose stop

restart:
	@echo "Restarting services..."
	docker-compose restart

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

clean:
	@echo "Removing containers, volumes, and images..."
	docker-compose down -v
	docker rmi $$(docker images -q voting-app) 2>/dev/null || true
	@echo "✓ Cleanup complete"

shell:
	docker-compose exec web /bin/bash

db-shell:
	docker-compose exec db psql -U $${DB_USER:-postgres} -d $${DB_NAME:-voting_app}

test:
	docker-compose exec web python -m pytest

ps:
	docker-compose ps

stats:
	docker stats

build-prod:
	docker-compose -f docker-compose.prod.yml build --no-cache

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down

logs-prod:
	docker-compose -f docker-compose.prod.yml logs -f
