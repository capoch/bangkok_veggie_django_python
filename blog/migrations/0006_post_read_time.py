# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170124_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]