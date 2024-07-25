import requests
import pandas as pd

# Function to fetch plants by color from Perenual API
def get_all_plants(api_key):
    all_plants = []
    page = 1
    while True:
        url = f'https://perenual.com/api/species-list?key={api_key}&page={page}'
        response = requests.get(url)
        data = response.json()

        if 'data' in data and data['data']:
            all_plants.extend(data['data'])
            page += 1
        else:
            break
    return all_plants

# Your actual API key
api_key = 'sk-uyma66a0c007ce2126318'

# Fetch all plant data
plants = get_all_plants(api_key)

# Convert to DataFrame
df = pd.DataFrame(plants)

# Save to CSV
df.to_csv('perenual_plants.csv', index=False)

print("Data downloaded and saved to perenual_plants.csv")