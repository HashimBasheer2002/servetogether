# Generated by Django 5.0.1 on 2025-01-29 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_otherdonation_resource_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherdonation',
            name='special_instructions',
        ),
    ]
