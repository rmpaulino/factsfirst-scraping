import requests
from bs4 import BeautifulSoup

def get_fact_check_details(url):
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
    
    # Extract the full article text
    article_text = []
    article_tag = soup.find('div', class_='et_pb_section et_pb_section_2_tb_body et_section_regular')
    if article_tag:
        for p in article_tag.find_all('p'):
            article_text.append(p.get_text(strip=True))
    article = '\n'.join(article_text) if article_text else 'No Article Found'
    
    return {
        'Title': title,
        'Author': author,
        'Rating': rating,
        'Full Article': article
    }

# Example usage
url = 'https://www.altermidya.net/hindi-totoo-lahat-ng-mga-aklat-sa-kasaysayan-na-inilathala-sa-panahon-ng-administrasyong-cory-aquino-ay-purong-paninira-sa-mga-marcos/'  # Replace with the actual URL of the fact-check article
fact_check_details = get_fact_check_details(url)

if fact_check_details:
    print(f"Title: {fact_check_details['Title']}")
    print(f"Author: {fact_check_details['Author']}")
    print(f"Rating: {fact_check_details['Rating']}")
    print(f"Full Article:\n{fact_check_details['Full Article']}")
