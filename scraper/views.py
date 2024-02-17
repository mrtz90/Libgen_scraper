from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup
import re

from libgen.models import Author, Book, Publisher, SearchResult, KeyWordSearched


def scrape_form(request):
    if request.method == 'POST':
        key_word = request.POST.get('key_word')
        from_books = int(request.POST.get('from_books'))
        to_books = int(request.POST.get('to_books'))
        result = search_key_work(key_word, from_books, to_books)
        scrape_books(result)

        return HttpResponse("Scraping completed successfully!")
    else:
        return render(request, 'scrape_form.html')


def search_key_work(key_word, from_page, to_page):
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
    return links


def scrape_books(links):
    for link in links[0:5]:
        url = f'https://libgen.is/{link}'
        response = requests.get(url, verify=False)
        print("status code:", response.status_code, "Fetching url:", url)
        content = BeautifulSoup(response.text, "html.parser")
        trs = content.find('table').find_all('tr')
        image_link = 'https://libgen.rs' + trs[1].find('img')['src']
        title = trs[1].find_all('a')[1].text.strip()
        authors = remove_strings_in_parentheses(trs[10].find('b').text.split(','))
        publisher = trs[12].find_all('td')[1].text.strip()
        year = trs[13].find_all('td')[1].text.strip()
        language = trs[14].find_all('td')[1].text.strip()
        pages = trs[14].find_all('td')[3].text.strip()
        topic = trs[22].find_all('td')[1].text.strip()
        about_book = trs[31].find('td').text.strip()
        print(about_book)


def remove_strings_in_parentheses(strings):
    # Define a regular expression pattern to match strings within parentheses
    pattern = r'\([^()]*\)'

    # Iterate over each string in the list
    for i in range(len(strings)):
        # Use re.sub() to replace matches of the pattern with an empty string
        strings[i] = re.sub(pattern, '', strings[i]).strip()

    return strings
