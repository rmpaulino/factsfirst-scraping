import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def scrape_website_data(url):
    url = "https://thebaguiochronicle.com/fact-check/fact-check-sagada-oranges-are-really-orange-in-hue-and-come-from-a-province-in-china-factsfirstph/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the page: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the title of the webpage
    website_title = soup.title.text.strip() if soup.title else 'No title found'

    # Find the author (always 'Baguio Chronicle' based on your description)
    author = "Baguio Chronicle"

    # Find the rating if available
    rating_tag = soup.find('div', class_='cxmmr5t8 oygrvhab hcukyx3x c1et5uql o9v6fnle ii04i59q')
    rating = rating_tag.text.strip() if rating_tag else 'No rating'

    # Find the date if available
    date_tag = soup.find('div', class_='jeg_meta_date')
    date_tag = date_tag.text.strip() if date_tag else 'No date available'

    return {
        'title': website_title,
        'author': author,
        'rating': rating,
        'date': date_tag,
    }

if __name__ == '__main__':
    url = 'https://www.baguiochronicles.com'
    website_data = scrape_website_data(url)
    
    if website_data:
        print(f"Website Title: {website_data['title']}")
        print(f"Author: {website_data['author']}")
        print(f"Rating: {website_data['rating']}")
        print(f"date: {website_data['date']}")
    else:
        print("Failed to fetch website data.")