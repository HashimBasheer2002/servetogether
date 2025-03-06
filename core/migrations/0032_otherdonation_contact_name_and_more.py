# Generated by Django 5.0.1 on 2025-01-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_otherdonation_contact_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherdonation',
            name='contact_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='donation_type',
            field=models.CharField(choices=[('Furniture', 'Furniture'), ('Clothing', 'Clothing'), ('Books', 'Books'), ('Electronics', 'Electronics'), ('Other', 'Other')], default='Other', max_length=50),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='pickup_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='otherdonation',
            name='special_instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
