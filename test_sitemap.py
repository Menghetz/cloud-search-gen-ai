from overrides import CustomSitemapLoader
from langchain.document_loaders.sitemap import SitemapLoader

import requests
import time
import math
import asyncio



# Constants for retrying and backoff
NUM_RETRIES = 10
BACKOFF_FACTOR = 1
MAX_DOCS = 50

def get_docs(url, max_items_percentage):
    # Variables to track if all URLs are parsed
    all_urls_parsed = False
    final_docs = []
    error_urls = []
    scrapping_factor = float(max_items_percentage)/100.0
    # Initialize SitemapLoader with web path (URL)
    sitemap_loader = CustomSitemapLoader(web_path=url, scrapping_factor = scrapping_factor)
    # Continue until all URLs are parsed
    while not all_urls_parsed:
        sitemap_loader.requests_per_second = 10
        sitemap_loader.raise_for_status = True
        # Retry the web request if there is an error
        for retry_num in range(NUM_RETRIES):
            mode = 'RETRY' if retry_num > 0 else 'INITIAL'
            time_to_sleep = BACKOFF_FACTOR * (2 ** (retry_num - 1))
            try:
                initial_docs = sitemap_loader.load(mode)
                if len(initial_docs) != len(error_urls) and len(error_urls) > 1:
                    raise requests.exceptions.HTTPError
                break
            except requests.exceptions.HTTPError:
                # Retry with exponential backoff if there is an error
                time.sleep(time_to_sleep)
                pass
            except requests.exceptions.ConnectionError:
                print("Invalid website")
        # Filter out documents with error content and append to the final list
        final_docs.extend([doc for doc in initial_docs if doc.page_content !=
                          '429 Too Many Requests\nYou have sent too many requests in a given amount of time.\n\n'])
        # Update error URLs for retry
        error_urls = [doc.metadata['source'] for doc in initial_docs if doc.page_content ==
                      '429 Too Many Requests\nYou have sent too many requests in a given amount of time.\n\n']
        # Check if all URLs are parsed, if not, continue retrying
        all_urls_parsed = True if len(error_urls) == 0 else False
        sitemap_loader.filter_urls = error_urls
    
    if len(final_docs) > MAX_DOCS:
        print(f"Embedding {len(final_docs)} documents may take a long time. Reduce the % of website to scrapped to less than {math.floor(MAX_DOCS*100/ len(final_docs))} %")
    return final_docs

asyncio.run(get_docs("https://www.sirmax.com/en/sitemaps/pages/sitemap.xml", 0.1))