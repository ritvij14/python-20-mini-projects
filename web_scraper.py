from bs4 import BeautifulSoup
import requests


def get_url():
    while True:
        url = input("Enter the URL: ").strip()
        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            return url
        print("Please enter a valid URL.")


def fetch_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None


def parse_html(html_content):
    anchor_links = {}
    try:
        parsed_html = BeautifulSoup(html_content, "html.parser")
        anchor_elements = parsed_html.find_all("a")
        for element in anchor_elements:
            label = element.get("aria-label") or element.text.strip()
            href = element.get("href")
            if label and href:
                anchor_links[label] = href
    except Exception as e:
        print(f"Error parsing HTML: {e}")
    return anchor_links


def main():
    print("WEB SCRAPER")
    while True:
        url = get_url()
        html_content = fetch_webpage(url)
        if html_content:
            anchor_links = parse_html(html_content)
            print(f"Found {len(anchor_links)} links:\n")
            for label, href in anchor_links.items():
                print(f"- {label}: {href}")
        else:
            print("Failed to fetch the webpage.")

        choice = input("\nDo you want to continue? (y/n): ").strip().lower()
        if choice != "y":
            break


if __name__ == "__main__":
    main()
