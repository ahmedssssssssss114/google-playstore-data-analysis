
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pytz

# Load and clean the dat
df = pd.read_csv("C:/Users/hp/Desktop/googleplaystore1.csv")

df = df.dropna(subset=['Rating', 'Reviews', 'Installs', 'Size', 'Last Updated'])

def size_to_mb(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024
    else:
        return None

df['Size_MB'] = df['Size'].apply(size_to_mb)
df = df.dropna(subset=['Size_MB'])
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(int)
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Apply filters
df = df[df['Last Updated'].dt.month == 1]
df = df[(df['Rating'] >= 4.0) & (df['Size_MB'] >= 10)]

# Aggregate
agg_df = df.groupby('Category').agg({
    'Rating': 'mean',
    'Reviews': lambda x: x.astype(int).sum(),
    'Installs': 'sum'
}).reset_index()
top10 = agg_df.sort_values(by='Installs', ascending=False).head(10)

# Time restriction (3 PM – 5 PM IST)
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
hour = now.hour

if 15 <= hour < 17:
    st.title("Top 10 App Categories: Rating vs Review Count (Jan Updates Only)")

    categories = top10['Category']
    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, top10['Rating'], width, label='Average Rating')
    ax.bar(x + width/2, top10['Reviews'] / 1e6, width, label='Total Reviews (in Millions)')

    ax.set_xlabel('App Category')
    ax.set_ylabel('Value')
    ax.set_title('Top 10 Categories by Installs')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45)
    ax.legend()

    st.pyplot(fig)
else:
    st.warning("⚠️ This chart is visible only between 3 PM and 5 PM IST.")
