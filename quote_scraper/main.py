import os
from scraper.scraper import scrape_all_data
from storage.json_writer import write_to_json

BASE_URL = 'https://quotes.toscrape.com'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    quotes, authors = scrape_all_data(BASE_URL)

    # Save data to JSON files in the output directory
    write_to_json(quotes, 'quotes.json')
    write_to_json(authors, 'authors.json')

if __name__ == '__main__':
    main()
