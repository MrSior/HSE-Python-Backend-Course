FROM python:3.9-slim

WORKDIR /myproject

RUN apt-get update && apt-get install -y libpq-dev gcc && \
    apt-get install -y make && \
    rm -rf /var/lib/apt/lists/*
