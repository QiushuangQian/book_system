# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2020-03-15 08:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20200315_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='num',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]
