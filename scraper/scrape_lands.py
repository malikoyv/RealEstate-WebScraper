import time
from datetime import datetime, timedelta
import random
import json
from bs4 import BeautifulSoup
import requests
from retry import retry
from config import collection

output_data = []
API_KEY = "c76de47d5f74419c14da1ee0df1ecec6"
base_url = "https://www.realtor.com/realestateandhomes-search/Makawao_HI/type-land"


# Get the date the land was listed
def get_listed_date(soup):
    # Find when the land was posted
    days_el1 = soup.find('span', string='Time on Realtor.com')
    days_el = days_el1.find_next('div') if days_el1 else None
    # Get only days
    days_ago = days_el.getText(strip=True).split(' ') if days_el else 'N/A'
    # Calculate the date when it was listed
    date = datetime.now() - timedelta(days=int(days_ago[0])) if days_ago != 'N/A' else datetime.now()

    # Return the date in the format dd-mm-yy
    return date.strftime('%d-%m-%Y')


def get_size(soup):
    # Get the size of the land
    size_el = soup.find('span', class_='meta-value')
    size = float(size_el.getText(strip=True).replace(',', '')) if size_el else 'N/A'

    # Find whether the size is in acres or sqft
    unit_el = size_el.find_next_sibling(string=True) if size_el else None
    unit = unit_el.strip() if unit_el else 'N/A'

    if unit == 'acre lot':
        size = round(float(size) * 43560)  # Convert acres to sqft

    return size


def scrape_listing(num_pages):
    for page in range(1, num_pages + 1):
        # To scrape page 1
        if page == 1:
            url = f"{base_url}"
        else:
            url = (
                f"{base_url}/pg-{page}"  # Adjust the URL structure based on the website
            )
        print(f"Scraping data from page {page}... {url}")

        payload = {"api_key": API_KEY, "url": url}
        # Make a request to the ScraperAPI
        r = requests.get("http://api.scraperapi.com", params=payload).text

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(r, "html.parser")

        # scraping individual page
        listings = soup.select("div[class^='BasePropertyCard_propertyCardWrap__']")
        print("Listings found!")

        for li in listings:
            for link1 in li.find_all('a', class_='LinkComponent_anchor__TetCm'):
                link = "https://www.realtor.com" + link1['href']
                request = requests.get(link, params=payload).text
                soup_link = BeautifulSoup(request, "html.parser")

                title_el = soup_link.find('h1', class_='sc-6a58edfc-3 kpZRpX')
                title = title_el.getText(strip=True) if title_el else 'N/A'
                location = title

                price_el = soup_link.find('div', class_='Pricestyles__StyledPrice-rui__btk3ge-0 kjbIiZ sc-54acf6bc-1 VAINH')
                price = price_el.getText(strip=True)[1:].replace(',', '') if price_el else 'N/A'

                date = get_listed_date(soup_link)

                land = {
                    'Title': title,
                    'Location': location,
                    'Price ($)': float(price) if price != 'N/A' else 'N/A',
                    'Size (sqft)': get_size(soup),
                    'Listing date': date,
                    'URL': link
                }

                collection.insert_one(land)

    print('Data has been scraped successfully!')


num_pages = 3
scrape_listing(num_pages)