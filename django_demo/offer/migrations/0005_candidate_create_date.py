# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 06:12
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_candidate_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='create_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
