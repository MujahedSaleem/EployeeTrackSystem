# Generated by Django 3.0.4 on 2020-03-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Attendant',
            name='out_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]