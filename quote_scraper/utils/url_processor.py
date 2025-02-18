from urllib.parse import urljoin, urlparse


def extract_url(tag, attribute = 'href', default = None, base_url = None):
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
