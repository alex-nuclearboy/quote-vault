import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


def extract_text(tag, default=''):
    if tag:
        # Join stripped strings and clean spaces around punctuation marks
        text = ' '.join(tag.stripped_strings)

        # Remove surrounding quotes (both standard and fancy quotes)
        text = re.sub(r'^[“"]|[”"]$', '', text)

        # Clean unnecessary spaces before punctuation marks
        text = re.sub(r'\s([.,;!?])', r'\1', text)

        return text

    logger.warning("Tag is None. Returning default text.")
    return default
