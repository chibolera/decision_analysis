# Generated by Django 2.2.7 on 2019-11-12 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0004_auto_20191112_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentslog',
            name='quantity',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]