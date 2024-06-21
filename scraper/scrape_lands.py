import time
from datetime import datetime, timedelta
import random
from bs4 import BeautifulSoup
import requests
from retry import retry
from config import collection

# Website to scrape
base_website = "https://www.realtor.com/realestateandhomes-search/Makawao_HI"

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

# Empty arrays for the apartments and links
apartments = []
apartment_links = []


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


# Get the date the apartment was listed
def get_listed_date(soup):
    # Find a when the land was posted
    days_el1 = soup.find('span', string='Time on Realtor.com')
    days_el = days_el1.find_next('div')
    # Get only days
    days_ago = days_el.getText(strip=True).split(' ') if days_el else 'N/A'
    # Calculate the date when it was listed
    date = datetime.now() - timedelta(days=int(days_ago[0]))

    # Return the date in the format dd-mm-yy
    return date.strftime('%d-%m-%Y')


# Handle pagination
def get_next_page(soup):
    next_link = soup.find('a', class_='base__StyledAnchor-rui__ermeke-0 Bcaij next-link')

    if next_link and 'disabled' not in next_link['class']:
        return 'https://www.realtor.com' + next_link['href']
    return None


def get_size(soup):
    # Get the size of the apartment
    size_el = soup.find('span', class_='meta-value')
    size = float(size_el.getText(strip=True).replace(',', '')) if size_el else 'N/A'

    # Find whether the size is in acres or sqft
    unit_el = size_el.find_next_sibling(string=True)
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
    # Rotate proxies
    proxy = {"http": random.choice(proxies)}
    next_page = base_website

    # Redirecting to the next pages
    while next_page:
        soup = get_data(next_page, headers, proxy)
        if soup is None:  # If you're not allowed to scrape the page, skip it
            continue

        # Find all "cards" of the apartments
        list_of_apartments = soup.find_all('div', class_='BasePropertyCard_propertyCardWrap__30VCU')

        # Iterate through apartments
        for apartment in list_of_apartments:
            for link in apartment.find_all('a', class_='LinkComponent_anchor__TetCm'):
                href = 'https://www.realtor.com' + link['href']

                # Add apartment link to a list
                if href not in apartment_links:
                    apartment_links.append(href)

            # Get the next page
            next_page = get_next_page(soup)

    for link in apartment_links:
        soup = get_data(link, headers, proxy)

        # Get the title of the apartment
        title_el = soup.find('h1', class_='sc-6a58edfc-3 kpZRpX')
        title = title_el.getText(strip=True) if title_el else 'N/A'

        # Get the location
        location = title

        # Get the price
        price_el = soup.find('div', class_='Pricestyles__StyledPrice-rui__btk3ge-0 kjbIiZ sc-54acf6bc-1 VAINH')
        price = price_el.getText(strip=True)[1:].replace(',', '') if price_el else 'N/A' # Remove the dollar sign and convert into text

        date = get_listed_date(soup)

        apartment = {
            'Title': title,
            'Location': location,
            'Price ($)': float(price),
            'Size (sqft)': get_size(soup),
            'Listing date': date,
            'URL': link
        }

        # Insert the apartment into the collection
        collection.insert_one(apartment)

        # Delay after a land scraping
        time.sleep(3)
    print('Data has been scraped successfully!')


main()
