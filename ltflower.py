import streamlit as st
import requests
import pandas as pd
import numpy as np
from webcolors import hex_to_rgb, rgb_to_hex

# Function to fetch plants by color from Perenual API
def get_plants_by_color(api_key, color, num_plants, sun_level, water_frequency, plant_cycle, growth_rate):
    url = (f'https://perenual.com/api/species-list?key={api_key}&flower_color={color}'
           f'&limit={num_plants}&sun_level={sun_level}&water_frequency={water_frequency}'
           f'&plant_cycle={plant_cycle}&growth_rate={growth_rate}')
    response = requests.get(url)
    return response.json()

# Function to convert hex to rgb
def hex_to_rgb_tuple(hex_color):
    return hex_to_rgb(hex_color)

# Function to find complementary color
def get_complementary_color(rgb_color):
    comp_rgb = tuple(255 - val for val in rgb_color)
    return rgb_to_hex(comp_rgb)

# Function to get analogous colors
def get_analogous_colors(rgb_color):
    shift = 30
    analogous1 = tuple((val + shift) % 256 for val in rgb_color)
    analogous2 = tuple((val - shift) % 256 for val in rgb_color)
    return [rgb_to_hex(analogous1), rgb_to_hex(analogous2)]

# Streamlit app
st.title('Flora Advisor: Professional Plant Matchmaking')

st.markdown("""
    Welcome to Flora Advisor! Our goal is to help you find the perfect plants to complement your garden. 
    Please provide the details below to receive tailored recommendations.
""")

api_key = st.text_input('Enter your Perenual API Key')
house_color = st.color_picker('Select the color of your house', '#ff0000')
scheme = st.radio('Choose a color scheme:', ['Similar', 'Complementary', 'Analogous'])
num_plants = st.slider('Number of plants to display:', min_value=1, max_value=20, value=10)

# Additional questions
sun_level = st.selectbox('What is the sun exposure level?', ['Full Shade', 'Part Shade', 'A Mix of Sun and Shade', 'Full Sun'])
water_frequency = st.selectbox('How often do you water your plants?', ['Frequently', 'Average', 'Minimal'])
st.write('Note: If you have an automatic sprinkler system, select based on its settings.')
plant_cycle = st.selectbox('Plant cycle:', ['Perennial', 'Annual', 'Biannual'])
growth_rate = st.selectbox('Growth rate:', ['High', 'Moderate', 'Low'])

if st.button('Find Plants'):
    if api_key:
        house_rgb = hex_to_rgb_tuple(house_color)
        color_hexes = []

        if scheme == 'Similar':
            color_hexes.append(house_color.lstrip('#'))
        elif scheme == 'Complementary':
            color_hexes.append(get_complementary_color(house_rgb).lstrip('#'))
        elif scheme == 'Analogous':
            color_hexes.extend([c.lstrip('#') for c in get_analogous_colors(house_rgb)])

        plant_data = []

        for color in color_hexes:
            data = get_plants_by_color(api_key, color, num_plants, sun_level, water_frequency, plant_cycle, growth_rate)
            if 'data' in data:
                for plant in data['data']:
                    plant_data.append({
                        'Common Name': plant['common_name'],
                        'Scientific Name': plant['scientific_name'],
                        'Family': plant['family'],
                        'Flower Color': plant.get('flower_color', 'N/A'),
                        'Image URL': plant.get('image_url', '')
                    })

        if plant_data:
            df = pd.DataFrame(plant_data)
            st.dataframe(df)

            # Calculate the average number of letters in common names using numpy
            common_name_lengths = np.array([len(name) for name in df['Common Name']])
            average_length = np.mean(common_name_lengths)
            st.write(f"Average number of letters in common names: {average_length:.2f}")

            for _, row in df.iterrows():
                st.subheader(row['Common Name'])
                st.write(f"Scientific Name: {row['Scientific Name']}")
                st.write(f"Family: {row['Family']}")
                st.write(f"Flower Color: {row['Flower Color']}")
                st.image(row['Image URL'])
        else:
            st.write(f"No plants found for the specified color scheme and criteria.")
    else:
        st.write("Please enter a valid API key.")
