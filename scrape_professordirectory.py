import requests
from bs4 import BeautifulSoup
import os
import time

os.makedirs('data', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Professors with most reviews at FIU
professor_urls = [
    'https://www.professors.directory/rate/jose-m-eirin-lopez_florida-international-university',
    'https://www.professors.directory/rate/george-obrien_florida-international-university',
    'https://www.professors.directory/rate/harry-m-rhea_florida-international-university',
    'https://www.professors.directory/rate/kevin-oshea_florida-international-university',
    'https://www.professors.directory/rate/jorge-l-rodriguez_florida-international-university',
    'https://www.professors.directory/rate/nathan-e-dodge_florida-international-university',
    'https://www.professors.directory/rate/m-orjuela-garabito_florida-international-university',
    'https://www.professors.directory/rate/annette-b-fromm_florida-international-university',
]

all_text = []

for url in professor_urls:
    print(f'Fetching {url}...')

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get professor name
        name = soup.find('h2')
        name_text = name.get_text(strip=True) if name else 'Unknown'

        # Get all paragraphs with review text (longer than 60 chars)
        paragraphs = soup.find_all('p')
        reviews = [
            p.get_text(strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 60
        ]

        if reviews:
            block = f"PROFESSOR: {name_text}\nSOURCE: {url}\n\n" + '\n\n'.join(reviews)
            all_text.append(block)
            print(f'  Saved {len(reviews)} reviews for {name_text}')
        else:
            print(f'  No reviews found for {name_text}')

        time.sleep(1)

    except requests.RequestException as e:
        print(f'  Error: {e}')

with open('data/professorsdirectory.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n---\n\n'.join(all_text))

print(f'\nDone! Saved {len(all_text)} professor pages to data/professorsdirectory.txt')