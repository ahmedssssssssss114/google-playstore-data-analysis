import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# Load data
df = pd.read_csv("C:/Users/hp/Desktop/googleplaystore1.csv")



# Filter: Clean and convert columns
df = df.dropna(subset=['Installs', 'Category', 'Type', 'Content Rating', 'Android Ver', 'App', 'Size'])

# Clean 'Installs' and 'Size'
df['Installs'] = df['Installs'].str.replace('+', '', regex=False).str.replace(',', '', regex=False).astype(int)
df['Size'] = df['Size'].replace('M', '', regex=True)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
df = df.dropna(subset=['Size'])

# Clean 'Revenue' column if exists (assume you added it)
if 'Revenue' not in df.columns:
    df['Revenue'] = df['Installs'] * 0.01  # Dummy revenue

# Filter according to conditions
filtered_df = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Android Ver'].str.extract('(\d+\.\d+)', expand=False).astype(float) > 4.0) &
    (df['Size'] > 15) &
    (df['Content Rating'] == 'Everyone') &
    (df['App'].str.len() <= 30)
]

# Get top 3 categories by count
top_categories = filtered_df['Category'].value_counts().head(3).index.tolist()
filtered_df = filtered_df[filtered_df['Category'].isin(top_categories)]

# Group by Type (Free/Paid)
grouped = filtered_df.groupby(['Type']).agg({
    'Installs': 'mean',
    'Revenue': 'mean'
}).reset_index()

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
hour = now.hour

# Streamlit UI
st.title("Task 3 - Dual Axis: Installs vs Revenue")

# Time condition: only show between 1PM to 2PM IST
if 13 <= hour < 14:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grouped['Type'],
        y=grouped['Installs'],
        name='Avg Installs',
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=grouped['Type'],
        y=grouped['Revenue'],
        name='Avg Revenue',
        yaxis='y2',
        mode='lines+markers'
    ))

    # Add dual axis
    fig.update_layout(
        title="Free vs Paid Apps - Avg Installs & Revenue (Top 3 Categories)",
        xaxis=dict(title='App Type'),
        yaxis=dict(title='Avg Installs'),
        yaxis2=dict(title='Avg Revenue', overlaying='y', side='right')
    )

    st.plotly_chart(fig)
else:
    st.warning("This chart is only visible between 1 PM and 2 PM IST.")
