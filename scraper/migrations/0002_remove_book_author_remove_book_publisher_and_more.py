# Generated by Django 4.2 on 2024-02-17 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='publisher',
        ),
        migrations.DeleteModel(
            name='KeyWordSearched',
        ),
        migrations.RemoveField(
            model_name='searchresult',
            name='book',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Publisher',
        ),
        migrations.DeleteModel(
            name='SearchResult',
        ),
    ]