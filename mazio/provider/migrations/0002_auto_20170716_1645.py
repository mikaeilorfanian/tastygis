# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='currency',
            field=models.CharField(max_length=3),
        ),
    ]
