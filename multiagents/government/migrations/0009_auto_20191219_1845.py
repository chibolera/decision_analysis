# Generated by Django 2.2.7 on 2019-12-19 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0008_auto_20191219_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentsstate',
            name='quantity',
            field=models.FloatField(default=0.0),
        ),
    ]
