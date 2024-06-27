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
url = "https://www.onenews.ph/articles/fact-check-tiktok-user-spliced-willie-ong-s-claim-about-vice-presidential-debate?fbclid=IwAR0cvffy9bEtfktu7S5pq51duCQ9-AIyRfpaXXvFjF-FI2A-aVk3jTlWK1o"
#url = "https://www.onenews.ph/articles/fact-check-pacquiao-did-not-withdraw-his-candidacy-for-president?fbclid=IwAR13fjQFQxuILEqx_G2sCChPdzwBCTd5sanzYXps7e9ag8WMaRd62MeJAqQ"
article_data = extract_article_data(url)

if article_data:
    print("Title:", article_data['title'],'\n')
    print("Author:", article_data['author'],'\n')
    print("Publishing Date:", article_data['date'],'\n')
    print("Rating:", article_data['rating'],'\n')
    print("Body Text:", article_data['body'])
