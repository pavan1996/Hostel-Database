# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeInfo', '0003_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='zipcode',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
