# Generated by Django 4.2 on 2024-05-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_place_description_long'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Место', 'verbose_name_plural': 'Места'},
        ),
        migrations.AlterField(
            model_name='place',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Уникальный id'),
        ),
        migrations.AlterUniqueTogether(
            name='place',
            unique_together={('title', 'slug')},
        ),
    ]
