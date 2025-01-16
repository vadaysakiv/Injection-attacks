import requests

import sys

def fetch_website_requests(url, search_string):


    try:
        response = requests.get(url)
        print(f"HTTP status code:{response.status_code}")
        print(f"Header of the url:\n{response.headers}")


        content=response.text
        print("Searching for the string in the source code...")

        lines=content.splitlines()
        found=False

        for line_num, line in enumerate(lines,start=1):
            if search_string in line:
                print(f"String '{search_string}' found on the line{line_num}:{line.strip()}")
                found=True
        if not found:
            print(f"String '{search_string}' not found in the source code.")

    except requests.exceptions.RequestException as e:

        print(f"An error occurred: {e}")



if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("usage:python fetch.py <url> <string to search>")

    else:

        url = sys.argv[1]
        search_string =sys.argv[2]

        fetch_website_requests(url,search_string)