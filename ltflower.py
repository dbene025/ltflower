import streamlit as st
import requests
import pandas as pd
import numpy as np
import base64
from io import BytesIO

# Function to convert image to base64
def get_base64_of_image(image_file):
    return base64.b64encode(image_file.read()).decode()

# Load the uploaded images
image_path = "fiuimage.png"
favicon_path = "favicon.png"

with open(image_path, "rb") as image_file:
    img_base64 = get_base64_of_image(image_file)

with open(favicon_path, "rb") as favicon_file:
    favicon_base64 = get_base64_of_image(favicon_file)

# Set page configuration with the favicon
st.set_page_config(page_title="Flora Advisor", page_icon=favicon_path)

# Function to fetch plants by criteria from Perenual API
def get_plants_by_criteria(api_key, sun_level, water_frequency, growth_rate, propagation, maintenance, drought_tolerant, salt_tolerant):
    url = (f'https://perenual.com/api/species-list?key={api_key}'
           f'&sun_level={sun_level}&water_frequency={water_frequency}'
           f'&growth_rate={growth_rate}&propagation={propagation}'
           f'&maintenance={maintenance}'
           f'&drought_tolerant={drought_tolerant}'
           f'&salt_tolerant={salt_tolerant}')
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get images from Unsplash API
def get_image(query, api_key):
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={api_key}"
    response = requests.get(url)
    data = response.json()
    image_url = data['results'][0]['urls']['regular'] if data.get('results') else None
    return image_url

# List of plant names
plant_names = [
    "Coneflower", "Lantana", "Bug bane", "Swamp milkweed",
    "Sea thrift", "Lily of the valley", "Aster", "Hybrid tuberous begonia",
    "Flowering quince", "Clematis", "Siam Tulip", "Dogwood",
    "Pink", "Cheddar pink", "Maiden pink", "Hardy geranium"
]

# Unsplash API key
unsplash_api_key = 'sk-YQBH66a1954d5a0d66318'

# Fetch images for each plant
plant_images = {name: get_image(name, unsplash_api_key) for name in plant_names}

# Custom CSS for reducing white space and centering elements
if img_base64:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap');

        .main-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            padding: 20px;
            border-radius: 10px;
            color: white; /* Text color to ensure readability over the background */
            margin-top: 0px; /* Reduce space above main content */
        }}
        .questions {{
            background-color: rgba(255, 255, 255, 0); /* Remove background */
            padding: 20px;
            border-radius: 10px;
            text-align: center; /* Center align text */
        }}
        .stSlider {{
            margin-top: 5px; /* Reduce space above the slider */
            margin-bottom: 5px; /* Reduce space below the slider */
        }}
        .stRadio {{
            display: flex;
            justify-content: center;
        }}
        table {{
            width: 100%;
            text-align: center; /* Center align table headings */
        }}
        th {{
            text-align: center; /* Center align table headings */
        }}
        td {{
            text-align: center; /* Center align table data */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Streamlit app
st.markdown('<div style="background-color:#333; color:fuchsia; font-family:\'Dancing Script\', cursive; font-size:2em; padding:10px; border-radius:10px; text-align:center; margin-bottom:10px; margin-top:0px;">Flora Advisor: Professional Plant Matchmaking</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="main-content">
        <div class="questions">
            <h2 style="color:#b8860b; font-weight:900; font-size:2em;">Welcome to Flora Advisor! Our goal is to help you find the perfect plants to complement your garden. 
            Please provide the details below to receive tailored recommendations.</h2>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hard-coded API key
api_key = 'sk-YQBH66a1954d5a0d66318'  # Updated API key

# Number of plants to display
num_plants = st.slider('Number of plants to display:', min_value=1, max_value=5, value=3)

# Layout for questions
col1, col2 = st.columns(2)

with col1:
    sun_level = st.selectbox('What is the sun exposure level?',
                             ['Full Shade', 'Part Shade', 'A Mix of Sun and Shade', 'Full Sun'])
    growth_rate = st.selectbox('Growth rate:',
                               ['High', 'Moderate', 'Low'])

with col2:
    water_frequency = st.selectbox('How often do you water your plants?',
                                   ['Frequently', 'Average', 'Minimal'])
    st.write('Note: If you have an automatic sprinkler system, select based on its settings.')
    drought_tolerant = st.checkbox('Include only drought-tolerant plants?')

# Add multiselect for additional questions
additional_details = st.multiselect(
    "Would you like to share more details for a customized recommendation?",
    options=['Propagation', 'Maintenance Level', 'Salt Tolerant'],
    default=[]
)

# Initialize variables to avoid NameError
propagation = ''
maintenance = ''
salt_tolerant = ''

# Conditional questions based on multiselect
if 'Propagation' in additional_details:
    propagation = st.selectbox('Propagation:', ['Seed', 'Stem', 'Layering', 'Division'])
if 'Maintenance Level' in additional_details:
    maintenance = st.selectbox('Maintenance Level:', ['Low', 'Moderate', 'High'])
if 'Salt Tolerant' in additional_details:
    salt_tolerant = st.selectbox('Salt Tolerant:', ['Yes', 'No'])

if st.button('Find Plants'):
    st.write("Fetching plant data from the API...")
    plant_data = get_plants_by_criteria(api_key, sun_level, water_frequency, growth_rate, propagation, maintenance, drought_tolerant, salt_tolerant)

    if plant_data is None:
        st.error("Failed to fetch data from the API. Please try again later.")
    elif 'data' in plant_data:
        plants = []
        for plant in plant_data['data']:
            plants.append({
                'Common Name': plant.get('common_name', 'N/A'),
                'Watering': plant.get('watering', 'N/A'),
                'Sunlight': ', '.join(plant.get('sunlight', [])),
                'Image': plant.get('default_image', {}).get('regular_url', '') if plant.get('default_image') else ''
            })

        # Limit the number of plants displayed
        plants = plants[:num_plants]

        if plants:
            df = pd.DataFrame(plants)

            # Convert image URLs to HTML <img> tags
            def path_to_image_html(path):
                return f'<img src="{path}" width="60" >'

            df = df[['Common Name', 'Watering', 'Sunlight', 'Image']]

            st.write(df.to_html(escape=False, formatters=dict(Image=path_to_image_html), index=False), unsafe_allow_html=True)

            # Calculate the average number of letters in common names using numpy
            common_name_lengths = np.array([len(name) for name in df['Common Name']])
            average_length = np.mean(common_name_lengths)
            st.write(f"Average number of letters in common names: {average_length:.2f}")

            # Embed the interactive GIF next to the success box
            st.success("Plant data fetched successfully!")
            st.markdown("""
                <iframe src="https://giphy.com/embed/MiVQ9nedzQ7HiQ2ShD" width="480" height="480" style="margin-left:10px;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
                <p><a href="https://giphy.com/stickers/FIU-fiu-fiuroary-roaryfiu-MiVQ9nedzQ7HiQ2ShD">via GIPHY</a></p>
            """, unsafe_allow_html=True)
        else:
            st.error("No plants found for the specified criteria.")
    else:
        st.error("No plant data fetched from the API.")
