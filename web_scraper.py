import os
import re
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
        self.overall_progress = None
        with requests.Session() as self.session:
            self.executor = ThreadPoolExecutor(max_workers=5)
    
    def update_overall_progress(self):
        if self.overall_progress:
            self.overall_progress.update(1)

    def download_file(self, url, local_path):
        response = self.session.get(url, stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

    def process_links(self, current_url, soup, url_queue, visited_urls):
        # Process links within the HTML content
        # Update their 'href' attributes to point to local paths
        # Add them to the queue for further processing
        all_links = soup.find_all('a')
        other_links = [link for link in all_links if link.get_text() not in ['next', 'previous', 'Home']]
        for link in other_links:
            href = link.get('href')
            if href:
                local_link = get_output_path(self.output_dir, urljoin(current_url, href))
                create_directory_if_not_exists(os.path.dirname(local_link))
                rel_path = os.path.relpath(local_link, self.output_dir)
                if 'page-' in current_url:
                    rel_path = rel_path.replace('catalogue/', '')
                link['href'] = rel_path
                if local_link not in visited_urls and local_link not in url_queue:
                    url_queue.append(local_link)

    def process_navigation_links(self, soup, current_url, visited_urls, url_queue):
        # Process 'next' and 'previous' navigation links
        all_links = soup.find_all('a')
        nav_links = [link for link in all_links if link.get_text() in ['next', 'previous']]
        for link in nav_links:
            href = link.get('href')
            text = link.text
            if href:
                local_link = get_output_path(self.output_dir, urljoin(current_url, href))
                rel_path = os.path.relpath(local_link, self.output_dir)
                if 'page-' in current_url:
                    rel_path = rel_path.replace('catalogue/', '')
                if 'page-2.html' in current_url and text == 'previous':
                    rel_path = '../index.html'
                link['href'] = rel_path
                if local_link not in visited_urls and local_link not in url_queue:
                    url_queue.append(local_link)
    
    def process_home_link(self, soup, current_url, visited_urls, url_queue):
        # Process 'Home' link
        all_links = soup.find_all('a')
        home_links = [link for link in all_links if link.get_text() == 'Home']
        for link in home_links:
            href = link.get('href')
            if href:
                local_link = get_output_path(self.output_dir, urljoin(current_url, href))
                rel_path = os.path.relpath(local_link, self.output_dir)
                if 'page-' in current_url:
                    rel_path = '../' + rel_path
                link['href'] = rel_path
                if local_link not in visited_urls and local_link not in url_queue:
                    url_queue.append(local_link)

    def process_images(self, soup):
        # Process and download images
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = urljoin(self.base_url, img.get('src'))
            img_path = get_output_path(self.output_dir, img_url)
            create_directory_if_not_exists(os.path.dirname(img_path))
            self.download_file(img_url, img_path)
    
    def process_container_divs(self, soup, visited_urls):
        # Process and download book-related content
        book_divs = soup.find_all("div", {"class": "image_container"})
        for book in book_divs:
            link = book.find('a')
            if link:
                href = link.get('href')
                if not href.startswith('catalogue/'):
                    href = 'catalogue/' + href
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url in visited_urls:
                        continue
                    visited_urls.add(full_url)
                    page_path = get_output_path(self.output_dir, full_url)
                    create_directory_if_not_exists(os.path.dirname(page_path))
                    self.download_file(full_url, page_path)

    def process_side_categories(self, soup, visited_urls):
        # Process and download side categories content
        href_list = []
        side_categories_divs = soup.find_all("div", {"class": "side_categories"})
        for side_categories_div in side_categories_divs:
            nested_ul_elements = side_categories_div.find_all('ul', recursive=False)
            for ul_element in nested_ul_elements:
                li_elements = ul_element.find_all('li', recursive=False)
                for li_element in li_elements:
                    href = li_element.a['href']
                    if href:
                        href_list.append(href)
                    ul_elements = li_element.find_all('ul', recursive=False)
                    for ule in ul_elements:
                        lie_list = ule.find_all('li', recursive=False)
                        for li in lie_list:
                            link = li.find('a')
                            if link:
                                href = link.get('href')
                                if href:
                                    href_list.append(href)
                                    
        for href in href_list:
            full_url = urljoin(self.base_url, href)
            if full_url in visited_urls:
                continue
            visited_urls.add(full_url)
            page_path = get_output_path(self.output_dir, full_url)
            create_directory_if_not_exists(os.path.dirname(page_path))
            self.download_file(full_url, page_path)

    def scrape_website(self, url):
        visited_urls = set()
        url_queue = [url]
        page_progress = None
        total_pages = 0

        while url_queue:
            current_url = url_queue.pop(0)
            self.update_overall_progress()
            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)

            if page_progress is None:
                page_progress = tqdm(desc=f"Processing Page: {current_url}", dynamic_ncols=True)
            page_progress.set_description(f"Processing Page: {current_url}")

            if current_url.startswith('http') or current_url.startswith('https'):
                # Only process valid URLs, not local file paths
                page_progress.update(1)
                response = self.session.get(current_url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page_path = get_output_path(self.output_dir, current_url)
                    create_directory_if_not_exists(os.path.dirname(page_path))

                    if total_pages == 0:
                        page_link = soup.find('li', class_='current')
                        total_pages = int(re.findall(r'\d+', page_link.get_text())[-1])
                        self.overall_progress.total = total_pages

                    futures = []

                    # Submit each task to the ThreadPoolExecutor
                    futures.append(self.executor.submit(self.process_images, soup))
                    futures.append(self.executor.submit(self.process_navigation_links, soup, current_url, visited_urls, url_queue))
                    futures.append(self.executor.submit(self.process_home_link, soup, current_url, visited_urls, url_queue))
                    futures.append(self.executor.submit(self.process_container_divs, soup, visited_urls))
                    futures.append(self.executor.submit(self.process_side_categories, soup, visited_urls))
                    # futures.append(self.executor.submit(self.process_links, current_url, soup, url_queue, visited_urls))

                    # Wait for all tasks to complete
                    for future in futures:
                        future.result()


                    with open(page_path, 'w', encoding='utf-8') as file:
                        file.write(soup.prettify())

                    # Check for the "Next" link and navigate to the next page
                    next_link = soup.find('li', class_='next')
                    if next_link:
                        if 'catalogue' in next_link.a['href']:
                            next_url = urljoin(self.base_url, next_link.a['href'])
                        else:
                            if next_link.a['href'].startswith('../'):
                                next_url = urljoin(self.base_url, 'catalogue/' + next_link.a['href'][3:])
                            else:
                                next_url = urljoin(self.base_url, 'catalogue/' + next_link.a['href'])
                        url_queue.append(next_url)
                        self.update_overall_progress()
                page_progress.close()
                page_progress = None

    def start_scraping(self):
        create_directory_if_not_exists(self.output_dir)
        with tqdm(total=1, desc="Overall Progress", dynamic_ncols=True) as self.overall_progress:
            self.scrape_website(self.base_url)
        self.overall_progress.close()
        print(f"Scraping completed! \nFiles are saved in the '{self.output_dir}' directory.")
