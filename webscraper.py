import requests
import sys
from bs4 import BeautifulSoup


def scrape_webpage(url):
    try:

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        title= soup.title.string if soup.title else "no title found"
        print(f"Page Title: {title}")

        print("\nLinks:")

        for link in soup.find_all("a",href=True):
            print(link["href"])
        
        print("\nImages:")

        for img in soup.find_all("img", src=True):
            print(img["src"])
    except requests.exceptions.RequestException as e:

        print(f"an error occured :{e}")

if __name__=="__main__":
    
    if len(sys.argv) < 2:
        print("usage:python fetch.py <url>")

    else:
        url= sys.argv[1]

        scrape_webpage(url)