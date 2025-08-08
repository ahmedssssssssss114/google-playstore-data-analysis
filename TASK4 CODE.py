
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load data
df = pd.read_csv("C:\\Users\\hp\\Desktop\\NULL CLASS PROJECT\\googleplaystore1.csv")

# Convert Reviews column to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Remove rows with NaN in Reviews
df = df.dropna(subset=['Reviews'])

# Filter reviews > 500
df = df[df['Reviews'] > 500]

# Exclude apps starting with x, y, z or containing 'S'
df = df[~df['App'].str.startswith(('x', 'y', 'z'))]
df = df[~df['App'].str.contains('S', case=False, na=False)]

# Filter categories starting with E, C, B
df = df[df['Category'].str.startswith(('E', 'C', 'B'))]

# Multilingual translation for categories
translations = {
    "E": "Education (Educación, Éducation)",
    "C": "Communication (Comunicación, Communication)",
    "B": "Business (Negocios, Affaires)"
}
df['Category_Translated'] = df['Category'].map(lambda x: translations.get(x[0], x))

# Convert Last Updated to datetime
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Time restriction: Show chart only between 6 PM IST and 9 PM IST
current_time_utc = datetime.utcnow()
current_hour_ist = (current_time_utc.hour + 5) % 24  # IST offset (+5:30 → +5 for hour)
if current_hour_ist >= 18 and current_hour_ist <= 21:
    fig = px.line(df, x='Last Updated', y='Installs', color='Category_Translated',
                  title="Installs Over Time by Category (Filtered)",
                  labels={'Installs': 'Number of Installs', 'Last Updated': 'Date'})
    fig.update_layout(xaxis_title="Date", yaxis_title="Installs")
    st.plotly_chart(fig)
else:
    st.warning("This chart is only visible between 6 PM IST and 9 PM IST.")
