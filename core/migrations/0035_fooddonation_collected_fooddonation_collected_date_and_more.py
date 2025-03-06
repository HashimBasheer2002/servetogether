# Generated by Django 5.0.1 on 2025-01-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_remove_otherdonation_special_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooddonation',
            name='collected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fooddonation',
            name='collected_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='collected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='collected_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
