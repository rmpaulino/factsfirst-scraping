import requests
from bs4 import BeautifulSoup

def extract_article_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the data. Status code: {response.status_code}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Extract publishing date/time
    date_tag = soup.find('span', class_='td-post-date')
    date = date_tag.text.strip() if date_tag else "Unknown Date/Time"

    # Extract article body
    article_content = ""
    
    possible_containers = [
        'td-post-content tagdiv-type',
        'td-ss-main-content'
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

    # Extract article rating
    rating = "Unavailable"
    # Find all <div> tags with class 'common-text-content-container'
    div_tags = soup.find_all('div', class_='td-post-content tagdiv-type')
    # Iterate over each <div> tag to find the rating
    for div_tag in div_tags:
        # Iterate through all <p> tags within the <div>
        for p_tag in div_tag.find_all('p'):
            # Check if the <p> tag contains a <strong> tag with "RATING:"
            if 'rating:' in p_tag.get_text().lower().strip():
                # Extract the full text of the <p> tag
                full_text = p_tag.get_text()
                rating = full_text.lower().strip().split('rating:')[-1].strip()
                break
            elif 'category:' in p_tag.get_text().lower().strip():
                # Extract the full text of the <p> tag
                full_text = p_tag.get_text()
                rating = full_text.lower().strip().split('category:')[-1].strip()
                break
        else:
            continue
        break

    # Return the extracted data
    return {
        'title': title,
        'date': date,
        'rating': rating,
        'body': article_content.strip()
    }

# Example usage
url = "https://mindanaogoldstardaily.com/archives/129938"
article_data = extract_article_data(url)

if article_data:
    print("Title:", article_data['title'],'\n')
    print("Author: MGSD",'\n')
    print("Publishing Date:", article_data['date'],'\n')
    print("Rating:", article_data['rating'],'\n')
    print("Body Text:", article_data['body'])
