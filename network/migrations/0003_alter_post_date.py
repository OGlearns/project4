# Generated by Django 4.1.1 on 2022-11-24 22:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 24, 22, 29, 39, 605404, tzinfo=datetime.timezone.utc)),
        ),
    ]
