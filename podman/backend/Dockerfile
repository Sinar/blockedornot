FROM debian:12-slim as builder

ENV PATH="/root/.local/bin:${PATH}" \
    POETRY_VERSION=1.8.3

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx python-is-python3 wget && \
    pipx install "poetry==$POETRY_VERSION" && \
    pipx inject poetry poetry-plugin-bundle && \
    poetry bundle venv --python=/usr/bin/python3 --only=main /venv && \
    wget https://github.com/Dj-Codeman/doge/releases/latest/download/doge_linux_64bit && \
    wget https://github.com/ooni/probe-cli/releases/latest/download/miniooni-linux-amd64 && \
    chmod +x doge_linux_64bit && \
    chmod +x miniooni-linux-amd64 && \
    sync

FROM gcr.io/distroless/python3-debian12

EXPOSE 8000/tcp

COPY --from=builder /venv /venv
COPY --from=builder /app/doge_linux_64bit /usr/bin/doge
COPY --from=builder /app/miniooni-linux-amd64 /usr/bin/miniooni

ENTRYPOINT ["/venv/bin/gunicorn", "-w", "3", "blockedornot.wsgi:application", "--bind=0.0.0.0:8000"]
