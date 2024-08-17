import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Set the page configuration (title only, no icon)
st.set_page_config(page_title="LeptoShield", layout="centered")

# Set matplotlib's default color scheme for the plots
plt.rcParams.update({
    'axes.facecolor': 'white',
    'axes.edgecolor': '#3d3d3d',
    'axes.labelcolor': 'gray',
    'xtick.color': 'gray',
    'ytick.color': 'gray',
    'text.color': '#19535b',
    'figure.facecolor': 'white',
    'figure.edgecolor': 'white',
    'grid.color': '#3d3d3d',
    'lines.color': '#19535b',
})

# Add custom CSS for Streamlit theme, including white page title
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
    .stRadio label, .stSelectbox label {
        color: #19535b;
    }
    .css-18e3th9 {
        color: white !important;
    }
    h1 {
        color: #19535b !important;
        font-family: 'Arial', sans-serif;
        font-size: 32px;  /* Adjusted font size */
        margin-top: 20px;  /* Add margin to prevent chopping */
    }
    h2 {
        font-size: 24px;  /* Make chart title smaller */
    }
    p {
        color: #3d3d3d;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .css-1lcbmhc {
        display: flex;
        justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)

# Load your dataset and handle errors
try:
    lepto_df = pd.read_csv('lepto_dfclean.csv')
    if lepto_df.empty:
        st.error("The dataset is empty. Please check the CSV file.")
    else:
        lepto_df['date'] = pd.to_datetime(lepto_df['date'])
        lepto_df['month'] = lepto_df['date'].dt.month
        lepto_df['year'] = lepto_df['date'].dt.year

except FileNotFoundError:
    st.error("The file 'lepto_dfclean.csv' was not found. Please upload the correct file and ensure the path is correct.")
except pd.errors.EmptyDataError:
    st.error("The file 'lepto_dfclean.csv' is empty. Please check the contents of the file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

if 'lepto_df' in locals() and not lepto_df.empty:
    def main():
        st.title("City Insights")
        st.markdown("This app helps you understand and predict leptospirosis risks based on environmental factors and historical data.")
        
        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Select Language", ["English", "Tagalog", "Bisaya"])
        with col2:
            selected_city = st.selectbox("Select a City", lepto_df['adm3_en'].unique())

        st.sidebar.title("Navigation")
        section = st.sidebar.radio("Go to", ["City Insights", "QnA Chatbot", "Medical Facility Locator"])
        
        if section == "City Insights":
            show_city_insights(selected_city)
        elif section == "QnA Chatbot":
            show_chatbot(language)
        elif section == "Medical Facility Locator":
            show_locator(language)

    def show_city_insights(selected_city):
        city_data = lepto_df[lepto_df['adm3_en'] == selected_city]
        
        # Visualization 1: Average Monthly Cases
        st.subheader(f"{selected_city} Ave Monthly Cases")
        monthly_data = city_data.groupby(['year', 'month'])['case_total'].sum().reset_index()
        monthly_avg = monthly_data.groupby('month')['case_total'].mean().reset_index()
        top_months = monthly_avg.sort_values(by='case_total', ascending=False).head(3)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(monthly_avg['month'], monthly_avg['case_total'], marker='o', color='#19535b')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Number of Cases')
        
        # Highlight top 3 months with a smaller marker and add month labels (3-letter abbreviations)
        for _, row in top_months.iterrows():
            ax.plot(row['month'], row['case_total'], marker='o', color='#1477ea', markersize=8)
            month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month']) - 1]
            ax.text(row['month'], row['case_total'] + 0.2, month_abbr, color='blue', ha='center')

        st.pyplot(fig)
        
        # Visualization 2: Total Number of Cases per Month
        st.subheader("Total Number of Cases per Month")
        monthly_cases = city_data.groupby('month')['case_total'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(monthly_cases['month'], monthly_cases['case_total'], color='#19535b')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Number of Cases')
        st.pyplot(fig)

    def show_chatbot(language):
        st.write(f"QnA Chatbot (Language: {language})")

    def show_locator(language):
        st.write(f"Medical Facility Locator (Language: {language})")

    if __name__ == "__main__":
        main()
