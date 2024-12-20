# Arabic Web Content Crawler
### Overview
This project provides tools to crawl web pages, extract Arabic content, and convert the extracted data into structured formats like JSON and CSV. It is designed for researchers, data analysts, and developers working with Arabic datasets and content analysis.

### The project includes:

- A Web Crawler: Extracts Arabic content from a given website.
- Data Conversion Tool: Converts the crawled JSON data into CSV format for further analysis.

### Features

**Web Crawler:**
 Crawls a specified website starting from a given URL.
 Extracts Arabic content and organizes it into structured sections based on headings and paragraphs.
 Saves the extracted content into a JSON file.

**Data Converter:**
 Converts the crawled JSON data into a CSV file.
 Ensures proper encoding (UTF-8 with BOM) for compatibility with tools like Excel.
 Includes structured headers such as "Document ID", "URL", "Title", "Section", and "Text".

**Prerequisites**
 - Python Version: Python 3.8 or higher.
 - beautifulsoup4
 - requests

### Example Output:
 The crawler saves the extracted data to crawled_data.json in the specified directory.
 
 **Example JSON Structure**
```json
[
  {
    "Document ID": 1,
    "URL": "https://example.com/article1",
    "Title": "عنوان المقالة",
    "Content": [

      {
        "section": "المقدمة",
        "text": "هذه فقرة تتحدث عن الموضوع."
      },
      {
        "section": "الخاتمة",
        "text": "هذه فقرة تلخص الموضوع."
     },
     ...
    ]
   ...
  }
]
```

The converter saves the data to crawled_data.csv in the specified directory.
**Example CSV Structure**
| Document ID | URL                        | Title            | Section     | Text                         |
|-------------|----------------------------|------------------|-------------|------------------------------|
| 1           | https://example.com/article1 | عنوان المقالة   | المقدمة      | هذه فقرة تتحدث عن الموضوع.   |

