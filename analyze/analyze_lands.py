import pandas as pd
from config import collection
import numpy as np

# Load data from MongoDB
data = pd.DataFrame(list(collection.find()))

# Create a new column for price per sqft
data['Price per sqft ($)'] = round(data['Price ($)'] / data['Size (sqft)'])

# Group by location and calculate the average price per sqft
avg_price_per_sqft = data.groupby('Location')['Price per sqft ($)'].mean().sort_values(ascending=False)
top_5 = avg_price_per_sqft.head(5)  # Get the top 5 expensive locations
print(top_5)

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

# Update the MongoDB collection with the new category
for _, row in data.iterrows():
    collection.update_one({'_id': row['_id']}, {'$set': {'Category': row['Category']}})
print('Data has been categorized successfully!')
