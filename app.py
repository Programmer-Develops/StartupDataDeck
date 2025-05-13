import streamlit as st
import pandas as pd
import numpy as np

import csv

st.write("""
# My first app
Hello *world!*
""")
 
df = pd.read_csv("investments_VC.csv")
st.line_chart(df)