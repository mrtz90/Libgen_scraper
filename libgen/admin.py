from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ExportMixin

from .models import Book, Author, Publisher, KeyWordSearched, SearchResult


@admin.register(Book)
class BookAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        'id', 'title', 'display_authors', 'display_publisher',
        'year', 'language', 'pages', 'topic', 'book_file_path',
        'image_file_path',
    ]
    list_display_links = ['id', 'display_authors', 'display_publisher', ]
    list_filter = ['title', 'author', 'publisher']

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.author.all()])

    def display_publisher(self, obj):
        return ", ".join([publisher.name for publisher in obj.publisher.all()])


@admin.register(Author)
class AuthorAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(Publisher)
class PublisherAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(KeyWordSearched)
class KeyWordSearchedAdmin(admin.ModelAdmin):
    list_display = ['id', 'key_word', 'search_date']
    list_display_links = ['id', 'key_word']


@admin.register(SearchResult)
class SearchResultAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'key_word', 'book', 'link']
    list_display_links = ['id', 'book', 'link']


class BookResource(ExportMixin, ModelResource):
    class Meta:
        model = Book
        fields = ('title', 'author__name', 'publisher__name', 'year', 'language')
