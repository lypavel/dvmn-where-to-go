# Generated by Django 4.2 on 2024-05-17 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0010_alter_place_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='place',
            unique_together={('title', 'id')},
        ),
        migrations.RemoveField(
            model_name='place',
            name='slug',
        ),
    ]
