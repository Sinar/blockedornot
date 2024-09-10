# Generated by Django 5.1.1 on 2024-09-10 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField()),
                ('query_cleaned', models.CharField()),
                ('dns_public_result', models.CharField()),
                ('dns_public', models.CharField()),
                ('dns_isp_result', models.CharField()),
                ('dns_isp', models.CharField()),
                ('blocked', models.BooleanField()),
                ('different_ip', models.BooleanField()),
                ('measurement_url', models.CharField(blank=True)),
                ('creation_time', models.DateTimeField(default=datetime.datetime(2024, 9, 10, 14, 13, 22, 498677))),
            ],
        ),
    ]
