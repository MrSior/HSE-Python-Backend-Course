#!/bin/bash

make install
make makemigrations
make migrate

exec "$@"
