from bs4 import BeautifulSoup
import requests

# Website to scrape
base_website = "https://www.otodom.pl/pl/firmy/biura-nieruchomosci/mo-real-estate-ID7575405"

# Replace the headers with yours ( https://httpbin.org/get )
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# Array for the apartments
apartments = []


def get_data(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_next_page(soup):
    page_nav = soup.find('nav', {'data-cy': 'adverts-pagination'})
    if page_nav:
        next_button = page_nav.find('button', {'data-cy': 'pagination.next-page'})
        if next_button:
            current_page_button = int(page_nav.find('button', {'aria-current': 'true'}).text)
            next_page_url = f"{base_website}?page={current_page_button + 1}"
            return next_page_url
    return None


def main():
    # Initial page
    current_page_url = base_website

    while current_page_url:
        # Make an HTTP request GET from the server
        soup = get_data(current_page_url)

        product_list = soup.find_all('li', class_='css-iq9jxc emxfic50')

        # Extract and print links
        product_links = []
        for item in product_list:
            for link in item.find_all('a', class_='css-1qenxk6 emxfic58'):
                # Append a link of an apartment to a list
                product_links.append('https://www.otodom.pl' + link['href'])

        # Iterate through a list with links and extract information
        for link in product_links:
            link_response = requests.get(link, headers=headers)
            if link_response.status_code == 200:
                soup = BeautifulSoup(link_response.content, 'html.parser')

                # Find a title of an apartment
                title_el = soup.find('h1', class_='css-z95p96 ehdsj771')
                title = title_el.getText(strip=True) if title_el else 'Title not found'

                # Find a location
                location_el = soup.find('a', class_='css-1jjm9oe e42rcgs1')
                location = location_el.getText(strip=True) if location_el else 'Location not found'

                # Find a price
                price_el = soup.find('strong', class_='css-13baep2 e1lbt8221')
                price = price_el.getText(strip=True) if price_el else 'Price not found'

                # Find a size
                size_el = soup.find('div', class_='css-1wmudpx')
                size = size_el.getText(strip=True) if size_el else 'Size not found'

                # Find a listing date
                date_label_div = soup.find('div', attrs={'aria-label': 'Dostępne od'})

                # Find the date inside this div
                if date_label_div:
                    date_el = date_label_div.find('div', class_='css-1wi2w6s e26jmad5')
                    date = date_el.getText(strip=True) if date_el else 'Date not found'
                else:
                    date = 'Date not found'

                # Save the data to a list
                apartment = {
                    'Title': title,
                    'Location': location,
                    'Price': price,
                    'Size': size,
                    'Listing Date': date,
                    'URL': link
                }

                # Adding to a list of all apartments
                apartments.append(apartment)

        # Get the next page URL
        current_page_url = get_next_page(soup)

    print(apartments)

main()
