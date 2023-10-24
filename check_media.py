import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://site.com/"
START = 1
END = 100000
OUTPUT_FILE = "missing_media.csv"

def get_pdf_link_from_article(article_id):
    """Récupère le lien du PDF d'un article."""
    url = BASE_URL + str(article_id) + "/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {url}: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    link_element = soup.find('a', id="publication-pdf")
    return link_element['href'] if link_element else None

def check_link(link):
    """Vérifie si un lien pointe vers un média manquant."""
    response = requests.head(link, allow_redirects=True)
    return response.status_code == 404

def main():
    with open(OUTPUT_FILE, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Missing Media URL", "Article URL"])

        for article_id in range(START, END + 1):
            print(f"Checking article {article_id}")
            article_url = BASE_URL + str(article_id) + "/"
            pdf_link = get_pdf_link_from_article(article_id)

            if pdf_link and check_link(pdf_link):
                writer.writerow([pdf_link, article_url])
                print(f"Missing media: {pdf_link} in article {article_url}")

            time.sleep(0.5)  # Ajoute un délai de 0,5 secondes entre chaque requête

if __name__ == "__main__":
    main()
