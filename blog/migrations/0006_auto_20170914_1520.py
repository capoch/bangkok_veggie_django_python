# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-14 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170914_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='cuisine',
            field=models.CharField(choices=[('VEG', 'vegetarian'), ('THA', 'thai'), ('CHI', 'chinese'), ('KOR', 'korean'), ('FUS', 'fusion'), ('IND', 'indian'), ('FRE', 'french'), ('ITA', 'italian'), ('MEX', 'mexican'), ('USA', 'american'), ('VIE', 'vietnamese'), ('OTH', 'other')], default='OTH', max_length=3),
            preserve_default=False,
        ),
    ]
