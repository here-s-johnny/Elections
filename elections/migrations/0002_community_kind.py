# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-07 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='kind',
            field=models.CharField(choices=[(1, 'miasto'), (2, 'wie\u015b'), (3, 'statki'), (4, 'zagranica')], default='miasto', max_length=10),
        ),
    ]
