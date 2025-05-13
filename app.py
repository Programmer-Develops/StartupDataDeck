import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('investments_VC.csv')
    
    # Clean funding amounts (remove commas and convert to float)
    df['funding_total_usd'] = df['funding_total_usd'].str.replace(',', '').str.replace('"', '').str.strip()
    df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')
    
    # Clean date columns
    date_cols = ['founded_at', 'first_funding_at', 'last_funding_at']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract year from founded date
    df['founded_year'] = df['founded_at'].dt.year
    
    # Clean market column
    df['market'] = df['market'].str.strip()
    
    return df

df = load_data()

# Dashboard title
st.title('Venture Capital Investments Dashboard')
st.markdown("""
This dashboard provides insights into venture capital investments from the dataset.
Explore the data using the filters and visualizations below.
""")

# Sidebar filters
st.sidebar.header('Filters')

# Market filter
market_list = ['All'] + sorted(df['market'].dropna().unique().tolist())
selected_market = st.sidebar.selectbox('Select Market', market_list)

# Status filter
status_list = ['All'] + sorted(df['status'].dropna().unique().tolist())
selected_status = st.sidebar.selectbox('Select Status', status_list)

# Country filter
country_list = ['All'] + sorted(df['country_code'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox('Select Country', country_list)

# Year range filter
min_year = int(df['founded_year'].min())
max_year = int(df['founded_year'].max())
year_range = st.sidebar.slider(
    'Select Founded Year Range',
    min_year, max_year, (min_year, max_year)
)

# Apply filters
filtered_df = df.copy()
if selected_market != 'All':
    filtered_df = filtered_df[filtered_df['market'] == selected_market]
if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['status'] == selected_status]
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country_code'] == selected_country]
filtered_df = filtered_df[
    (filtered_df['founded_year'] >= year_range[0]) & 
    (filtered_df['founded_year'] <= year_range[1])
]

# Key metrics
st.subheader('Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Companies", filtered_df.shape[0])
col2.metric("Total Funding (USD)", f"${filtered_df['funding_total_usd'].sum():,.0f}")
col3.metric("Average Funding (USD)", f"${filtered_df['funding_total_usd'].mean():,.0f}")
col4.metric("Median Funding (USD)", f"${filtered_df['funding_total_usd'].median():,.0f}")

# Top markets by funding
st.subheader('Top Markets by Total Funding')
market_funding = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
fig1 = px.bar(
    market_funding, 
    x=market_funding.values, 
    y=market_funding.index,
    orientation='h',
    labels={'x': 'Total Funding (USD)', 'y': 'Market'},
    title='Top 10 Markets by Total Funding'
)
st.plotly_chart(fig1, use_container_width=True)

# Funding over time
st.subheader('Funding Over Time')
time_group = st.radio(
    "Group by:",
    ('Year', 'Quarter'),
    horizontal=True
)

if time_group == 'Year':
    funding_over_time = filtered_df.groupby(filtered_df['founded_at'].dt.year)['funding_total_usd'].sum().reset_index()
    funding_over_time.columns = ['Year', 'Total Funding']
    fig2 = px.line(
        funding_over_time, 
        x='Year', 
        y='Total Funding',
        title='Total Funding by Founding Year'
    )
else:
    filtered_df['founded_quarter'] = filtered_df['founded_at'].dt.to_period('Q').astype(str)
    funding_over_time = filtered_df.groupby('founded_quarter')['funding_total_usd'].sum().reset_index()
    funding_over_time.columns = ['Quarter', 'Total Funding']
    fig2 = px.line(
        funding_over_time, 
        x='Quarter', 
        y='Total Funding',
        title='Total Funding by Founding Quarter'
    )
st.plotly_chart(fig2, use_container_width=True)

# Status distribution
st.subheader('Company Status Distribution')
status_counts = filtered_df['status'].value_counts()
fig3 = px.pie(
    status_counts,
    values=status_counts.values,
    names=status_counts.index,
    title='Company Status Distribution'
)
st.plotly_chart(fig3, use_container_width=True)

# Top countries by funding
st.subheader('Top Countries by Total Funding')
country_funding = filtered_df.groupby('country_code')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
fig4 = px.bar(
    country_funding, 
    x=country_funding.values, 
    y=country_funding.index,
    orientation='h',
    labels={'x': 'Total Funding (USD)', 'y': 'Country Code'},
    title='Top 10 Countries by Total Funding'
)
st.plotly_chart(fig4, use_container_width=True)

# Funding by round type
st.subheader('Funding by Round Type')
round_types = ['seed', 'venture', 'equity_crowdfunding', 'undisclosed', 
               'convertible_note', 'debt_financing', 'angel', 'grant', 
               'private_equity', 'post_ipo_equity']
round_funding = filtered_df[round_types].sum().sort_values(ascending=False)
fig5 = px.bar(
    round_funding,
    x=round_funding.values,
    y=round_funding.index,
    orientation='h',
    labels={'x': 'Total Funding (USD)', 'y': 'Round Type'},
    title='Total Funding by Round Type'
)
st.plotly_chart(fig5, use_container_width=True)

# Top funded companies
st.subheader('Top 10 Funded Companies')
top_companies = filtered_df.nlargest(10, 'funding_total_usd')[['name', 'market', 'country_code', 'funding_total_usd']]
top_companies = top_companies.sort_values('funding_total_usd', ascending=True)
fig6 = px.bar(
    top_companies,
    x='funding_total_usd',
    y='name',
    orientation='h',
    color='market',
    labels={'x': 'Total Funding (USD)', 'y': 'Company Name'},
    title='Top 10 Companies by Funding Amount'
)
st.plotly_chart(fig6, use_container_width=True)

# Data table
st.subheader('Investment Data')
st.dataframe(filtered_df.sort_values('funding_total_usd', ascending=False), height=300)

# Download button
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='vc_investments_filtered.csv',
    mime='text/csv'
)