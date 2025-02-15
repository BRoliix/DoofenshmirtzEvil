import streamlit as st
import pandas as pd
import requests

st.title("Email Click Tracking Stats")

# Attempt to fetch tracking stats from the Flask endpoint
try:
    response = requests.get("http://localhost:5000/stats")
    response.raise_for_status()
    stats = response.json()
    
    if stats:
        df = pd.DataFrame(stats)
        st.dataframe(df)  # Displays an interactive table
    else:
        st.write("No click events recorded yet.")
except Exception as e:
    st.error(f"Error fetching stats: {e}")
