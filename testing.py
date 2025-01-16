import requests
import sys
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


def scrape_webpage(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the webpage using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and display the title of the webpage
        title = soup.title.string if soup.title else "no title found"
        print(f"Page Title: {title}")

        # Create a folder based on the site's domain name
        domain = urlparse(url).netloc  # Extract the domain name from the URL
        if not os.path.exists(domain):  # Check if the directory already exists
            os.makedirs(domain)  # Create the directory

        # Extract and display all links on the page
        print("\nLinks:")
        for link in soup.find_all("a", href=True):
            print(link["href"])

        # Extract and save all images
        print("\nDownloading Images:")
        for img in soup.find_all("img", src=True):
            img_url = img["src"]
            # Handle relative URLs
            if not img_url.startswith(("http://", "https://")):
                img_url = urlparse(url)._replace(path=img_url).geturl()

            try:
                # Extract the image filename
                img_filename = os.path.join(domain, os.path.basename(img_url))
                # Download and save the image
                urlretrieve(img_url, img_filename)
                print(f"Downloaded: {img_filename}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the HTTP request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python webscrapper_save_images.py <URL>")
    else:
        url = sys.argv[1]
        scrape_webpage(url)
