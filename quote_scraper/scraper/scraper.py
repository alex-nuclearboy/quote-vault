import requests
from bs4 import BeautifulSoup

from utils.date_processor import parse_date
from utils.text_processor import extract_text
from utils.url_processor import extract_url, get_next_page_url


def fetch_quotes(soup, base_url):
    quotes = []

    for quote in soup.find_all('div', class_='quote'):
        text = extract_text(
            quote.find('span', class_='text'), 'No text available'
        )
        author = extract_text(
            quote.find('small', class_='author'), 'Unknown Author'
        )
        author_link_tag = quote.find('a')
        if author_link_tag:
            author_url = extract_url(
                author_link_tag, 'href', base_url=base_url
            )
        tags = [
                extract_text(tag)
                for tag in quote.find_all('a', class_='tag')
                if tag.text.strip()  # Filter out empty tags
            ]
        quotes.append({
            'text': text,
            'author': author,
            'author_url': author_url,
            'tags': tags
        })

    return quotes


def fetch_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = extract_text(
        soup.find('h3', class_='author-title'), 'Unknown Author'
    )
    birth_date = parse_date(
                extract_text(
                    soup.find('span', class_='author-born-date')
                )
            )
    birth_location = extract_text(
        soup.find('span', class_='author-born-location'), 'Unknown Location'
    )
    bio = extract_text(
        soup.find('div', class_='author-description'), 'No bio available'
    )

    return {
        "fullname": fullname,
        "birth_date": birth_date,
        "birth_location": birth_location,
        "bio": bio
    }


def scrape_page_data(base_url, page_url, fetched_authors):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    quotes = fetch_quotes(soup, base_url)

    authors_urls = {
        quote['author_url'] for quote in quotes if quote['author_url']
        and quote['author_url'] not in fetched_authors
    }

    authors_details = [fetch_author_details(url) for url in authors_urls]

    fetched_authors.update(authors_urls)

    return quotes, authors_details


def scrape_all_data(base_url):
    all_quotes = []
    all_authors_details = []
    fetched_authors = set()
    current_url = base_url

    while current_url:
        quotes, authors_details = scrape_page_data(base_url, current_url,
                                                   fetched_authors)
        all_quotes.extend(quotes)
        all_authors_details.extend(authors_details)

        next_url = get_next_page_url(
            current_url, base_url, ['li.next a'], 'href'
        )
        current_url = next_url

    return all_quotes, all_authors_details
