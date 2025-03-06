# Generated by Django 5.0.1 on 2025-02-04 05:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_campaign_volunteers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='joined_campaigns', to=settings.AUTH_USER_MODEL),
        ),
    ]
