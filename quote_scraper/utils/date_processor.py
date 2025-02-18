from datetime import datetime

def parse_date(date_str, input_format='%B %d, %Y', output_format='%Y-%m-%d'):
    try:
        return datetime.strptime(date_str, input_format).strftime(output_format)
    except ValueError:
        return None
