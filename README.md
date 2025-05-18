# Startup Investments Analysis Dashboard

## Project Overview
This project analyzes startup investment data from Crunchbase, providing insights into funding trends, market sectors, and geographic distributions. The data is visualized through an interactive Streamlit dashboard, featuring 8 key insights. The dashboard is designed for deployment on Streamlit Cloud and is documented in this GitHub repository.

### Objectives
- Clean and preprocess the Crunchbase dataset to ensure data integrity.
- Build an interactive Streamlit app with visualizations for startup investment analysis.
- Deploy the app on Streamlit Cloud for public access.
- Provide clear documentation for setup, usage, and troubleshooting.

## Dataset
**Source**: [Kaggle: Startup Investments (Crunchbase)](https://www.kaggle.com/datasets/arindam235/startup-investments-crunchbase)  
**File**: `investments_VC.csv`  
- Download the dataset and place `investments_VC.csv` in the project root directory (`/workspaces/StartupDataDeck` or equivalent).
- **Required Columns**: `name`, `funding_total_usd`, `market`, `country_code`, `status` (among others like `region`, `category_list`).
- **Note**: If you’ve edited the CSV, ensure column names match (e.g., no spaces like `' funding_total_usd '`) and data types are consistent (e.g., `funding_total_usd` should be numeric).

## Key Insights
The dashboard provides the following visualizations:
1. **Top Markets by Total Funding**: Bar chart of total funding by market sector.
2. **Top Countries by Number of Startups**: Pie chart of startup counts by country.
3. **Funding by Startup Status**: Bar chart of funding totals by status (e.g., operating, closed).
4. **Top Regions by Funding**: Bar chart of funding by geographic region.
5. **Most Funded Startups**: Bar chart of top-funded startups by name.
6. **Funding Distribution by Market**: Pie chart of funding distribution across markets.
7. **Average Funding by Market**: Bar chart of average funding per market.
8. **Startup Status Breakdown**: Pie chart of startup status distribution.