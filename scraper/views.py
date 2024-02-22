import os
import re
import requests
import shutil
from datetime import datetime
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from import_export.admin import ExportActionMixin
from import_export.resources import ModelResource

from libgen.models import Author, Book, Publisher, SearchResult, KeyWordSearched
from .exporter import export_books
from .forms import ScrapForm


def scrape_form(request):
    """
    View function to handle the scraping form submission.
    """
    if request.method == 'POST':
        form = ScrapForm(request.POST)
        if form.is_valid():
            key_word = form.cleaned_data['key_word']
            from_page = form.cleaned_data['from_page']
            to_page = form.cleaned_data['to_page']
            export_format = form.cleaned_data['export_format']

        result = search_key_word(key_word, from_page, to_page)

        # Create a folder for images
        folder_path = os.path.join(settings.MEDIA_ROOT, key_word
                                   + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                                   )
        os.makedirs(folder_path, exist_ok=True)
        print(folder_path)
        scrape_books(result, key_word, folder_path)
        exported_file_path = export_books(key_word, from_page, to_page, export_format, folder_path)
        # zip_output_folder(folder_path)
        return HttpResponse("Scraping completed successfully!")
    else:
        form = ScrapForm()
    return render(request, 'scrape_form.html', {'form': form})


def search_key_word(key_word, from_page, to_page):
    """
    Search for the given keyword in Libgen and extract links to books.
    """
    url = f'https://libgen.is/search.php?req={key_word}' \
          f'&open=0&res=25&view=simple&phrase=1&column=def'
    response = requests.get(url)
    print("status code:", response.status_code, "Fetching url:", url)
    content = BeautifulSoup(response.text, "html.parser")
    tables = content.find_all('table')
    items = tables[1].find_all('td')[0].text.split('files')[0]
    pages = int(items) // 25 + 1
    links = []
    if pages < to_page:
        to_page = pages
    for page in range(from_page, to_page):
        url = f'https://libgen.is/search.php?req={key_word}' \
              f'&open=0&res=25&view=simple&phrase=1&column=def&page={page}'
        response = requests.get(url)
        print("status code:", response.status_code, "Fetching url:", url)
        content = BeautifulSoup(response.text, "html.parser")
        info = content.find_all('table')[2].find_all('tr')[1:]
        for tr in info:
            tds = tr.find_all('td')
            all_a = tds[2].find_all('a')
            for a in all_a:
                if a['href'].startswith('book'):
                    link = a['href']
                    links.append(link)
    print(len(links))
    return links


def scrape_books(links, keyword_searched, folder_path):
    """
    Scrape book details from Libgen based on provided links.
    """
    for link in links:
        try:
            url = f'https://libgen.is/{link}'
            response = requests.get(url, verify=False)
            print("status code:", response.status_code, "Fetching url:", url)
            content = BeautifulSoup(response.text, "html.parser")
            trs = content.find('table').find_all('tr')
            image_link = 'https://libgen.rs' + trs[1].find('img')['src']
            title = trs[1].find_all('a')[1].text.strip()
            file_url = trs[1].find_all('a')[1]['href']
            authors = remove_strings_in_parentheses(trs[10].find('b').text.split(','))
            publisher = trs[12].find_all('td')[1].text.strip()
            year = trs[13].find_all('td')[1].text.strip()
            language = trs[14].find_all('td')[1].text.strip()
            pages = trs[14].find_all('td')[3].text.strip().split('\\')[0]
            book_file_type = trs[18].find_all('td')[3].text
            topic = trs[22].find_all('td')[1].text.strip()
            about_book = trs[31].find('td').text.strip()

            # Save the html file
            download_and_save_file(response, 'html', title, folder_path, 'html')
            # Download and save the image
            file_type = 'image'
            image_filename = download_and_save_file(image_link, 'images', title, folder_path, file_type)
            
            # Download and save the PDF file (if available)
            file_link = find_pdf_link(file_url)
            if file_link:
                pdf_filename = download_and_save_file(file_link, 'files', title, folder_path, book_file_type)
            else:
                pdf_filename = None
            
            # Fetch or create authors
            authors = [Author.objects.get_or_create(name=name)[0] for name in authors]
            # Fetch or create publisher
            publisher, _ = Publisher.objects.get_or_create(name=publisher)
            # Create book instance
            book = Book.objects.create(
                title=title,
                year=year,
                language=language,
                pages=pages,
                topic=topic,
                about_book=about_book,
                image_file_path=image_filename,
                book_file_path=pdf_filename,
            )
            # Add authors and publisher to the book
            book.author.add(*authors)
            book.publisher.add(publisher)

            # Save the search result
            SearchResult.objects.create(key_word=keyword_searched, book=book, link=url)

            print(f"Created Book: {book}")
        except Exception as e:
            print(e)


def remove_strings_in_parentheses(strings):
    # Define a regular expression pattern to match strings within parentheses
    pattern = r'\([^()]*\)'

    # Iterate over each string in the list
    for i in range(len(strings)):
        # Use re.sub() to replace matches of the pattern with an empty string
        strings[i] = re.sub(pattern, '', strings[i]).strip()

    return strings


def download_and_save_file(file_url, folder_name, book_title, folder_path, file_type):
    folder_path = os.path.join(folder_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    """
    Download a file from the given URL and save it in the specified folder with a sanitized file name.
    """
    try:
        # Determine the file extension based on the file type
        print(file_type)

        if file_type == 'image':
            file_extension = 'jpg'
        elif file_type == 'html':
            file_extension = 'html'
        else:
            file_extension = file_type

        # Sanitize the book title to remove any invalid characters
        sanitized_title = sanitize_filename(book_title)

        # Construct the file path with the book title and appropriate file extension
        file_path = os.path.join(folder_path, f"{sanitized_title}.{file_extension}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        # Check if the file already exists
        if os.path.exists(file_path):
            # Append a number to the file name to make it unique
            file_name = f"{sanitized_title}_1.{file_extension}"
            file_path = os.path.join(folder_path, file_name)
            i = 2
            # Keep incrementing the number until a unique file name is found
            while os.path.exists(file_path):
                file_name = f"{sanitized_title}_{i}.{file_extension}"
                file_path = os.path.join(folder_path, file_name)
                i += 1

        # Download the file
        if file_type != 'html':
            response = requests.get(file_url, headers)
        else:
            response = file_url

        # Save the file
        with open(file_path, 'wb+') as f:
            f.write(response.content)
    except Exception as e:
        print(e)

    return os.path.join(folder_name, f"{sanitized_title}.{file_extension}")


def sanitize_filename(filename):
    """
    Sanitize the filename by removing any characters that are not allowed in file names.
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-'))


def find_pdf_link(url):
    try:
        # Search for PDF links in the content
        response = requests.get(url, verify=False)
        print("status code:", response.status_code, "Fetching url:", url)
        content = BeautifulSoup(response.text, "html.parser")
        link = content.find('div', {'id': 'download'}).find_all('a')[0]['href']
        if link.endswith('.pdf'):
            return link
    except Exception as e:
        print(e)
    return None


'''
def zip_output_folder(output_folder):
    """
    Zip the output folder containing the generated reports.

    :param output_folder: The path of the folder to be zipped.
    :return: The path of the zipped file.
    """
    zip_filename = output_folder.split('\\')[1]
    shutil.make_archive(zip_filename, 'zip', base_dir=zip_filename, root_dir='media\\')
    shutil.move(f'{zip_filename}.zip', f'output\\{zip_filename}.zip')
    return f'output\\{zip_filename}'
'''
