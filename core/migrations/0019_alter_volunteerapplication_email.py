# Generated by Django 5.0.1 on 2025-01-23 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerapplication',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]
