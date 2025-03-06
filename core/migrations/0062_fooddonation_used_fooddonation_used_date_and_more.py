# Generated by Django 5.0.1 on 2025-02-06 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_remove_fooddonation_used_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooddonation',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fooddonation',
            name='used_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='used_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
