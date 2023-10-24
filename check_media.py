
import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, cpu_count

# Définition des arguments et valeurs par défaut
parser = argparse.ArgumentParser(description="Scan articles for missing media links.")
parser.add_argument("--base-url", default="https://ives-openscience.eu/", help="Base URL of the articles.")
parser.add_argument("--start", type=int, default=1, help="Starting article number.")
parser.add_argument("--end", type=int, default=40197, help="Ending article number.")
parser.add_argument("--output-file", default="missing_media.csv", help="Output CSV file.")
parser.add_argument("--id-url", default="publication-pdf", help="ID of the target URL to check.")

args = parser.parse_args()

BASE_URL = args.base_url
START = args.start
END = args.end
OUTPUT_FILE = args.output_file
ID_URL = args.id_url
CHUNK_SIZE = (END - START + 1) // cpu_count()

async def fetch(session, url):
    print(f"Fetching {url}")  # Log
    async with session.get(url) as response:
        return await response.text()

async def check_link(session, url):
    print(f"Checking link {url}")  # Log
    async with session.head(url) as response:
        return response.status == 404

async def process_chunk(start, end):
    async with aiohttp.ClientSession() as session:
        for article_id in range(start, end + 1):
            article_url = BASE_URL + str(article_id) + "/"
            html_content = await fetch(session, article_url)
            soup = BeautifulSoup(html_content, "html.parser")
            link_element = soup.find('a', id="target-pdf-id")
            pdf_link = link_element['href'] if link_element else None
            if pdf_link and await check_link(session, pdf_link):
                print(f"Found missing media at {article_url}")  # Log
                with open(OUTPUT_FILE, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([pdf_link, article_url])

def worker(start):
    print(f"Starting worker for range {start} to {start + CHUNK_SIZE}")  # Log
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_chunk(start, start + CHUNK_SIZE))
    loop.close()

if __name__ == "__main__":
    # Write header to the CSV file
    with open(OUTPUT_FILE, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Missing Media URL", "Article URL"])

    # Split the work among processes
    print(f"Starting multiprocessing with chunk size {CHUNK_SIZE}")  # Log
    with Pool() as pool:
        pool.map(worker, range(START, END + 1, CHUNK_SIZE))
