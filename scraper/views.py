import os
from datetime import datetime
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup
import re
import urllib3

from libgen.models import Author, Book, Publisher, SearchResult, KeyWordSearched


def scrape_form(request):
    if request.method == 'POST':
        key_word = request.POST.get('key_word')
        from_books = int(request.POST.get('from_books'))
        to_books = int(request.POST.get('to_books'))

        # Save the keyword searched
        keyword_searched = KeyWordSearched.objects.create(key_word=key_word)
        result = search_key_word(key_word, from_books, to_books)

        # Create a folder for images
        print(datetime.now().astimezone())
        folder_path = os.path.join(settings.MEDIA_ROOT, key_word + '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        os.makedirs(folder_path, exist_ok=True)

        scrape_books(result, keyword_searched, folder_path)

        return HttpResponse("Scraping completed successfully!")
    else:
        return render(request, 'scrape_form.html')


def search_key_word(key_word, from_page, to_page):
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
            topic = trs[22].find_all('td')[1].text.strip()
            about_book = trs[31].find('td').text.strip()

            # Save the html file
            download_and_save_file(response, 'html', title, folder_path, 'html')
            # Download and save the image
            file_type = 'image'
            image_filename = download_and_save_file(image_link, 'images', title, folder_path, file_type)

            # Download and save the PDF file (if available)
            pdf_link = find_pdf_link(file_url)
            if pdf_link:
                file_type = 'pdf'
                pdf_filename = download_and_save_file(pdf_link, 'pdfs', title, folder_path, file_type)
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
    try:
        # Determine the file extension based on the file type
        print(file_type)
        if file_type == 'pdf':
            file_extension = 'pdf'
        elif file_type == 'image':
            file_extension = 'jpg'
        elif file_type == 'html':
            file_extension = 'html'
        else:
            raise ValueError("Invalid file type. Supported types are 'pdf' and 'image'.")

        # Construct the file path with the book title and appropriate file extension
        file_path = os.path.join(folder_path, f"{book_title}.{file_extension}")

        # Download the file
        if file_type != 'html':
            response = requests.get(file_url)
        else:
            response = file_url

        # Save the file
        with open(file_path, 'wb+') as f:
            f.write(response.content)
    except Exception as e:
        print(e)

    return os.path.join(folder_name, f"{book_title}.{file_extension}")


def find_pdf_link(url):
    # Search for PDF links in the content
    response = requests.get(url, verify=False)
    print("status code:", response.status_code, "Fetching url:", url)
    content = BeautifulSoup(response.text, "html.parser")
    link = content.find('div', {'id': 'download'}).find_all('a')[2]['href']
    if link.endswith('.pdf'):
        return link
    return None
