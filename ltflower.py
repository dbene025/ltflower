import streamlit as st
import requests
import pandas as pd
import numpy as np
import base64
import matplotlib.pyplot as plt

# Function to convert image to base64
def get_base64_of_image(image_file):
    return base64.b64encode(image_file.read()).decode()

# Load the uploaded images
def load_image(path):
    with open(path, "rb") as image_file:
        return get_base64_of_image(image_file)

image_path = "fiuimage.png"
favicon_path = "favicon.png"

img_base64 = load_image(image_path)
favicon_base64 = load_image(favicon_path)

# Set page configuration with the favicon
st.set_page_config(page_title="Flora Advisor", page_icon=favicon_path)

# Function to fetch plant data from Perenual API
def fetch_plant_data(api_key, plant_names):
    plant_data = {}
    for name in plant_names:
        response = requests.get(f"https://perenual.com/api/species-list?key={api_key}&q={name}")
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                plant = data[0]
                plant_data[name] = {
                    'image': plant.get('default_image', {}).get('regular_url'),
                    'watering': plant.get('watering', 'N/A'),
                    'growth_rate': plant.get('growth_rate', 'N/A'),
                    'drought_tolerant': plant.get('drought_tolerant', 'N/A')
                }
            else:
                plant_data[name] = {'image': None, 'watering': 'N/A', 'growth_rate': 'N/A', 'drought_tolerant': 'N/A'}
        else:
            plant_data[name] = {'image': None, 'watering': 'N/A', 'growth_rate': 'N/A', 'drought_tolerant': 'N/A'}
    return plant_data

# Function to fetch plants by criteria from Perenual API
def fetch_plants_by_criteria(api_key, criteria):
    url = f"https://perenual.com/api/species-list?key={api_key}&{criteria}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# List of plant names (common names)
plant_names = [
    "Coneflower", "Lantana", "Peony", "Swamp milkweed", "Flowering maple",
    "Sea thrift", "Floss flower", "Aster", "Hybrid tuberous begonia",
    "Flowering quince", "Clematis", "Siam Tulip", "Dogwood",
    "Tree Peony", "Cheddar pink", "Maiden pink", "Hardy geranium"
]

# Perenual API key
perenual_api_key = 'sk-YQBH66a1954d5a0d66318'

# Fetch plant data
plant_data = fetch_plant_data(perenual_api_key, plant_names)

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
            color: white;
            margin-top: 0px;
        }}
        .questions {{
            background-color: rgba(255, 255, 255, 0);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stSlider {{
            margin-top: 5px;
            margin-bottom: 5px;
        }}
        .stRadio {{
            display: flex;
            justify-content: center;
        }}
        table {{
            width: 100%;
            text-align: center;
        }}
        th {{
            text-align: center;
            font-weight: bold;
        }}
        td {{
            text-align: center;
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

# Number of plants to display
num_plants = st.slider('Number of plants to display:', min_value=1, max_value=5, value=3)

# Sidebar to display plant images
st.sidebar.header("Debbie's Picks")
for plant, data in plant_data.items():
    if data['image']:
        st.sidebar.image(data['image'], caption=plant, use_column_width=True)
    else:
        st.sidebar.write(f"No image found for {plant}")

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
    criteria = {
        'sun_level': sun_level,
        'water_frequency': water_frequency,
        'growth_rate': growth_rate,
        'propagation': propagation,
        'maintenance': maintenance,
        'drought_tolerant': drought_tolerant,
        'salt_tolerant': salt_tolerant
    }
    criteria_str = '&'.join(f"{key}={value}" for key, value in criteria.items() if value)
    st.write("Fetching plant data from the API...")
    plant_data = fetch_plants_by_criteria(perenual_api_key, criteria_str)

    if plant_data is None:
        st.error("Failed to fetch data from the API. Please try again later.")
    elif 'data' in plant_data:
        plants = []
        for plant in plant_data['data']:
            plants.append({
                'Common Name': plant.get('common_name', 'N/A'),
                'Watering': plant.get('watering', 'N/A'),
                'Sunlight': ', '.join(plant.get('sunlight', [])),
                'Growth Rate': plant.get('growth_rate', 'N/A'),
                'Drought Tolerant': plant.get('drought_tolerant', 'N/A'),
                'Image': plant.get('default_image', {}).get('regular_url', '') if plant.get('default_image') else ''
            })

        # Limit the number of plants displayed
        plants = plants[:num_plants]

        if plants:
            df = pd.DataFrame(plants)

            # Convert image URLs to HTML <img> tags
            def path_to_image_html(path):
                return f'<img src="{path}" width="60" >'

            df = df[['Common Name', 'Watering', 'Sunlight', 'Growth Rate', 'Drought Tolerant', 'Image']]

            st.write(df.to_html(escape=False, formatters=dict(Image=path_to_image_html), index=False), unsafe_allow_html=True)

            # Prepare data for bar chart
            watering_needs = [plant['Watering'] for plant in plants]
            watering_counts = pd.Series(watering_needs).value_counts()

            # Create smaller bar chart and invert axes
            fig, ax = plt.subplots(figsize=(3, 1.5))  # Adjust size here
            watering_counts.plot(kind='barh', ax=ax, color='fuchsia')
            ax.set_title("Number of Plants by Watering Needs", color='fuchsia')
            ax.set_xlabel("Number of Plants", color='fuchsia')
            ax.set_ylabel("Watering Needs", color='fuchsia')
            ax.tick_params(axis='x', labelsize=10, colors='fuchsia')
            ax.tick_params(axis='y', labelsize=10, colors='fuchsia')

            # Display the bar chart in Streamlit
            st.pyplot(fig)

            # Prepare data for scatter chart using Streamlit's built-in functionality
            growth_rate_map = {'High': 3, 'Moderate': 2, 'Low': 1}
            df['Growth Rate'] = df['Growth Rate'].map(growth_rate_map)
            df['Drought Tolerant'] = df['Drought Tolerant'].apply(lambda x: 1 if x == 'Yes' else 0)

            scatter_data = df[['Growth Rate', 'Drought Tolerant']]

            # Create scatter chart
            st.markdown("### Scatter Plot: Growth Rate vs. Drought Tolerance")
            fig, ax = plt.subplots(figsize=(3, 1.5))  # Adjust size here
            scatter = ax.scatter(scatter_data['Growth Rate'], scatter_data['Drought Tolerant'], color='fuchsia')
            ax.set_title("Growth Rate vs. Drought Tolerance", color='fuchsia')
            ax.set_xlabel("Growth Rate (1: Low, 2: Moderate, 3: High)", color='fuchsia')
            ax.set_ylabel("Drought Tolerant (0: No, 1: Yes)", color='fuchsia')
            ax.tick_params(axis='x', labelsize=10, colors='fuchsia')
            ax.tick_params(axis='y', labelsize=10, colors='fuchsia')
            st.pyplot(fig)

            # Display success message
            st.success("Plant data fetched and displayed successfully!")

            # Calculate the average number of letters in common names using numpy
            common_name_lengths = np.array([len(name) for name in df['Common Name']])
            average_length = np.mean(common_name_lengths)
            st.write(f"Average number of letters in common names: {average_length:.2f}")

        else:
            st.error("No plants found for the specified criteria.")
    else:
        st.error("No plant data fetched from the API.")

# Interactive sticker
st.markdown("""
<iframe src="https://giphy.com/embed/MiVQ9nedzQ7HiQ2ShD" width="240" height="240" style="border:none; margin-top:20px;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/stickers/FIU-fiu-fiuroary-roaryfiu-MiVQ9nedzQ7HiQ2ShD">via GIPHY</a></p>
""", unsafe_allow_html=True)
