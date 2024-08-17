import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set matplotlib's default color scheme for the plots
plt.rcParams.update({
    'axes.facecolor': 'white',         # Background of the plot
    'axes.edgecolor': '#3d3d3d',       # Border color of the plot
    'axes.labelcolor': '#19535b',      # Label color
    'xtick.color': '#19535b',          # X-axis tick color
    'ytick.color': '#19535b',          # Y-axis tick color
    'text.color': '#19535b',           # Text color in the plot
    'figure.facecolor': 'white',       # Background color outside the plot
    'figure.edgecolor': 'white',       # Edge color around the plot
    'grid.color': '#3d3d3d',           # Gridline color
    'lines.color': '#1477ea',          # Default line color
})

# Add custom CSS for Streamlit theme
st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    .stButton>button {
        background-color: #19535b;
        color: white;
    }
    .stRadio label {
        color: #19535b;
    }
    .stSelectbox label {
        color: #19535b;
    }
    .stSidebar .stRadio label {
        color: #19535b;
    }
    .stSidebar .stSelectbox label {
        color: #19535b;
    }
    </style>
""", unsafe_allow_html=True)

# Attempt to load the dataset and handle errors
try:
    lepto_df = pd.read_csv('lepto_dfclean.csv')
    if lepto_df.empty:
        st.error("The dataset is empty. Please check the CSV file.")
    else:
        # Convert the date column to datetime format
        lepto_df['date'] = pd.to_datetime(lepto_df['date'])
        lepto_df['month'] = lepto_df['date'].dt.month
        lepto_df['year'] = lepto_df['date'].dt.year

except FileNotFoundError:
    st.error("The file 'lepto_dfclean.csv' was not found. Please upload the correct file and ensure the path is correct.")
except pd.errors.EmptyDataError:
    st.error("The file 'lepto_dfclean.csv' is empty. Please check the contents of the file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# Only proceed if the dataset was loaded successfully
if 'lepto_df' in locals() and not lepto_df.empty:
    # Set up the main structure of the app
    d
