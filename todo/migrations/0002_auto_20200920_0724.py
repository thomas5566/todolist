# Generated by Django 3.1 on 2020-09-20 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
