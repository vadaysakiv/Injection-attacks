import requests
import sys
import time

from bs4 import BeautifulSoup

from urllib.parse import urljoin 
from collections import deque

import re


def clean_title(title):


    return re.sub(r'[\\*/?:"<>|]', "", title)


#Main function to scrape a webpage

def scrape_webpage(url, visited, max_depth=20):


    try:
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


         
        response= requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup= BeautifulSoup(response.text, "html.parser")  
        
        title = soup.title.string if soup.title else "no title found"
        title_cleaned = clean_title(title)


        links = []

        with open(f"{title_cleaned}_links.txt", "w", encoding="utf-8") as links_file:
            print("\nLinks:")
            for link in soup.find_all("a",href=True):
                full_url = urljoin(url, link["href"])
                print(full_url)
                links_file.write(full_url + "\n")                
                links.append(full_url)

        with open(f"{title_cleaned}_images.txt", "w", encoding="utf-8") as images_file:
            print("\nImages:")
            for img in soup.find_all("img",src=True):
                img_url = urljoin(url, img["src"])
                print(img_url)
                images_file.write(img_url + "\n")
                

        return links

    except requests.exceptions.RequestException as e:
        print(f"an error occured :{e}") 
        return []


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage:python  filename.py <url>")

    else:
        start_url = sys.argv[1]
        visited = set()
        depth_ini = 0
        queue = deque([start_url])

        while queue and depth_ini < 20:
            current_url = queue.popleft()
            if current_url in visited:
                continue

            visited.add(current_url)
            print(f"\n [Depth {depth_ini} Scraping:{current_url}]")
            found_links = scrape_webpage(current_url, visited)

            for link in found_links:
                if link not in visited:
                    queue.append(link)

            depth_ini += 1
            time.sleep(2)

        