# Generated by Django 5.0.1 on 2025-01-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_volunteer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
