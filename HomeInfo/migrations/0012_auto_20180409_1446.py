# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeInfo', '0011_auto_20180406_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='period_of_stay_end',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='period_of_stay_start',
            field=models.IntegerField(null=True),
        ),
    ]