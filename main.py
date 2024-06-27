import csv
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define scraper functions for each website
# def rappler_scraper(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     title = soup.find('h1', class_='post-single__title').text.strip()
    
#     author_element = soup.find('span', class_='post-single__author-name')
#     author = author_element.text.strip() if author_element else "Author not found"

#     meta_div = soup.find('div', class_='post-single__meta')
#     date = meta_div.find('time', class_='entry-date published post__timeago').text.strip() if meta_div else "Date not found"

#     rating = "Rating not found"
#     rating_elements = soup.find_all(class_='wp-block-heading')
#     for element in rating_elements:
#         if 'rating' in element.text.lower() or 'marka' in element.text.lower():
#             rating = element.text.strip()
#             break
    
#     article_content = ""
#     possible_containers = [
#         'container article-content-container cropped',
#         'post-single__content',
#         'storypage-divider',
#         'article-content'
#     ]
    
#     article_container = None
#     for container_class in possible_containers:
#         article_container = soup.find('div', class_=container_class)
#         if article_container:
#             break
    
#     if article_container:
#         for element in article_container.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol']):
#             if element.name in ['ul', 'ol']:
#                 for li in element.find_all('li'):
#                     article_content += li.get_text(strip=True) + "\n"
#                 article_content += "\n"
#             else:
#                 article_content += element.get_text(strip=True) + "\n\n"
#     else:
#         article_content = "Could not find article content."
    
#     return {
#         'title': title,
#         'author': author,
#         'date': date,
#         'rating': rating,
#         'content': article_content.strip()
#     }

def rappler_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1', class_='post-single__title').text.strip()
    
    author_element = soup.find('span', class_='post-single__author-name')
    author = author_element.text.strip() if author_element else "Author not found"

    meta_div = soup.find('div', class_='post-single__meta')
    date = meta_div.find('time', class_='entry-date published post__timeago').text.strip() if meta_div else "Date not found"

    rating = "Rating not found"
    
    # Search the entire page content for rating information
    page_text = soup.get_text()
    index = page_text.lower().find('rating:')
    if index == -1:
        index = page_text.lower().find('marka:')
    
    if index != -1:
        # Find the next paragraph or sentence after 'rating:' or 'marka:'
        start_index = index + len('rating:') if index != -1 else index + len('marka:')
        end_index = page_text.find('\n', start_index)
        if end_index == -1:
            end_index = page_text.find('.', start_index)
        if end_index == -1:
            end_index = len(page_text)
        
        rating_text = page_text[start_index:end_index].strip()
        
        # Check if 'Ang katotohanan:' is present and truncate text after it
        katotohanan_index = rating_text.lower().find('ang katotohanan:')
        if katotohanan_index != -1:
            rating_text = rating_text[:katotohanan_index].strip()
        
        # Check if 'The facts:' is present and truncate text after it (for English articles)
        facts_index = rating_text.lower().find('the facts:')
        if facts_index != -1:
            rating_text = rating_text[:facts_index].strip()
        
        rating = rating_text
    
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
        'date': date,
        'rating': rating,
        'content': article_content.strip()
    }



# Function to fetch and parse data from Altermidya
def altermidya_scraper(url):
    # Send a request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    # Parse the webpage content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title
    title_tag = soup.find('div', class_='et_pb_module et_pb_text et_pb_text_1_tb_body et_pb_text_align_left et_pb_bg_layout_light').find('div', class_='et_pb_text_inner')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title Found'

    # Extract the date
    date_tag = soup.find('div', class_='et_pb_module et_pb_text et_pb_text_2_tb_body et_pb_text_align_left et_pb_bg_layout_light').find('div', class_='et_pb_text_inner')
    date = date_tag.get_text(strip=True) if date_tag else 'No Date Found'

    # Extract the author
    author_tag = soup.find('meta', attrs={'name': 'author'})
    author = author_tag['content'] if author_tag else 'No Author Found'

    # Extract the rating
    rating = 'No Rating Found'
    for h4 in soup.find_all('h4', class_='wp-block-heading'):
        if 'MARKA:' in h4.get_text():
            next_p = h4.find_next_sibling('p')
            if next_p:
                strong_tag = next_p.find('strong')
                if strong_tag:
                    rating = strong_tag.get_text(strip=True)
                    break
    if rating == 'No Rating Found':
        rating_div = soup.find('div', string='RATING:')
        if rating_div:
            next_div = rating_div.find_next_sibling('div')
            if next_div:
                rating = next_div.get_text(strip=True)

    # Extract the full article text
    article_text = []
    article_tag = soup.find('div', class_='et_pb_section et_pb_section_2_tb_body et_section_regular')
    if article_tag:
        for p in article_tag.find_all('p'):
            paragraph_text = p.get_text(strip=True)
            if paragraph_text and paragraph_text not in article_text:  # Check for duplicates
                article_text.append(paragraph_text)
        article = '\n'.join(article_text) if article_text else 'No Article Found'
        if article_text == []:
            for div in article_tag.find_all('div', recursive=False):
                paragraph_text = div.get_text(strip=True)
                if paragraph_text and paragraph_text not in article_text:  # Check for duplicates
                    article_text.append(paragraph_text)
            article = '\n'.join(article_text) if article_text else 'No Article Found'
    else:
        article = 'No Article Found'

    return {
        'Title': title,
        'Author': author,
        'Date': date,
        'Rating': rating,
        'Full Article': article
    }
    # return {
    #     'title': "None",
    #     'author': "None",
    #     'date': "None",
    #     'rating': "None",
    #     'content': "None"
    # }
    # pass

# Function to fetch and parse data from Interaksyon
def interaksyon_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1', class_='entry-title').text.strip() if soup.find('h1', class_='entry-title') else "Unknown Title"

    author = soup.find('div', class_='td-post-author-name').find('a').text.strip() if soup.find('div', class_='td-post-author-name') else "Unknown Author"
    
    date = "Unknown Date/Time"
    date_tag = soup.find('div', class_='meta-info')
    if date_tag:
        date = date_tag.text.strip().split('-')[-1].strip()

    article_content = ""
    article_container = soup.find('div', class_='td-post-content td-pb-padding-side')
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
        'date': date,
        'content': article_content.strip()
    }

# Function to fetch and parse data from OneNews
def onenews_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('div', class_='post-header-container').text.strip() if soup.find('div', class_='post-header-container') else "Unknown Title"

    date = soup.find('div', class_='post-meta-wrapper full-size ver-2').find_all('div', class_='meta-item')[1].text.strip() if soup.find('div', class_='post-meta-wrapper full-size ver-2') else "Unknown Date/Time"

    author = soup.find('div', class_='post-meta-wrapper full-size ver-2').find_all('div', class_='meta-item')[0].text.strip() if soup.find('div', class_='post-meta-wrapper full-size ver-2') else "Unknown Author"

    # Extract rating
    rating = "Unavailable"
    # Find all <div> tags with class 'common-text-content-container'
    div_tags = soup.find_all('div', class_='common-text-content-container')
    # Iterate over each <div> tag to find the rating
    for div_tag in div_tags:
        # Iterate through all <p> tags within the <div>
        for p_tag in div_tag.find_all('p'):
            # Check if the <p> tag contains a <strong> tag with "RATING:"
            strong_tag = p_tag.find('strong')
            if strong_tag and 'rating:' in strong_tag.get_text().lower().strip():
                # Extract the full text of the <p> tag
                full_text = p_tag.get_text()
                rating = full_text.lower().strip().split('rating:')[-1].strip()
                break
        else:
            continue
        break
    
    article_content = ""
    for div_tag in div_tags:
        for p_tag in div_tag.find_all('p'):
            article_content += p_tag.get_text(strip=True) + "\n\n"
    
    return {
        'title': title,
        'author': author,
        'date': date,
        'rating': rating,
        'content': article_content.strip()
    }

# Function to fetch and parse data from Mindanao Gold Star Daily
def mindanaogoldstardaily_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1', class_='entry-title').text.strip() if soup.find('h1', class_='entry-title') else "Unknown Title"

    date = soup.find('span', class_='td-post-date').find('time').text.strip() if soup.find('span', class_='td-post-date') else "Unknown Date/Time"

    article_content = ""
    article_container = soup.find('div', class_='td-post-content tagdiv-type')
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

    rating = "Unavailable"
    div_tags = soup.find_all('div', class_='td-post-content tagdiv-type')
    for div_tag in div_tags:
        for p_tag in div_tag.find_all('p'):
            if 'rating:' in p_tag.get_text().lower().strip():
                rating = p_tag.get_text().split(':')[-1].strip()
                break
            elif 'category:' in p_tag.get_text().lower().strip():
                rating = p_tag.get_text().split(':')[-1].strip()
                break

    return {
        'title': title,
        'date': date,
        'rating': rating,
        'content': article_content.strip()
    }


filename = r'uniquelinks.txt'
if os.path.exists(filename):
    with open(filename, 'r') as file:
        links = file.read().splitlines()  # Limit to the first 10 links
        
        # Prepare CSV file
        csv_filename = 'extracted_data.csv'
        csv_columns = ['Title', 'Author', 'Date', 'Rating']
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            
            # Process each link
            for idx, link in enumerate(links, start=1):
                print(f"Processing Link No. {idx}: {link}")
                parsed_url = urlparse(link)
                domain = parsed_url.netloc
                
                data = {}

                # Determine which scraper function to call based on domain
                if domain == 'www.rappler.com':
                    data = rappler_scraper(link)
                elif domain == 'www.altermidya.net':
                    data = altermidya_scraper(link)
                elif domain == 'interaksyon.philstar.com':
                    data = interaksyon_scraper(link)
                elif domain == 'www.onenews.ph':
                    data = onenews_scraper(link)
                elif domain == 'mindanaogoldstardaily.com':
                    data = mindanaogoldstardaily_scraper(link)
                else:
                    print(f"No scraper function defined for {domain}")
                    continue
                
                # Write data to CSV
                writer.writerow({
                    'Title': data.get('title', ''),
                    'Author': data.get('author', ''),
                    'Date': data.get('date', ''),
                    'Rating': data.get('rating', '')
                })

                # Sleep to avoid overloading the server
                time.sleep(1.5)

        print(f"CSV file '{csv_filename}' has been created with extracted data.")
else:
    print(f"File {filename} not found.")
