# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-09-05 08:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0012_auto_20160831_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='last_modification',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
