# Generated by Django 3.0.8 on 2020-07-13 14:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0005_auto_20200713_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelupload',
            name='document',
            field=models.FileField(upload_to='user/', validators=[django.core.validators.FileExtensionValidator(['xlsx'])]),
        ),
    ]
