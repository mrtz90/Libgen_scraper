# Generated by Django 4.2 on 2024-02-18 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libgen', '0003_alter_searchresult_book_alter_searchresult_key_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=55, unique=True, verbose_name='Author Name'),
        ),
        migrations.AlterField(
            model_name='book',
            name='about_book',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(related_name='author', to='libgen.author', verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=55, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(verbose_name='Number of Pages'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ManyToManyField(related_name='publisher', to='libgen.publisher', verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='book',
            name='topic',
            field=models.CharField(max_length=100, verbose_name='Topic'),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.PositiveIntegerField(verbose_name='Publication Year'),
        ),
        migrations.AlterField(
            model_name='keywordsearched',
            name='key_word',
            field=models.CharField(max_length=100, verbose_name='Keyword Searched'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=55, unique=True, verbose_name='Publisher Name'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='search_result', to='libgen.book', verbose_name='Book'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='link',
            field=models.URLField(verbose_name='Search Result Link'),
        ),
    ]
