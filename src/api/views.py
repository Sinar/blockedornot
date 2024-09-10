import json
import subprocess
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from os import environ
from typing import Tuple
from urllib.parse import urlparse

import structlog
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
from django.views.decorators.http import require_GET

DEFAULT_DNS_PUBLIC = "1.1.1.1"
DEFAULT_DNS_ISP = "183.171.212.193"
DEFAULT_SINKHOLE_IP = "175.139.142.25"

logger = structlog.get_logger(__name__)


@require_GET
def query(request: HttpRequest) -> HttpResponse:
    result = HttpResponseBadRequest()

    query = _process_query(request.GET.get("query"))

    if query:
        try:
            is_blocked, different_ip = _doge_check_is_blocked(query)
            result = JsonResponse(
                dict(
                    {
                        "blocked": is_blocked,
                        "different_ip": different_ip,
                        "measurement": _ooni_check_url(query)
                        if is_blocked or different_ip
                        else None,
                    },
                    query=query,
                )
            )

        except Exception:
            result = HttpResponseServerError()

    return result


def _process_query(query: str | None) -> str | None:
    result = None

    if query:
        result = urlparse(
            query if query.startswith("http") else f"http://{query}"
        ).netloc

    return result


def _doge_check_against_dns(query: str, dns: str) -> subprocess.CompletedProcess:
    process = subprocess.run(
        [
            'doge',
            "-1",
            query,
            f"@{dns}",
        ],
        capture_output=True,
        check=True,
        text=True,
    )

    for line in process.stdout.splitlines():
        logger.info(line, query=query, dns=dns, command="doge")

    return process


def _doge_check_is_blocked(query: str) -> Tuple[bool, bool]:
    with ProcessPoolExecutor() as executor:
        futures = (
            executor.submit(
                _doge_check_against_dns,
                query,
                environ.get("DNS_PUBLIC", DEFAULT_DNS_PUBLIC),
            ),
            executor.submit(
                _doge_check_against_dns,
                query,
                environ.get("DNS_ISP", DEFAULT_DNS_ISP),
            ),
        )

        result = tuple(
            set(future.result(timeout=5).stdout.strip().splitlines())
            for future in futures
        )

        return any(
            ip.startswith(environ.get("SINKHOLE_IP", DEFAULT_SINKHOLE_IP))
            for ip in result[1]
        ), len(result[0].intersection(result[1])) == 0


def _ooni_check_url(query: str) -> str:
    process = subprocess.run(
        [
            'miniooni',
            'urlgetter',
            '-y',
            f'-OResolverURL=udp://{environ.get("DNS_ISP", DEFAULT_DNS_ISP)}:53/',
            f'-ODNSCache=one.one.one.one 1.0.0.1 1.1.1.1',
            f'-idnslookup://{query}/',
        ],
        capture_output=True,
        check=True,
        text=True
    )

    for line in process.stderr.splitlines():
        logger.info(line, query=query, command="miniooni")

    return (
        tuple(
            line for line in process.stderr.splitlines() if "Measurement URL" in line
        )[0]
        .partition("URL")[-1]
        .strip(": ")
    )
