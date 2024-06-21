import pandas as pd
from pymongo import UpdateOne

from scraper.config import collection
import numpy as np
import matplotlib.pyplot as plt

# Load data from MongoDB
data = pd.DataFrame(list(collection.find()))

# Create a new column for price per sqft
data['Price per sqft ($)'] = round(data['Price ($)'] / data['Size (sqft)'])

# Group by location and calculate the average price per sqft
avg_price_per_sqft = data.groupby('Location')['Price per sqft ($)'].mean().sort_values(ascending=False)
top_5 = avg_price_per_sqft.head(5)  # Get the top 5 expensive locations

# Calculate the mean and standard deviation of the price per sqft
mean_price_per_sqft = np.mean(avg_price_per_sqft)
std_price_per_sqft = np.std(avg_price_per_sqft)

# Define the thresholds for each category
cheap_threshold = mean_price_per_sqft - std_price_per_sqft
expensive_threshold = mean_price_per_sqft + std_price_per_sqft

# Define the thresholds for each category
thresholds = [0, cheap_threshold, expensive_threshold, np.inf]

# Ensure the thresholds are sorted
thresholds.sort()

# Categorize the land listings
data['Category'] = pd.cut(data['Price per sqft ($)'], bins=thresholds,
                          labels=['Cheap', 'Moderate', 'Expensive'])

# Perform the migration by updating MongoDB documents with the new 'Category' field
bulk_updates = [
    {
        'filter': {'_id': row['_id']},
        'update': {'$set': {'Category': row['Category']}}
    }
    for _, row in data.iterrows()
]

# Execute bulk updates in MongoDB
collection.bulk_write([UpdateOne(update['filter'], update['update']) for update in bulk_updates])

print('Data has been categorized and updated successfully!')

# Plotting the bar chart for the top 5 most expensive locations
plt.figure(figsize=(10, 6))
top_5.plot(kind='bar', color='skyblue')
plt.title('Average Price per Square Foot for Top 5 Most Expensive Locations')
plt.xlabel('Location')
plt.ylabel('Average Price per Square Foot ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot as an image file
plt.savefig('top_locations.png')
plt.show()
