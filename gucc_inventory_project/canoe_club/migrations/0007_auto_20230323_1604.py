# Generated by Django 2.2.28 on 2023-03-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canoe_club', '0006_social_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
