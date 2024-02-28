import os

from import_export.fields import Field
from import_export.widgets import ManyToManyWidget
from import_export.resources import ModelResource
from import_export.formats.base_formats import XLS, CSV, JSON

from .models import Book, Author, Publisher


class BookResource(ModelResource):
    author = Field(
        attribute='author',
        widget=ManyToManyWidget(Author, field='name', separator='|'),
    )
    publisher = Field(
        attribute='publisher',
        widget=ManyToManyWidget(Publisher, field='name', separator='|'),

    )

    class Meta:
        model = Book
        fields = (
            'title', 'author', 'publisher', 'year', 'language', 'pages', 'topic',
            'about_book', 'book_file_path', 'image_file_path'
        )


def export_books(export_format, folder_path, created):
    print(created)
    query = Book.objects.filter(created_at=created)

    # Initialize the resource based on the selected export format
    export_resource = BookResource()
    f_format = CSV()

    if export_format == 'json':
        export_resource = BookResource()
        f_format = JSON()
    elif export_format == 'xls':
        export_resource = BookResource()
        f_format = XLS()

    # Export the data using import_export
    dataset = export_resource.export(queryset=query, format=f_format)
    file_path = os.path.join(folder_path, f"report_books.{f_format.get_extension()}")
    if export_format == 'xls':
        with open(file_path, 'wb') as f:
            f.write(dataset.xls)
    else:
        with open(file_path, 'wb') as f:
            f.write(bytes(dataset.export(export_format), 'utf-8'))

    return file_path
