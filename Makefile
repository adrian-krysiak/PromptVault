DC=docker compose

.PHONY: up down logs init admin urls reset

up:
	$(DC) up --build -d

down:
	$(DC) down

logs:
	$(DC) logs -f

init:
	$(DC) exec backend python manage.py migrate

admin:
	$(DC) exec backend python manage.py createsuperuser

urls:
	@echo "Frontend: http://localhost:8080"
	@echo "Backend API: http://localhost:8081/api/prompts/"
	@echo "Django admin: http://localhost:8081/admin/"

reset:
	$(DC) down -v
	$(DC) up --build -d
	$(DC) exec backend python manage.py migrate
