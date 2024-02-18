# Generated by Django 4.2 on 2024-02-18 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libgen', '0002_keywordsearched_search_date_searchresult_key_word_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='search_result', to='libgen.book'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='key_word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='search_result', to='libgen.keywordsearched'),
        ),
    ]
