# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 05:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(choices=[('SH', 'Shanghai'), ('HZ', 'Hangzhou'), ('TJ', 'Tianjian'), ('DL', 'Dalian'), ('BJ', 'Beijing'), ('SZ', 'Shenzhen')], max_length=2, null=True),
        ),
    ]
