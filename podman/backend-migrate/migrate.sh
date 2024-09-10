#!/usr/bin/env bash

export PATH="/root/.local/bin:${PATH}"

# install pipx
apt-get update && apt-get install --no-install-suggests --no-install-recommends --yes pipx

# install poetry
pipx install poetry
# poetry install
poetry install --only=main

poetry run python manage.py migrate