import streamlit as st
import pandas as pd
import numpy as np

import csv

st.write("# My first app\nHello *world!*")

df = pd.read_csv("investments_VC.csv", encoding="latin1")

# Debugging: Show the DataFrame
st.write("### Data Preview", df.head())  # Display first few rows
st.write("### Data Types", df.dtypes)  # Show column types

# Ensure numeric data
df = df.apply(pd.to_numeric, errors="coerce")

# Drop missing values
df.dropna(inplace=True)

# Plot the chart
st.line_chart(df)
