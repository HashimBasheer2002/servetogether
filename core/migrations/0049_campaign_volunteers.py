# Generated by Django 5.0.1 on 2025-02-04 05:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_campaign'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='joined_campaigns', to=settings.AUTH_USER_MODEL),
        ),
    ]
