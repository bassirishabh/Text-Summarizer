# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 19:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summarizer', '0005_auto_20171126_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getfile',
            name='length',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
