# Generated by Django 3.0.4 on 2020-03-07 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EmployeeTracker', '0006_auto_20200307_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inTime', models.DateTimeField(auto_now=True)),
                ('outTime', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='leaves', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
