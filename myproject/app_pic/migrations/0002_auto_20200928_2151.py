# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_pic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic_4k',
            name='img_cre_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 21, 51, 47, 913453)),
        ),
    ]
