# Generated by Django 5.1.4 on 2025-03-31 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviewapp', '0002_movie_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
    ]
