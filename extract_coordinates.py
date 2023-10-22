import pandas as pd
import re
import requests

def expand_url(short_url):
    response = requests.get(short_url)
    return response.url

# Read the Excel file into a DataFrame
df = pd.read_excel("data/Ready to Use - with google map-cleaned.xlsx")

# Initialize empty lists to store latitudes and longitudes
latitudes = []
longitudes = []

# Loop through the URLs in the DataFrame
for url in df['Google Maps Link']:
    if pd.isna(url):  # Check if the URL is NaN
        latitudes.append(None)
        longitudes.append(None)
        continue  # Skip to the next iteration

    # Expand short URL
    full_url = expand_url(url)
    
    # Use regex to extract latitude and longitude
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', full_url)
    if match:
        lat, lng = match.groups()
        latitudes.append(lat)
        longitudes.append(lng)
    else:
        latitudes.append(None)
        longitudes.append(None)

# Add the extracted latitudes and longitudes to the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

# Save the updated DataFrame back to Excel
df.to_excel("updated_file.xlsx", index=False)
