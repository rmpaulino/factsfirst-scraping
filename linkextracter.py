from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

# URL of the page to scrape
base_url = "https://factsfirst.ph/fact-checks"

# Define the allowed domains in the specified format
allowed_domains = {
    "www.rappler.com",
    "www.altermidya.net",
    "interaksyon.philstar.com",
    "www.onenews.ph",
    "mindanaogoldstardaily.com"
}

# Set to store unique links across all pages
all_unique_links = set()

# Setup Chrome WebDriver
service = Service('/Users/rolandoyoung/Downloads/chromedriver-mac-arm64/chromedriver')  # Update with the correct path to your ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless Chrome
driver = webdriver.Chrome(service=service, options=options)
driver.get(base_url)

# Function to extract links from a single page
def extract_links(soup, base_url, allowed_domains):
    unique_links = set()
    items = soup.find_all('div', class_='collection-item-5 w-dyn-item', role='listitem')
    for item in items:
        links = item.find_all('a', href=True)
        for link in links:
            href = link['href']
            absolute_url = urljoin(base_url, href)
            domain = urlparse(absolute_url).netloc
            if not domain == "www.rappler.com":
                print(domain)
            if domain in allowed_domains:
                unique_links.add(absolute_url)
    return unique_links

# Loop through all pages
page_number = 1
while True:
    print(f"Scraping page {page_number}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_unique_links.update(extract_links(soup, base_url, allowed_domains))
    
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'pagination-button.jetboost-pagination-next-dgzj.w-button'))
        )
        next_button.click()
        time.sleep(2)  # Wait for new content to load
        page_number += 1
    except Exception as e:
        print("No more pages or error occurred:", e)
        break

driver.quit()

# Save the unique links to a text file
with open('unique_links.txt', 'w') as file:
    for link in all_unique_links:
        file.write(link + '\n')

print(f"Saved {len(all_unique_links)} unique links to unique_links.txt")
