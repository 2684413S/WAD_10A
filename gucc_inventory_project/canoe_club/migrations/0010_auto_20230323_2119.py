# Generated by Django 2.2.28 on 2023-03-23 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canoe_club', '0009_merge_20230323_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kit',
            name='maintenance',
            field=models.BooleanField(default=False),
        ),
    ]
