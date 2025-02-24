from datetime import datetime

from utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_date(date_str, input_format='%B %d, %Y', output_format='%Y-%m-%d'):
    try:
        return (
            datetime.strptime(date_str, input_format).strftime(output_format)
        )
    except ValueError as e:
        logger.error(f"Error parsing date '{date_str}': {e}")
        return None
