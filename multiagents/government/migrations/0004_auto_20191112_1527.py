# Generated by Django 2.2.7 on 2019-11-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0003_auto_20191112_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentslog',
            name='dollar',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agentslog',
            name='tenge',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
