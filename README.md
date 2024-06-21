# Real Estate Data Scraper

This script scrapes real estate listings from Realtor.com and stores the data in a MongoDB database. Additionally, it processes the data to categorize listings based on price per square foot and visualizes the top 5 most expensive locations.

#### Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- `requests` library: `pip install requests`
- `beautifulsoup4` library: `pip install beautifulsoup4`
- `pymongo` library: `pip install pymongo`
- `retry` library: `pip install retry`
- `pandas` library: `pip install pandas`
- `numpy` library: `pip install numpy`
- `matplotlib` library: `pip install matplotlib`

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
https://github.com/malikoyv/RealEstate-WebScraper/assets/124885789/c6d95d82-7322-4be6-b716-9d4f2872dd87
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

6. **Data Processing and Visualization**:
   - Loads data from MongoDB into a pandas DataFrame.
   - Creates a new column for price per square foot.
   - Groups data by location and calculates the average price per square foot.
   - Defines thresholds to categorize listings into 'Cheap', 'Moderate', and 'Expensive'.
   - Performs a bulk update in MongoDB to include the category field.
   - Plots a bar chart for the top 5 most expensive locations and saves it as an image file.

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
  
5. **View the Visualization**:
   - The bar chart for the top 5 most expensive locations will be saved as top_locations.png.
   <img src="https://github.com/malikoyv/RealEstate-WebScraper/assets/124885789/67c860bc-b6e8-4ddf-bad7-c106a2b4ce0a" height=200px>

#### Example Usage

```python
# Example call to main function
if __name__ == "__main__":
    main()
```

This script automates the process of scraping real estate listings from Realtor.com, extracting relevant information, and storing it in a MongoDB database. Adjust the script as needed for your specific use case or target websites.
