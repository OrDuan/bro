# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_auth_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='brotype',
            name='bros_needed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brotype',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
