


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pytz

# Set IST time zone
ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)

# Time check
if not (now.hour >= 17 and now.hour < 19):
    st.warning("⛔ This chart is available only between 5 PM and 7 PM IST.")
    st.stop()

# Load datasets
df_apps = pd.read_csv("C:\\Users\\hp\\Desktop\\googleplaystore1.csv")
df_reviews = pd.read_csv("C:\\Users\\hp\\Desktop\\User Reviews (1).csv")

# Basic cleaning
df_apps.columns = df_apps.columns.str.strip()
df_reviews.columns = df_reviews.columns.str.strip()

# Clean Installs column safely
df_apps['Installs'] = (
    df_apps['Installs']
    .astype(str)
    .str.replace('[+,]', '', regex=True)
    .str.strip()
)
df_apps = df_apps[df_apps['Installs'].str.isnumeric()]
df_apps['Installs'] = df_apps['Installs'].astype(float)

# Clean and convert other columns
df_apps['Size'] = df_apps['Size'].replace('Varies with device', None)
df_apps['Size'] = df_apps['Size'].str.replace('M', '', regex=False)
df_apps['Size'] = pd.to_numeric(df_apps['Size'], errors='coerce')
df_apps['Reviews'] = pd.to_numeric(df_apps['Reviews'], errors='coerce')
df_apps['Rating'] = pd.to_numeric(df_apps['Rating'], errors='coerce')

# Merge sentiment subjectivity
df_sentiment = df_reviews.groupby('App')['Sentiment_Subjectivity'].mean().reset_index()
df_apps = pd.merge(df_apps, df_sentiment, how='left', on='App')

# Filters
categories = ['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENT']
df_filtered = df_apps[
    (df_apps['Rating'] > 3.5) &
    (df_apps['Category'].isin(categories)) &
    (df_apps['Reviews'] > 500) &
    (~df_apps['App'].str.contains('s', case=False, na=False)) &
    (df_apps['Sentiment_Subjectivity'] > 0.5) &
    (df_apps['Installs'] > 50000)
].copy()

# Translate categories
translation = {
    'BEAUTY': 'सौंदर्य (Beauty)',
    'BUSINESS': 'வணிகம் (Business)',
    'DATING': 'Partnersuche (Dating)'
}
df_filtered['Category'] = df_filtered['Category'].apply(lambda x: translation.get(x, x))

# Plotting
fig, ax = plt.subplots(figsize=(12, 7))
colors = df_filtered['Category'].apply(lambda x: 'pink' if 'GAME' in x.upper() else 'skyblue')

scatter = ax.scatter(
    df_filtered['Size'],
    df_filtered['Rating'],
    s=df_filtered['Installs'] / 10000,  # Bubble size
    alpha=0.6,
    c=colors
)

ax.set_title("App Size vs Rating (Bubble = Installs)", fontsize=16)
ax.set_xlabel("Size (MB)")
ax.set_ylabel("Average Rating")

st.pyplot(fig)

