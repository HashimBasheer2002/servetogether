# Generated by Django 5.0.1 on 2025-01-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_volunteer_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/'),
        ),
    ]
