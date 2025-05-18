import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Startup Investments Dashboard", layout="wide")

# Title and description
st.title("Startup Investments Analysis Dashboard")
st.markdown("""
This dashboard provides insights into startup investments based on Crunchbase data.
Use the filters below to explore the data interactively.
""")

st.write("")
st.write("")

# Load data
@st.cache_data
def load_data():
    try:
        # Check if file exists
        if not os.path.exists("investments_VC.csv"):
            raise FileNotFoundError("investments_VC.csv not found in the project directory.")

        # Try loading with different encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1']
        for encoding in encodings:
            try:
                df = pd.read_csv("investments_VC.csv", encoding=encoding)
                # Strip spaces from column names
                df.columns = df.columns.str.strip()
                # Verify required columns
                required_columns = ['name', 'funding_total_usd', 'market', 'country_code', 'status']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    raise ValueError(f"Missing required columns: {missing_columns}")

                # Data cleaning
                df = df.dropna(subset=['name', 'funding_total_usd', 'market'])
                df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'].replace('[\$,]', '', regex=True), errors='coerce')
                df = df[df['funding_total_usd'] > 0]
                # Standardize market and category_list
                df['market'] = df['market'].str.strip().str.lower()
                df['category_list'] = df['category_list'].fillna('').str.split('|').apply(lambda x: [i.strip().lower() for i in x if i])
                # Clean country_code and status
                df['country_code'] = df['country_code'].fillna('Unknown').astype(str).str.strip()
                df['status'] = df['status'].fillna('Unknown').astype(str).str.strip()
                return df
            except UnicodeDecodeError:
                continue

        # Fallback: load with error handling
        df = pd.read_csv("investments_VC.csv", encoding='latin1', errors='ignore')
        df.columns = df.columns.str.strip()
        required_columns = ['name', 'funding_total_usd', 'market', 'country_code', 'status']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        df = df.dropna(subset=['name', 'funding_total_usd', 'market'])
        df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'].replace('[\$,]', '', regex=True), errors='coerce')
        df = df[df['funding_total_usd'] > 0]
        df['market'] = df['market'].str.strip().str.lower()
        df['category_list'] = df['category_list'].fillna('').str.split('|').apply(lambda x: [i.strip().lower() for i in x if i])
        df['country_code'] = df['country_code'].fillna('Unknown').astype(str).str.strip()
        df['status'] = df['status'].fillna('Unknown').astype(str).str.strip()
        return df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.markdown("""
    **No data loaded.** Please check the following:
    - Ensure `investments_VC.csv` is in the same directory as `app.py`.
    - Verify the file is not corrupted (open it in a text editor or Excel).
    - Confirm the dataset contains columns: `name`, `funding_total_usd`, `market`, `country_code`, `status`.
    - Check column names:
      ```python
      import pandas as pd
      df = pd.read_csv("investments_VC.csv", encoding='latin1')
      print(df.columns.tolist())
      ```
    - If encoding issues persist, convert to UTF-8:
      ```python
      import pandas as pd
      df = pd.read_csv("investments_VC.csv", encoding='latin1')
      df.to_csv("investments_VC_utf8.csv", encoding='utf-8', index=False)
      ```
    """)
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
markets = st.sidebar.multiselect("Select Markets", options=sorted(df['market'].unique()), default=df['market'].unique()[:3])
countries = st.sidebar.multiselect("Select Countries", options=sorted(df['country_code'].unique()), default=['USA', 'CHN', 'GBR'])
min_funding = float(df['funding_total_usd'].min())
max_funding = float(df['funding_total_usd'].max())
funding_range = st.sidebar.slider("Select Funding Range (USD)", min_funding, max_funding, (min_funding, max_funding/10))
statuses = st.sidebar.multiselect("Select Status", options=sorted(df['status'].unique()), default=df['status'].unique())

# Filter data
filtered_df = df[
    (df['market'].isin(markets)) &
    (df['country_code'].isin(countries)) &
    (df['funding_total_usd'].between(funding_range[0], funding_range[1])) &
    (df['status'].isin(statuses))
]

# Layout
col1, col2 = st.columns(2)

# Insight 1: Top Markets by Funding
with col1:
    st.subheader("Top Markets by Total Funding")
    market_funding = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    fig1 = px.bar(x=market_funding.values, y=market_funding.index, orientation='h', title="Top 10 Markets by Funding")
    fig1.update_layout(xaxis_title="Total Funding (USD)", yaxis_title="Market")
    st.plotly_chart(fig1, use_container_width=True)

# Insight 2: Top Countries by Number of Startups
with col2:
    st.subheader("Top Countries by Number of Startups")
    country_counts = filtered_df['country_code'].value_counts().head(10)
    fig2 = px.pie(values=country_counts.values, names=country_counts.index, title="Top 10 Countries")
    st.plotly_chart(fig2, use_container_width=True)

# Insight 3: Funding by Status
st.subheader("Funding by Startup Status")
status_funding = filtered_df.groupby('status')['funding_total_usd'].sum()
fig3 = px.bar(x=status_funding.index, y=status_funding.values, title="Total Funding by Status")
fig3.update_layout(xaxis_title="Status", yaxis_title="Total Funding (USD)")
st.plotly_chart(fig3, use_container_width=True)

# Insight 4: Top Regions by Funding
with col1:
    st.subheader("Top Regions by Funding")
    region_funding = filtered_df.groupby('region')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    fig4 = px.bar(x=region_funding.index, y=region_funding.values, title="Top 10 Regions by Funding")
    fig4.update_layout(xaxis_title="Region", yaxis_title="Total Funding (USD)")
    st.plotly_chart(fig4, use_container_width=True)

# Insight 5: Most Funded Startups
with col2:
    st.subheader("Most Funded Startups")
    top_startups = filtered_df.groupby('name')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    fig5 = px.bar(x=top_startups.index, y=top_startups.values, title="Top 10 Funded Startups")
    fig5.update_layout(xaxis_title="Startup", yaxis_title="Total Funding (USD)")
    st.plotly_chart(fig5, use_container_width=True)

# Insight 6: Funding by Market
st.subheader("Funding Distribution by Market")
market_dist = filtered_df.groupby('market')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
fig6 = px.pie(values=market_dist.values, names=market_dist.index, title="Funding Distribution by Market")
st.plotly_chart(fig6, use_container_width=True)

# Insight 7: Average Funding by Market
with col1:
    st.subheader("Average Funding by Market")
    avg_market_funding = filtered_df.groupby('market')['funding_total_usd'].mean().sort_values(ascending=False).head(10)
    fig7 = px.bar(x=avg_market_funding.index, y=avg_market_funding.values, title="Top 10 Markets by Average Funding")
    fig7.update_layout(xaxis_title="Market", yaxis_title="Average Funding (USD)")
    st.plotly_chart(fig7, use_container_width=True)

# Insight 8: Status Breakdown
with col2:
    st.subheader("Startup Status Breakdown")
    status_counts = filtered_df['status'].value_counts()
    fig8 = px.pie(values=status_counts.values, names=status_counts.index, title="Status Distribution")
    st.plotly_chart(fig8, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made By Shantanu Pandya | Data Source: Crunchbase | Deployed on Streamlit Cloud")