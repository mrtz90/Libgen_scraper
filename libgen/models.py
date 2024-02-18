from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=55, unique=True, verbose_name='Author Name')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=55, unique=True, verbose_name='Publisher Name')

    def __str__(self):
        return self.name


class KeyWordSearched(models.Model):
    key_word = models.CharField(max_length=100, verbose_name='Keyword Searched')
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key_word


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Title')
    author = models.ManyToManyField(
        Author, related_name='author',
        verbose_name='Author',
    )
    publisher = models.ManyToManyField(
        Publisher, related_name='publisher',
        verbose_name='Publisher'
    )
    year = models.PositiveIntegerField(verbose_name='Publication Year')
    language = models.CharField(max_length=55, verbose_name='Language')
    pages = models.IntegerField(verbose_name='Number of Pages')
    topic = models.CharField(max_length=100, verbose_name='Topic')
    about_book = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.title


class SearchResult(models.Model):
    key_word = models.ForeignKey(
        KeyWordSearched,
        related_name='search_result',
        on_delete=models.PROTECT
    )
    book = models.ForeignKey(
        Book, related_name='search_result',
        on_delete=models.PROTECT,
        verbose_name="Book"
    )
    link = models.URLField(verbose_name='Search Result Link')

    def __str__(self):
        return self.link
