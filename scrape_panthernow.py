import requests
from bs4 import BeautifulSoup
import os
import time

os.makedirs('data', exist_ok=True)

article_urls = [
    'https://panthernow.com/2024/02/16/fiu-has-a-surge-in-online-classes-and-its-clear-why/',
    'https://panthernow.com/2024/05/11/fiu-online-is-wasted-potential/',
    'https://panthernow.com/2026/02/12/the-vanishing-of-david-grutmans-fiu-course-are-colleges-keeping-up/',
    'https://panthernow.com/2024/08/20/alleged-anti-semitism-controversy-at-fiu-ignites-statewide-review-of-course-material/',
    'https://panthernow.com/2024/09/08/and-so-it-continues-fiu-faculty-navigate-statewide-anti-semitism-review/',
    'https://panthernow.com/2024/11/25/fiu-faculty-oppose-volunteering-on-antisemitism-committee-reviews/',
]

# Add browser-like headers so the site doesn't block the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

all_text = []

for url in article_urls:
    print(f'Fetching {url}...')

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get article title
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else 'No title'

        # Grab ALL paragraphs and keep only meaningful ones (over 60 chars)
        paragraphs = soup.find_all('p')
        body = ' '.join([
            p.get_text(strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 60
        ])

        if body:
            all_text.append(f"TITLE: {title_text}\n\n{body}")
            print(f'  Saved: {title_text[:60]}')
        else:
            print(f'  No content found for: {url}')

        time.sleep(1)

    except requests.RequestException as e:
        print(f'  Error: {e}')

with open('data/panthernow.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n---\n\n'.join(all_text))

print(f'\nDone! Saved {len(all_text)} articles to data/panthernow.txt')