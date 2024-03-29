# Generated by Django 4.2 on 2024-02-17 14:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libgen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordsearched',
            name='search_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 2, 17, 14, 55, 29, 758029, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchresult',
            name='key_word',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='search_result', to='libgen.keywordsearched'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_result', to='libgen.book'),
        ),
    ]
