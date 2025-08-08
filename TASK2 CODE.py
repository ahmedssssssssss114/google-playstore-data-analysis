import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Title
st.title("📍 App Locations Map by Installs and Ratings")

# Load CSV file (correct Windows path with raw string)
df = pd.read_csv("C:\\Users\\hp\\Desktop\\NULL CLASS PROJECT\\googleplaystore1.csv")

# Drop rows with missing critical values
df.dropna(subset=['Rating', 'Installs', 'Category', 'Type'], inplace=True)

# 🔧 Clean Installs column (remove +, commas, and filter out non-numeric entries)
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
df = df[df['Installs'].str.isnumeric()]  # Keep only numeric entries
df['Installs'] = df['Installs'].astype(int)

# ✅ Keep only apps with Rating > 4
df = df[df['Rating'] > 4]

# --- UI Filters ---
st.sidebar.header("🔍 Filters")
selected_category = st.sidebar.multiselect("Select Categories", options=df['Category'].unique(), default=df['Category'].unique())
selected_type = st.sidebar.selectbox("Select App Type", ['All', 'Free', 'Paid'])

# Apply filters
filtered_df = df[df['Category'].isin(selected_category)]
if selected_type != 'All':
    filtered_df = filtered_df[filtered_df['Type'] == selected_type]

# Top/Bottom 10 by installs
install_view = st.sidebar.radio("Select View", ['Top 10 Installs', 'Bottom 10 Installs'])

if install_view == 'Top 10 Installs':
    map_df = filtered_df.nlargest(10, 'Installs')
else:
    map_df = filtered_df.nsmallest(10, 'Installs')

# Simulated country coordinates (for visual purpose)
countries = ['India', 'United States', 'United Kingdom', 'Germany', 'France', 'Japan', 'South Korea', 'Canada', 'China', 'Australia']
country_coords = {
    'India': [20.5937, 78.9629],
    'United States': [37.0902, -95.7129],
    'United Kingdom': [55.3781, -3.4360],
    'Germany': [51.1657, 10.4515],
    'France': [46.6034, 1.8883],
    'Japan': [36.2048, 138.2529],
    'South Korea': [35.9078, 127.7669],
    'Canada': [56.1304, -106.3468],
    'China': [35.8617, 104.1954],
    'Australia': [-25.2744, 133.7751]
}

# Assign random countries (only if no country data available in CSV)
map_df['Country'] = random.choices(countries, k=len(map_df))
map_df['Latitude'] = map_df['Country'].apply(lambda x: country_coords[x][0])
map_df['Longitude'] = map_df['Country'].apply(lambda x: country_coords[x][1])

# Plot the map
fig = px.scatter_mapbox(
    map_df,
    lat='Latitude',
    lon='Longitude',
    hover_name='App',
    size='Installs',
    color='Rating',
    color_continuous_scale='Viridis',
    zoom=1,
    height=600,
    mapbox_style="open-street-map"
)

st.plotly_chart(fig)


