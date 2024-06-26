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
    title_tag = soup.find('div', class_='post-header-container')
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Extract publishing date/time
    date_tag = soup.find('div', class_='post-meta-wrapper full-size ver-2')
    date = date_tag.find_all('div', class_='meta-item')[1].text.strip() if date_tag else "Unknown Date/Time"

    # Extract author
    author_tag = soup.find('div', class_='post-meta-wrapper full-size ver-2')
    author = author_tag.find_all('div', class_='meta-item')[0].text.strip() if author_tag else "Unknown Author"

    # Extract rating
    rating = "Rating: Not Rated"
    article_container = soup.find('div', class_='common-text-content-container')
    if article_container:
        rating_tag = article_container.find('p', string='RATING:')
        if rating_tag:
            rating_text = rating_tag.find_next('strong').text.strip() if rating_tag.find('strong') else rating_tag.text.strip()
            rating = f"Rating: {rating_text}"

    # Extract article body
    article_content = ""
    main_content_container = soup.find('div', class_='common-text-content-container')
    if main_content_container:
        for paragraph in main_content_container.find_all('p'):
            article_content += paragraph.get_text(strip=True) + "\n\n"

    # Return the extracted data
    return {
        'title': title,
        'author': author,
        'date': date,
        'rating': rating,
        'body': article_content.strip()
    }

# Example usage
url = "https://www.onenews.ph/articles/fact-check-tiktok-user-spliced-willie-ong-s-claim-about-vice-presidential-debate?fbclid=IwAR0cvffy9bEtfktu7S5pq51duCQ9-AIyRfpaXXvFjF-FI2A-aVk3jTlWK1o"
article_data = extract_article_data(url)

if article_data:
    print("Title:", article_data['title'],'\n')
    print("Author:", article_data['author'],'\n')
    print("Publishing Date/Time:", article_data['date'],'\n')
    print("Rating:", article_data['rating'],'\n')
    print("Body Text:", article_data['body'])
