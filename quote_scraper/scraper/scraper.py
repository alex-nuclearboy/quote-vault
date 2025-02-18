import requests
from bs4 import BeautifulSoup

from utils.utils import extract_text, parse_date

BASE_URL = 'https://quotes.toscrape.com'


def fetch_quotes(soup, authors_urls):
    quotes = []

    for quote in soup.find_all('div', class_='quote'):
        text = extract_text(quote.find('span', class_='text'))
        author = extract_text(quote.find('small', class_='author'))
        author_url = BASE_URL + quote.find('a')['href']
        tags = [
                extract_text(tag)
                for tag in quote.find_all('a', class_='tag')
                if tag.text.strip()  # Filter out empty tags
            ]
        if author not in authors_urls:
            authors_urls[author] = author_url
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes


def fetch_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = extract_text(soup.find('h3', class_='author-title'))
    birth_date = parse_date(
                extract_text(
                    soup.find('span', class_='author-born-date')
                )
            )
    birth_location = extract_text(soup.find('span', class_='author-born-location'))
    description = extract_text(soup.find('div', class_='author-description'))

    return {
        "fullname": fullname,
        "birth_date": birth_date,
        "birth_location": birth_location,
        "description": description
    }


def scrape_all_data(initial_url):
    quotes = []
    authors_urls = {}
    url = initial_url

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes += fetch_quotes(soup, authors_urls)

        next_btn = soup.find('li', class_='next')
        if next_btn:
            url = initial_url + next_btn.find('a')['href']
        else:
            url = None

    authors_details = [
        fetch_author_details(url) for url in authors_urls.values()
    ]

    return quotes, authors_details

