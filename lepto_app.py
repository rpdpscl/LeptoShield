import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from googletrans import Translator

# Initialize the translator
translator = Translator()

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
    'axes.titlecolor': 'gray',
})

# Add custom CSS for Streamlit theme with adjustments for title, description, and spacing
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
        font-size: 36px;  /* Larger font size for the LeptoShield title */
        margin-top: 20px;
        text-align: center;  /* Center the title */
    }
    p {
        color: #3d3d3d;
        font-size: 14px;  /* Smaller font size for the description */
        line-height: 1.4;
        opacity: 0.8;  /* Slightly lower opacity for the description */
        margin-bottom: 10px;  /* Reduce the space after the description */
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h2 {
        margin-top: 20px;  /* Reduce the space between description and City Insights */
    }
    .stMarkdown {
        margin-bottom: 10px;  /* Adjust margin to reduce space between sections */
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
        lepto_df['week'] = lepto_df['date'].dt.isocalendar().week

except FileNotFoundError:
    st.error("The file 'lepto_dfclean.csv' was not found. Please upload the correct file and ensure the path is correct.")
except pd.errors.EmptyDataError:
    st.error("The file 'lepto_dfclean.csv' is empty. Please check the contents of the file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# Define available dialects and their corresponding Googletrans language codes
language_codes = {
    "English": "en",
    "Tagalog": "tl",
    "Cebuano (Bisaya)": "ceb"
}

# Add a function to translate the text based on selected language
def translate_text(text, language):
    try:
        lang_code = language_codes.get(language)
        if lang_code:
            if lang_code == "en":  # No translation needed for English
                return text
            translated = translator.translate(text, dest=lang_code)
            return translated.text
        else:
            st.warning(f"Translation for {language} is not supported. Defaulting to Tagalog.")
            translated = translator.translate(text, dest='tl')  # Use Tagalog as fallback
            return translated.text
    except Exception as e:
        st.warning(f"Translation error: {e}")
        return text

if 'lepto_df' in locals() and not lepto_df.empty:
    def main():
        st.title("LeptoShield")
        
        # Display the app description and disclaimer
        description = """
        **This app helps predict and prevent leptospirosis by analyzing key risk factors and providing essential medical information through an interactive chatbot named LeptoGuide.**

        *Disclaimer: This app is for informational purposes only. Always consult with a healthcare professional for medical advice, diagnosis, or treatment.*

        **Data Source:** The data available here are sourced from the Project CCHAIN dataset.

        **Project CCHAIN:** Covers 29 tables over 20 years (2003-2022) with health, climate, environmental, and socioeconomic data for 12 Philippine cities.
        """
        
        # Display the markdown content
        st.markdown(description)

        # Other parts of the app...

        st.header("City Insights")
        st.selectbox("Select a City", lepto_df['adm3_en'].unique())
        st.selectbox("Select Language", list(language_codes.keys()))

        # More content like charts...

    if __name__ == "__main__":
        main()
