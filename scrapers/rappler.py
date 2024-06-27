import requests
from bs4 import BeautifulSoup
import re

def extract_rappler_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1', class_='post-single__title').text.strip()
    
    author_element = soup.find('span', class_='post-single__author-name')
    author = author_element.text.strip() if author_element else "Author not found"
    
    # Look for rating in elements with class 'wp-block-heading'
    rating = "Rating not found"
    rating_elements = soup.find_all(class_='wp-block-heading')
    for element in rating_elements:
        if 'rating' in element.text.lower() or 'marka' in element.text.lower():
            rating = element.text.strip()
            break
    
    article_content = ""
    
    possible_containers = [
        'container article-content-container cropped',
        'post-single__content',
        'storypage-divider',
        'article-content'
    ]
    
    article_container = None
    for container_class in possible_containers:
        article_container = soup.find('div', class_=container_class)
        if article_container:
            break
    
    if article_container:
        for element in article_container.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol']):
            if element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    article_content += li.get_text(strip=True) + "\n"
                article_content += "\n"
            else:
                article_content += element.get_text(strip=True) + "\n\n"
    else:
        article_content = "Could not find article content."
    
    return {
        'title': title,
        'author': author,
        'rating': rating,
        'content': article_content.strip()
    }

# Example usage
url = "https://www.rappler.com/newsbreak/fact-check/bir-job-facebook-post-link-fake-may-21-2024/"
article_data = extract_rappler_article(url)

print(f"Title: {article_data['title']}")
print(f"Author: {article_data['author']}")
print(f"Rating: {article_data['rating']}")
print(f"Content:\n{article_data['content']}")