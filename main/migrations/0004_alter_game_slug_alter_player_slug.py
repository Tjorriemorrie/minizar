# Generated by Django 4.1.4 on 2023-01-09 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_building_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(blank=True, default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
