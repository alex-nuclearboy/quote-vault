import re

def extract_text(tag, default = ''):
    if tag:
        # Join stripped strings and clean spaces around punctuation marks
        text = ' '.join(tag.stripped_strings)

        # Remove surrounding quotes (both standard and fancy quotes)
        text = re.sub(r'^[“"]|[”"]$', '', text)

        # Clean unnecessary spaces before punctuation marks
        text = re.sub(r'\s([.,;!?])', r'\1', text)

        return text
    return default
