# Generated by Django 5.0.1 on 2025-01-31 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_rename_title_disasterreport_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='help_request',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='core.helprequest'),
        ),
    ]
