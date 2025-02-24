import requests
from bs4 import BeautifulSoup

from utils.date_processor import parse_date
from utils.text_processor import extract_text
from utils.url_processor import extract_url, get_next_page_url
from utils.logger import setup_logger

logger = setup_logger(__name__)


def fetch_quotes(soup, base_url):
    logger.info("Fetching quotes from the page...")
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

    logger.info(f"Extracted {len(quotes)} quotes")
    return quotes


def fetch_author_details(author_url):
    try:
        response = requests.get(author_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching author details from {author_url}: {e}")
        return None

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

    logger.info(f"Fetched details for author {fullname}")

    return {
        "fullname": fullname,
        "birth_date": birth_date,
        "birth_location": birth_location,
        "bio": bio
    }


def scrape_page_data(base_url, page_url, fetched_authors):
    try:
        response = requests.get(page_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching page {page_url}: {e}")
        return [], []

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
    logger.info(f"Starting scraping from {base_url}")
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
        if next_url:
            logger.info(f"Fetching next page: {next_url}")
            current_url = next_url
        else:
            logger.info("No more pages to fetch.")
            break

    return all_quotes, all_authors_details
