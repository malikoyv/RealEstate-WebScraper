import time
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
import requests
from retry import retry
from config import collection

payload = { 'api_key': 'c76de47d5f74419c14da1ee0df1ecec6', 'url': 'https://www.realtor.com/realestateandhomes-search/Makawao_HI/type-land/' }
r = requests.get('https://api.scraperapi.com/', params=payload)

# Website to scrape
base_website = "https://www.realtor.com/realestateandhomes-search/Makawao_HI/type-land/"

# User Agents to rotate to avoid getting blocked
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
]

# List of proxies to rotate
proxies = [
    "http://116.125.141.115:80",
    "http://101.255.116.125:8080",
    "http://116.203.28.43:80",
    "http://103.110.10.190:3128",
    "http://117.250.3.58:8080",
]

# Empty arrays for the land and links
land_links = []


# Handle retries
@retry(tries=5, delay=2, backoff=2)
def get_data(url, headers, proxy):
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        response.raise_for_status()  # If the request was unsuccessful, raise an exception
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {str(e)}")
        raise  # Re-raise the exception so that the @retry decorator can catch it
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup


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


# Handle pagination
def get_next_page(soup, page_number):
    next_link = soup.find('a', class_='base__StyledAnchor-rui__ermeke-0 Bcaij next-link')
    if next_link and 'disabled' not in next_link.get('class', []):
        return base_website + "pg-" + page_number
    return None


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


def main():
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
    }
    proxy = {"http": random.choice(proxies)}
    next_page = base_website
    page_count = 1
    max_pages = 3  # Adjust this value to scrape more or fewer pages

    while next_page and page_count < max_pages:
        print(f"Scraping page {page_count}")
        soup = get_data(next_page, headers, proxy)

        list_of_lands = soup.find_all('div', class_='BasePropertyCard_propertyCardWrap__30VCU')

        for land in list_of_lands:
            for link in land.find_all('a', class_='LinkComponent_anchor__TetCm'):
                href = 'https://www.realtor.com' + link['href']
                if href not in land_links:
                    land_links.append(href)

        next_page = get_next_page(soup, page_count)
        if next_page:
            page_count += 1
        time.sleep(random.uniform(2, 5))  # Add a random delay between page requests

    print(f"Found {len(land_links)} land listings across {page_count} pages")

    for index, link in enumerate(land_links):
        print(f"Scraping listing {index + 1} of {len(land_links)}")
        soup = get_data(link, headers, proxy)

        title_el = soup.find('h1', class_='sc-6a58edfc-3 kpZRpX')
        title = title_el.getText(strip=True) if title_el else 'N/A'

        location = title

        price_el = soup.find('div', class_='Pricestyles__StyledPrice-rui__btk3ge-0 kjbIiZ sc-54acf6bc-1 VAINH')
        price = price_el.getText(strip=True)[1:].replace(',', '') if price_el else 'N/A'

        date = get_listed_date(soup)

        land = {
            'Title': title,
            'Location': location,
            'Price ($)': float(price) if price != 'N/A' else 'N/A',
            'Size (sqft)': get_size(soup),
            'Listing date': date,
            'URL': link
        }

        collection.insert_one(land)

        time.sleep(random.uniform(3, 6))  # Add a random delay between listing scrapes

    print('Data has been scraped successfully!')

if __name__ == "__main__":
    main()