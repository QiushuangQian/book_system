# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2020-03-12 08:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20200312_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='book',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
    ]
