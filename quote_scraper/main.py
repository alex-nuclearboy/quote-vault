import os
from scraper.scraper import scrape_all_data
from storage.json_writer import write_to_json

BASE_URL = 'https://quotes.toscrape.com'
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    quotes, authors = scrape_all_data(BASE_URL)

    # Ensure the output directory exists
    ensure_directory_exists(OUTPUT_DIR)

    # Save data to JSON files in the output directory
    write_to_json(quotes, os.path.join(OUTPUT_DIR, 'quotes.json'))
    write_to_json(authors, os.path.join(OUTPUT_DIR, 'authors.json'))

if __name__ == '__main__':
    main()
