import requests
import sys

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def scrape_webpage(url, visited, max_depth=20):
    try:
        response= requests.get(url)

        response.raise_for_status()
        soup=BeautifulSoup(response.text,"html.parser")


        title= soup.title.string if soup.title else "no title found"
        print(f"\nPage title:{title} \nURL: {url}")

        print("\nLinks")
        links = []

        for link in soup.find_all("a", href=True):
            full_url= urljoin(url,link["href"])
            print(full_url)
            links.append(full_url)
            
        print("\nImages:")
        for img in soup.find_all("img",src=True):
            img_url = urljoin(url,img["src"])
            print(img_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f"an error occured :{e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch.py <URL>")

    else:
        start_url = sys.argv[1]
        visited = set()
        queue = deque([start_url])
        depth = 0

        while queue and depth < 20:
            current_url = queue.popleft()

            if current_url in visited:
                continue

            visited.add(current_url)
            print(f"\n [Depth {depth} Scraping:{current_url}]")

            found_links = scrape_webpage(current_url, visited)

            for link in found_links:
                if link not in visited:
                    queue.append(link)

            depth += 1
                