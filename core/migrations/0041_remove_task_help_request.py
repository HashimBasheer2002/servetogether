# Generated by Django 4.2.4 on 2025-01-31 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_task_help_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='help_request',
        ),
    ]
