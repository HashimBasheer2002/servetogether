# Generated by Django 5.0.1 on 2025-01-23 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_volunteer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
