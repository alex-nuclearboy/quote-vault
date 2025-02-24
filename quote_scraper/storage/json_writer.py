import os
import json

from utils.logger import setup_logger

logger = setup_logger(__name__)

# Define the path to the 'data' folder
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../..', 'data'
)


def ensure_directory_exists(directory):
    """Ensure the 'data' folder exists, create it if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_json(data, filename):
    """
    Write data to a JSON file.
    """
    ensure_directory_exists(OUTPUT_DIR)

    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        if 'quotes' in filename:
            logger.info(
                f"{len(data)} quotes successfully written to {file_path}."
            )
        elif 'authors' in filename:
            logger.info(
                f"{len(data)} authors successfully written to {file_path}."
            )
        else:
            logger.info(f"Data successfully written to {file_path}.")
    except Exception as e:
        logger.info(f"Error writing to {filename}: {e}")
