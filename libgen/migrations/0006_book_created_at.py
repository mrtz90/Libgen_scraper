# Generated by Django 4.2 on 2024-02-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libgen', '0005_book_book_file_path_book_image_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default='2024-02-26 12:21:11'),
            preserve_default=False,
        ),
    ]