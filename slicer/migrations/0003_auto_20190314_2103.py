# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-14 21:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slicer', '0002_auto_20170310_0642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageseries',
            options={'verbose_name_plural': 'Image Series'},
        ),
    ]