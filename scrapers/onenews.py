import requests
from bs4 import BeautifulSoup
'''
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
    title_tag = soup.find('div', class_='post-header-container')
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Extract publishing date/time
    date_tag = soup.find('div', class_='post-meta-wrapper full-size ver-2')
    date = date_tag.find_all('div', class_='meta-item')[1].text.strip() if date_tag else "Unknown Date/Time"

    # Extract author
    author_tag = soup.find('div', class_='post-meta-wrapper full-size ver-2')
    author = author_tag.find_all('div', class_='meta-item')[0].text.strip() if author_tag else "Unknown Author"

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

    # Extract article body
    article_content = ""
    for div_tag in div_tags:
        for p_tag in div_tag.find_all('p'):
            article_content += p_tag.get_text(strip=True) + "\n\n"
        else:
            continue
        break

    # Return the extracted data
    return {
        'title': title,
        'author': author,
        'date': date,
        'rating': rating,
        'body': article_content.strip()
    }

# Example usage
print("Paste the OneNews URL: ")
url = input()
article_data = extract_article_data(url)

if article_data:
    print("Title:", article_data['title'],'\n')
    print("Author:", article_data['author'],'\n')
    print("Publishing Date:", article_data['date'],'\n')
    print("Rating:", article_data['rating'],'\n')
    print("Body Text:", article_data['body'])
'''
def onenews_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('div', class_='post-header-container').text.strip() if soup.find('div', class_='post-header-container') else "Unknown Title"

    date = soup.find('div', class_='post-meta-wrapper full-size ver-2').find_all('div', class_='meta-item')[1].text.strip() if soup.find('div', class_='post-meta-wrapper full-size ver-2') else "Unknown Date/Time"

    author = soup.find('div', class_='post-meta-wrapper full-size ver-2').find_all('div', class_='meta-item')[0].text.strip() if soup.find('div', class_='post-meta-wrapper full-size ver-2') else "Unknown Author"

    rating = "Unavailable"
    div_tags = soup.find_all('div', class_='common-text-content-container')
    for div_tag in div_tags:
        for p_tag in div_tag.find_all('p'):
            strong_tag = p_tag.find('strong')
            if strong_tag and 'rating:' in strong_tag.get_text().lower().strip():
                rating = strong_tag.get_text().split(':')[-1].strip()
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

print("Paste the OneNews URL: ")
url = input()
article_data = onenews_scraper(url)

if article_data:
    print("Title:", article_data['title'],'\n')
    print("Author:", article_data['author'],'\n')
    print("Publishing Date:", article_data['date'],'\n')
    print("Rating:", article_data['rating'],'\n')
    print("Body Text:", article_data['content'])