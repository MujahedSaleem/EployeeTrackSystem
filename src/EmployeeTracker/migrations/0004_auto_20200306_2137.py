# Generated by Django 3.0.4 on 2020-03-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeTracker', '0003_auto_20200306_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendants',
            name='inTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='attendants',
            name='outTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]