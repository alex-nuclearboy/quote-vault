import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def extract_url(tag, attribute='href', default=None, base_url=None):
    if not tag or not tag.has_attr(attribute):
        return default

    url = tag.get(attribute)

    if not url:
        return default

    if base_url and not urlparse(url).netloc:
        url = urljoin(base_url, url)  # Add the base URL to the relative one

    return url if is_valid_url(url) else default


def is_valid_url(url):
    if not url:
        return False

    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def get_next_page_url(current_url, base_url, selectors=None, attribute='href'):
    if selectors is None:
        selectors = ['li.next a', 'a.next_page']

    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Try fetching the next URL from the selectors
    next_url = find_next_url(soup, selectors, current_url, base_url, attribute)
    if next_url:
        return next_url

    return None


def find_next_url(soup, selectors, current_url, base_url, attribute):
    for selector in selectors:
        next_element = soup.select_one(selector)
        if next_element:
            next_url = extract_url(
                next_element, attribute, default=None, base_url=base_url
            )
            if next_url and next_url != current_url:
                return next_url
    return None
