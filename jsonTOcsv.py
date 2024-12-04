import json
import csv
import os

def json_to_csv(json_file_path, output_csv_path, delimiter=';', quotechar='"'):
    """
    Converts a JSON file to a CSV file with proper UTF-8 encoding.

    Parameters:
    - json_file_path (str): Path to the input JSON file.
    - output_csv_path (str): Path to the output CSV file.
    - delimiter (str): Delimiter to use in the CSV file. Default is ';'.
    - quotechar (str): Quote character for CSV. Default is '"'.

    Returns:
    - None
    """
    if not os.path.exists(json_file_path):
        print(f"Error: JSON file at {json_file_path} does not exist.")
        return
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return

    with open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)

        # Define headers
        headers = ["Document ID", "URL", "Title", "text", "section"]
        csv_writer.writerow(headers)

        # Write data to CSV
        for doc in json_data:
            doc_id = doc.get("Document ID", "")
            url = doc.get("URL", "")
            title = doc.get("Title", "")
            
            for content in doc.get("Content", []):
                text = content.get("text", "")
                section = content.get("section", "")

                csv_writer.writerow([doc_id, url, title, text, section])

    print(f"Data successfully written to {output_csv_path}")

# Example usage:
json_data_path = "crawled_data.json"  # Path to the input JSON file
output_csv_path = "crawled_data.csv"  # Path to the output CSV file
json_to_csv(json_data_path, output_csv_path)
