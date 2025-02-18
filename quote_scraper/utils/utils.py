import re
from datetime import datetime
from bs4 import Tag, BeautifulSoup

def extract_text(tag):
    if tag:
        # Join stripped strings and clean spaces around punctuation marks
        text = ' '.join(tag.stripped_strings)

        # Remove surrounding quotes (both standard and fancy quotes)
        text = re.sub(r'^[“"]|[”"]$', '', text)

        # Clean unnecessary spaces before punctuation marks
        text = re.sub(r'\s([.,;!?])', r'\1', text)

        return text
    return ''


def parse_date(date_string, date_format = "%B %d, %Y"):
    try:
        return (
            datetime.strptime(date_string.strip(), date_format)
            .strftime("%Y-%m-%d")
        )
    except ValueError:
        return None