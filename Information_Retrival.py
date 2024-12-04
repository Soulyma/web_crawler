import os
import json
import re
from urllib.parse import urlparse, urljoin, urldefrag
import requests
from bs4 import BeautifulSoup

class ArabicTitleCrawler:
    
    def __init__(self, start_url, desktop_path):
        self.urls_to_be_visited = [start_url]
        self.visited = set()
        self.domain = urlparse(start_url).scheme + "://" + urlparse(start_url).netloc
        self.docs = []
        self.desktop_path = desktop_path

    def clean_text(self, text):
        clean_text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        clean_text = ' '.join(clean_text.split())
        return clean_text.strip()

    def normalize_url(self, url):
        url, _ = urldefrag(url)
        parsed_url = urlparse(url)
        return parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    def is_arabic_content(self, text):
        arabic_characters = re.compile(r'[\u0600-\u06FF]')
        return bool(arabic_characters.search(text))

    def extract_content(self, soup):
     sections = []
     current_section = {"text": "", "section": ""}  
     for element in soup.find_all(
         ['div','h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'i', 'li']
         ):
        tag = element.name
        text = self.clean_text(element.get_text())
        print(f"Found text: {text} in tag: {tag}")
        if self.is_arabic_content(text):
            print(f"Arabic content detected: {text}")
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and text:
                if current_section["text"]:
                    sections.append(current_section)
                current_section = {"text": "", "section": text}
            elif tag in ['p', 'li', 'i'] and text:
                if current_section["text"]:
                    current_section["text"] += " " + text
                else:
                    current_section["text"] = text
     if current_section["text"]:
        sections.append(current_section)
     return sections if sections else None


    def crawl(self, link):
     try:
        normalized_link = self.normalize_url(link)
        if normalized_link in self.visited:
            print(f"Already visited: {normalized_link}")
            return
        response = requests.get(link)
        response.raise_for_status()
        if not '<html lang="ar"' in response.text.lower():
            print(f"Skipping non-Arabic page: {link}")
            return
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")
        cleaned_title = self.clean_text(title.text) if title else "بدون عنوان"
        main_content = soup.find("main") or soup.body
        content_sections = self.extract_content(main_content)
        if not content_sections:
            print(f"No relevant Arabic content found in {link}")
        else:
            print(f"Arabic content successfully extracted from {link}")
        self.docs.append({
            "Document ID": len(self.docs),
            "URL": normalized_link,
            "Title": cleaned_title,
            "Content": content_sections
        })
        self.visited.add(normalized_link)
        for url in soup.find_all("a", href=True):
            href = url['href']
            full_url = urljoin(self.domain, href)
            normalized_full_url = self.normalize_url(full_url)
            print(f"Checking URL: {normalized_full_url}") 
            if (normalized_full_url.startswith(self.domain)
                and normalized_full_url not in self.visited
                and normalized_full_url not in self.urls_to_be_visited):
                    self.urls_to_be_visited.append(normalized_full_url)
     except requests.RequestException as e:
        print(f"Error crawling {link}: {e}")
     except Exception as e:
        print(f"General error occurred: {e}")


    def start(self, max_pages=10):
        while self.urls_to_be_visited and len(self.visited) < max_pages:
            current_url = self.urls_to_be_visited.pop(0)
            self.crawl(current_url)

        print(f"Crawling finished. {len(self.docs)} pages crawled.")
        self.save_data()

    def save_data(self):
        file_path = os.path.join(self.desktop_path, 'crawled_data.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")


# To run the crawler:
start_url = 'url' # Path to the start CSV file
saving_path = 'path' # Path to the saving CSV file
crawler = ArabicTitleCrawler(start_url, saving_path)
crawler.start(max_pages=200)
