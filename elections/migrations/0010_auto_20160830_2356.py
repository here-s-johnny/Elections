# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-30 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0009_auto_20160829_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='last_modification',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
