# Generated by Django 3.0.9 on 2020-11-04 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_auto_20201104_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='entry',
            field=models.TextField(max_length=500),
        ),
    ]
