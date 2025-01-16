import requests
import sys
import time 
from bs4 import BeautifulSoup

from urllib.parse import urljoin
from collections import deque

import re
import os
 

def clean_title(title):
    return re.sub(r'\\*//:"<>/|]', "", title)


def scrape_webpage(url, visited, images_set):
    try:
         headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\nScrapping: {url}")

        for link in soup.find_all("a",href = True):
            full_url  = urljoin(url,link["href"])
            if full_url not in links_set:
                links_set.add(full_url)

        for img in soup.find_all("img",src = True):
            img_url = urljoin(url,img["src"])
            if img_url not in images_set:
                images_set.add(img_url)

        return True

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage python filename.py <url>")
    
    else:
        start_url = sys.argv[1]

        visited = set()
        links_set = set()
        images_set = set()

        queue = deque([start_url])
        depth = 0 
        max_depth = 20

        output_folder = "scrapped_data"
        os.makedirs(output_folder, exist_ok=True)


        while queue and depth < max_depth:

            current_url = queue.popleft()

            if current_url in visited:
                continue

            visited.add(current_url)
            print(f"[Depth {depth} Scraping: {current_url}]")

            if scrape_webpage(current_url, visited, links_set, images_set):
                    for link in links_set:
                        if link not in visited:
                            queue.append(link)

            depth += 1
            time.sleep(2)

        links_file_path = os.path.join(output_folder, "all_links.txt")
        with open(links_file_path, "w", encoding="utf-8") as links_file:
            for link in links_set:
                links_file.write(link + "\n")

        images_file_path = os.path.join(output_folder, "all_images.txt")
        with open(images_file_path, "w", encoding="utf-8") as images_file:
            for image in images_set:
                images_file.write(image + "\n")

        print(f"\nScrapping complete. Result saved in the '{output_folder}' folder.")    