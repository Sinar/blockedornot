import subprocess
from concurrent.futures import ProcessPoolExecutor
from os import environ
from typing import NamedTuple
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

from api.models import Query

DEFAULT_DNS_PUBLIC = "1.1.1.1"
DEFAULT_DNS_ISP = "183.171.212.193"
DEFAULT_SINKHOLE_IP = "175.139.142.25"

logger = structlog.get_logger(__name__)

class DNSCheck(NamedTuple):
    blocked: bool
    different_ip: bool

    dns_isp_result: str
    dns_public_result: str


@require_GET
def query(request: HttpRequest) -> HttpResponse:
    result = HttpResponseBadRequest()

    query = _process_query(request.GET.get("query"))

    if query:
        try:
            dns_result = _doge_check_is_blocked(query)
            measurement = (
                _ooni_check_url(query)
                if dns_result.blocked or dns_result.different_ip
                else None
            )
            result = JsonResponse(
                dict(
                    {
                        "blocked": dns_result.blocked,
                        "different_ip": dns_result.different_ip,
                        "measurement": measurement,
                    },
                    query=query,
                )
            )
            Query.objects.create(
                query=request.GET.get("query"),
                query_cleaned=query,
                dns_public_result=dns_result.dns_public_result,
                dns_public=environ.get("DNS_PUBLIC", DEFAULT_DNS_PUBLIC),
                dns_isp_result=dns_result.dns_isp_result,
                dns_isp=environ.get("DNS_ISP", DEFAULT_DNS_ISP),
                blocked=dns_result.blocked,
                different_ip=dns_result.different_ip,
                measurement_url=measurement or "",
            )

        except Exception as e:
            logger.exception(e)
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


def _doge_check_is_blocked(query: str) -> DNSCheck:
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

        results = tuple(future.result(timeout=5).stdout.strip() for future in futures)
        result_set = tuple(set(result.splitlines()) for result in results)

        return DNSCheck(
            blocked=any(
                ip.startswith(environ.get("SINKHOLE_IP", DEFAULT_SINKHOLE_IP))
                for ip in result_set[1]
            ),
            different_ip=len(result_set[0].intersection(result_set[1])) == 0,
            dns_isp_result=results[0],
            dns_public_result=results[1],
        )


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
