# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-20 03:32
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantedge', '0003_asset_usability_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='aoi',
            name='raw_coordinates',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), null=True, size=None),
        ),
    ]