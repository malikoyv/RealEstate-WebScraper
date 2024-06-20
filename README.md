# Real Estate Data Scraper

This script scrapes real estate listings from Realtor.com for properties in Makawao, HI, and stores the data in a MongoDB database. 

#### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `requests` library: `pip install requests`
- `beautifulsoup4` library: `pip install beautifulsoup4`
- `pymongo` library: `pip install pymongo`
- `retry` library: `pip install retry`

#### MongoDB Setup

1. **Create a MongoDB Atlas Account**:
   - Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
   - Create a new cluster and set up a database user with a username and password.

2. **Get the Connection URI**:
   - Once your cluster is set up, get the connection string. Replace the placeholders with your database user's credentials and cluster information. It should look similar to:
     ```plaintext
     mongodb+srv://root:1234567890@atlascluster.hpyo9qg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster
     ```

3. **Modify the Script**:
   - Update the `uri` variable in the script with your MongoDB connection string.
   - Replace `'real_estate'` and `'data'` in the `db` and `collection` assignments with your desired database and collection names if they differ.

#### Demo Video
https://github.com/malikoyv/RealEstate-WebScraper/assets/124885789/ec9a30bc-3754-47fe-adc0-397076195d2a
#### Script Explanation

The script is divided into several parts:

1. **Imports and Setup**:
   - Import necessary libraries (`time`, `datetime`, `random`, `BeautifulSoup`, `requests`, `MongoClient`, `retry`).

2. **Database Connection**:
   - Connect to MongoDB using the provided URI and select the database and collection.

3. **User Agents and Proxies**:
   - Define a list of user agents and proxies to rotate during scraping to avoid being blocked.

4. **Utility Functions**:
   - `get_data(url, headers, proxy)`: Fetches the HTML content of a page, retries up to 5 times if it fails.
   - `get_listed_date(soup)`: Extracts and calculates the listing date from the HTML content.
   - `get_next_page(soup)`: Identifies the link to the next page of listings.

5. **Main Function**:
   - Initializes headers and proxy.
   - Iterates through listing pages, collecting apartment links.
   - For each apartment link, fetches detailed information and stores it in MongoDB.

#### How to Run the Script

1. **Install Required Libraries**:
   - Ensure all necessary Python libraries are installed using `pip`:
     ```bash
     pip install requests beautifulsoup4 pymongo retry
     ```

2. **Update Database URI**:
   - Update the `uri` variable in the script with your MongoDB connection string.

3. **Run the Script**:
   - Execute the script in your terminal or command prompt:
     ```bash
     python real_estate_scraper.py
     ```

4. **Check MongoDB**:
   - After running the script, check your MongoDB database to ensure the data has been inserted correctly.

#### Example Usage

```python
# Example call to main function
if __name__ == "__main__":
    main()
```

This script automates the process of scraping real estate listings from Realtor.com, extracting relevant information, and storing it in a MongoDB database. Adjust the script as needed for your specific use case or target websites.
