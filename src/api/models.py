from datetime import datetime

from django.db import models


class Query(models.Model):
    query = models.CharField()
    query_cleaned = models.CharField()

    dns_public_result = models.CharField()
    dns_public = models.CharField()

    dns_isp_result = models.CharField()
    dns_isp = models.CharField()

    blocked = models.BooleanField()
    different_ip = models.BooleanField()
    measurement_url = models.CharField(blank=True)

    creation_time = models.DateTimeField(default=datetime.now())