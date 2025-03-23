.PHONY: install makemigrations migrate run createsuperuser freeze setup clean reset

# Install dependencies
install:
	pip install -r requirements.txt

# Create migrations
makemigrations:
	python manage.py makemigrations

# Apply migrations
migrate: makemigrations
	python manage.py migrate

# Run server
run: migrate
	python manage.py runserver 0.0.0.0:8000

# Create superuser
createsuperuser:
	python manage.py createsuperuser

# Update requirements.txt
freeze:
	pip freeze > requirements.txt

# Clean project
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".DS_Store" -delete
	find . -name "db.sqlite3" -delete

# Complete setup from scratch
setup: install makemigrations migrate

# Reset and setup
reset: clean setup

install:
	pip install -r requirements.txt

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

createsuperuser:
	python manage.py createsuperuser

freeze:
	pip freeze > requirements.txt

setup: install migrate