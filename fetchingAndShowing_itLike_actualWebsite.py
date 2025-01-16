import requests
from bs4 import BeautifulSoup
import sys


def fetch_and_display_content(url):


    try:
        response = requests.get(url)
        print(f"HTTP status code {response.status_code}")
        

        soup = BeautifulSoup(response.text, "html.parser") 

        visible_text = soup.get_text()

        print("cleaned website content\n")
        print(visible_text.strip())

    except requests.exceptions.RequestException as e:
        print(f"An Error occurred: {e}")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("use python fetch.py <url>")

    else:
        url=sys.argv[1]


        fetch_and_display_content(url)