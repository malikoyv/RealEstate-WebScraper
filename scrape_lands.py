from datetime import datetime, timedelta
import random

from bs4 import BeautifulSoup
import requests

# Website to scrape
base_website = "https://www.realtor.com/realestateandhomes-search/Makawao_HI"

# Replace the headers with yours ( https://httpbin.org/get )
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
]

# List of proxies to rotate
proxies = [
    "http://116.125.141.115:80",
]

# Array for the apartments
apartments = []
apartment_links = []


def get_data(url, headers, proxy):
    response = requests.get(url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_listed_date(soup):
    days_el1 = soup.find('span', string='Time on Realtor.com')
    days_el = days_el1.find_next('div')
    days_ago = days_el.getText(strip=True).split(' ') if days_el else 'N/A'
    date = datetime.now() - timedelta(days=int(days_ago[0]))

    return date.strftime('%d-%m-%y')


def main():
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
    }
    proxy = {"http": random.choice(proxies)}

    soup = get_data(base_website, headers, proxy)
    list_of_apartments = soup.find_all('div', class_='BasePropertyCard_propertyCardWrap__30VCU')

    for apartment in list_of_apartments:
        for link in apartment.find_all('a', class_='LinkComponent_anchor__TetCm'):
            apartment_links.append('https://www.realtor.com' + link['href'])

    for link in apartment_links:
        soup = get_data(link, headers, proxy)

        # Get the title of the apartment
        title_el = soup.find('h1', class_='sc-6a58edfc-3 kpZRpX')
        title = title_el.getText(strip=True) if title_el else 'N/A'

        # Get the location
        location = title

        # Get the price
        price_el = soup.find('div', class_='Pricestyles__StyledPrice-rui__btk3ge-0 kjbIiZ sc-54acf6bc-1 VAINH')
        price = price_el.getText(strip=True)[1:] if price_el else 'N/A'  # Remove the dollar sign and convert into text

        # Get the size of the apartment
        size_el = soup.find('span', class_='meta-value')
        size = size_el.getText(strip=True) if size_el else 'N/A'

        date = get_listed_date(soup)

        apartment = {
            'Title': title,
            'Location': location,
            'Price ($)': price,
            'Size (sqft)': size,
            'Listing date': date,
            'URL': link
        }
        apartments.append(apartment)

    print(apartments)


main()
