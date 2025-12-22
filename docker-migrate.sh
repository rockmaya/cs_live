#!/bin/bash
# Run Django migrations safely inside container

docker-compose run --rm web python manage.py migrate
