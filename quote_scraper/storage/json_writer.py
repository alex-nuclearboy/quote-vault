import json

def write_to_json(data, filename):
    """
    Write data to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")
