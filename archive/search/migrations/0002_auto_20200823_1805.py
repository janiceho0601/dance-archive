# Generated by Django 3.1 on 2020-08-24 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_update',
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
