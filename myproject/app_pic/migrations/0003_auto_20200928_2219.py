# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_pic', '0002_auto_20200928_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic_4k',
            name='img_cre_time',
            field=models.DateTimeField(),
        ),
    ]
