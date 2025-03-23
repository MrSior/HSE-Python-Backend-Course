#!/bin/bash

make install
make makemigrations blog
make migrate

exec "$@"
