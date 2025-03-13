## Создание моков
В корне проекта вызвать команду:

```shell
docker exec -it hw-6-django-project-2-db-1 psql -U user -d mydb -f ./storage/init.sql
```

## Создать миграции
В корне проекта вызвать команду:

```shell
docker exec -it hw-6-django-project-2-web-1 make makemigrations
```

## Выполнить миграции
В корне проекта вызвать команду:

```shell
docker exec -it hw-6-django-project-2-web-1 make migrate
```