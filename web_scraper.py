import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import BASE_URL, OUTPUT_DIR
from utils import create_directory_if_not_exists, get_output_path

class WebScraper:
    def __init__(self):
        self.base_url = BASE_URL
        self.output_dir = OUTPUT_DIR
        with requests.Session() as self.session:
            self.executor = ThreadPoolExecutor(max_workers=5)

    def download_file(self, url, local_path):
        response = self.session.get(url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    def download_page(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_path = get_output_path(self.output_dir, url)
            create_directory_if_not_exists(os.path.dirname(page_path))

            # Add a base tag to set the base URL for relative links
            base_tag = soup.new_tag("base", href=url)
            soup.head.insert(0, base_tag)

            with open(page_path, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

            img_tags = soup.find_all('img')
            for img in img_tags:
                img_url = urljoin(self.base_url, img.get('src'))
                img_path = get_output_path(self.output_dir, img_url)
                create_directory_if_not_exists(os.path.dirname(img_path))
                self.download_file(img_url, img_path)

    def scrape_website(self, url):
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(self.base_url, a['href']) for a in soup.find_all('a')]
            
            with tqdm(total=len(links), desc="Scraping Progress") as pbar:
                for link in links:
                    self.executor.submit(self.download_page, link)
                    pbar.update(1)

    def start_scraping(self):
        create_directory_if_not_exists(self.output_dir)
        self.scrape_website(self.base_url)
        print(f"Scraping completed. Files are saved in the '{self.output_dir}' directory.")
