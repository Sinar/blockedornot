#!/usr/bin/env bash
NETWORK="${DOCKER_NETWORK:-blockedornot}"

podman run \
    --rm  -it \
    --env-file .env \
    --mount type=bind,source="$(pwd)",target=/project \
    --workdir /project \
    --network "$NETWORK" \
    python:3.11-slim bash podman/backend-migrate/migrate.sh
