# Generated by Django 2.2.5 on 2020-03-21 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='TaskCategory',
        ),
    ]