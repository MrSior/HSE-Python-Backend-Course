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