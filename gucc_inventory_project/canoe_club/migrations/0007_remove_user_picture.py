# Generated by Django 2.2.28 on 2023-02-26 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canoe_club', '0006_auto_20230226_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='picture',
        ),
    ]
