# Generated by Django 3.0.9 on 2020-11-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_journal'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='entry',
            field=models.CharField(default='', max_length=500),
        ),
    ]
