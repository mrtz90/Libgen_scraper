from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=55, unique=True)


class Publisher(models.Model):
    name = models.CharField(max_length=55, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ManyToManyField(
        Author, related_name='author',
        on_delete=models.CASCADE
    )
    publisher = models.ManyToManyField(
        Publisher, related_name='publisher',
        on_delete=models.CASCADE
    )
    year = models.PositiveIntegerField()
    language = models.CharField(max_length=55)
    pages = models.IntegerField()
    topic = models.CharField(max_length=100)
    about_book = models.TextField()


class KeyWordSearched(models.Model):
    key_word = models.CharField(max_length=100)


class SearchResult(models.Model):
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE)
    link = models.URLField()
