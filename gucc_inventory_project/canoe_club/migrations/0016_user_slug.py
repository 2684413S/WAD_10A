# Generated by Django 2.2.28 on 2023-03-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canoe_club', '0015_auto_20230308_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(default='no', unique=True),
            preserve_default=False,
        ),
    ]