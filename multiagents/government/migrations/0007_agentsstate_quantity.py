# Generated by Django 2.2.7 on 2019-12-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0006_auto_20191210_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentsstate',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]