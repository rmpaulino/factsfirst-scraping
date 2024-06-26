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
    date_tag = soup.find('div', class_='td-module-meta-info')
    date = date_tag.text.strip() if date_tag else "Unknown Date/Time"

    article_content = ""
    
    possible_containers = [
        'td-post-content tagdiv-type'
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

    # Return the extracted data
    return {
        'title': title,
        'date': date,
        'body': article_content.strip()
    }

# Example usage
url = "https://dailyguardian.com.ph/false-chris-rock-says-he-forgives-will-smith-but-not-the-marcoses/?fbclid=IwAR0hSyyVrYMyxLZgmMD-KkaUESgIHE88qPSfJEugqqEJ-go1S1nMGun46rU"
article_data = extract_article_data(url)

if article_data:
    print("Title:", article_data['title'])
    print("Publishing Date/Time:", article_data['date'])
    print("Body Text:", article_data['body'])
