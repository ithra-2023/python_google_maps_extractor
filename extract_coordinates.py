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
    print(f"Processing: {url}")  # Print the URL being processed

    if pd.isna(url):  # Check if the URL is NaN
        print("Skipping: NaN value")
        latitudes.append(None)
        longitudes.append(None)
        continue  # Skip to the next iteration
    
    # Check if the entry is already coordinates
    match = re.search(r'(-?\d+\.\d+),(-?\d+\.\d+)', str(url))
    if match:
        lat, lng = match.groups()
        print(f"Coordinates found: {lat}, {lng}")
        latitudes.append(lat)
        longitudes.append(lng)
        continue  # Skip to the next iteration

    # Expand short URL
    # Expand short URL
    try:
        full_url = expand_url(url)
        print(f"Expanded URL: {full_url}")  # Print the expanded URL

    except requests.exceptions.MissingSchema:
        print("Skipping: Invalid URL")
        latitudes.append(None)
        longitudes.append(None)
        continue  # Skip to the next iteration

    # Use regex to extract latitude and longitude
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', full_url)
    if match:
        lat, lng = match.groups()
        print(f"Extracted coordinates: {lat}, {lng}")
        latitudes.append(lat)
        longitudes.append(lng)
    else:
        print("No coordinates found")
        latitudes.append(None)
        longitudes.append(None)

# Add the extracted latitudes and longitudes to the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

# Save the updated DataFrame back to Excel
df.to_excel("updated_file.xlsx", index=False)
