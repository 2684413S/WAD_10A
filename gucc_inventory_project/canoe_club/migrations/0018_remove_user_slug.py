# Generated by Django 2.2.28 on 2023-03-08 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canoe_club', '0017_trip_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slug',
        ),
    ]