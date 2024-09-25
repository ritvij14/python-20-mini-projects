import multiprocessing.process
from multiprocessing import Queue
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import multiprocessing
from urllib.parse import urljoin, urlparse
import time
import json


def fetch_url(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "Sample_Crawler/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_html(html_content: str, base_url: str):
    anchor_links = {}
    try:
        parsed_html = BeautifulSoup(html_content, "html.parser")
        anchor_elements = parsed_html.find_all("a")
        for element in anchor_elements:
            label = element.get("aria-label") or element.text.strip()
            href = element.get("href")
            if label and href:
                full_url = urljoin(base_url, href)
                anchor_links[label] = full_url
    except Exception as e:
        print(f"Error parsing HTML: {e}")
    return anchor_links


def crawl_worker(url_queue: Queue, result_queue: Queue, max_depth: int):
    while not url_queue.empty():
        current_url, current_depth = url_queue.get()

        if current_depth > max_depth:
            continue

        html_content = fetch_url(current_url)
        if html_content:
            parsed_links = parse_html(html_content, current_url)

            result_queue.put({current_url: parsed_links})

            for link in parsed_links.values():
                url_queue.put((link, current_depth + 1))



def run_parallel_crawler(start_urls: list, max_depth: int, num_workers: int):
    url_queue = Queue()
    for item in start_urls:
        url_queue.put((item, max_depth))

    visited_urls = set()

    result_queue = Queue()

    workers = []
    for _ in range(num_workers):
        worker = multiprocessing.Process(target=crawl_worker, args=(url_queue, result_queue, max_depth))
        workers.append(worker)
        worker.start()

    collected_data = {}
    
    # Manage the crawling process
    while any(worker.is_alive() for worker in workers):
        # Process results
        while not result_queue.empty():
            result = result_queue.get()
            for url, links in result.items():
                visited_urls.add(url)
                collected_data[url] = links

        # Rate limiting
        time.sleep(0.1)  # Adjust as needed

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

    # Process any remaining results
    while not result_queue.empty():
        result = result_queue.get()
        for url, links in result.items():
            visited_urls.add(url)
            collected_data[url] = links

    # Final processing of collected data
    print(f"Crawled {len(visited_urls)} unique URLs")
    print(f"Collected data for {len(collected_data)} pages")

    # You could save collected_data to a file here if needed

    return collected_data


if __name__ == "__main__":
    start_urls = ["http://books.toscrape.com/"]
    max_depth = 3
    num_workers = 4

    results = run_parallel_crawler(start_urls, max_depth, num_workers)

    print(f"Crawl Summary:")
    print(f"Starting URLs: {start_urls}")
    print(f"Max Depth: {max_depth}")
    print(f"Number of Workers: {num_workers}")
    print(f"Total URLs crawled: {len(results)}")

    # Calculate total links found
    total_links = sum(len(links) for links in results.values())
    print(f"Total links found: {total_links}")

    # Display a sample of the results
    print("\nSample of crawled pages:")
    for url, links in list(results.items())[:5]:  # Show first 5 results
        print(f"\nURL: {url}")
        print(f"Number of links found: {len(links)}")
        print("Sample links:")
        for label, link in list(links.items())[:3]:  # Show first 3 links
            print(f"  - {label}: {link}")

    # Optionally, save full results to a file
    import json
    with open('crawler_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nFull results saved to 'crawler_results.json'")