# Generated by Django 3.0.4 on 2020-03-15 14:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_tracker', '0007_leave'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vacation',
            unique_together={('emp', 'date')},
        ),
    ]
