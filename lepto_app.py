import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
lepto_df = pd.read_csv('lepto_dfclean.csv')

# Convert the date column to datetime format
lepto_df['date'] = pd.to_datetime(lepto_df['date'])

# Set up the main structure of the app
def main():
    # Header section
    st.title("Leptospirosis Risk and Response Tool")
    st.markdown("This app helps you understand and predict leptospirosis risks based on environmental factors and historical data.")
    
    # Language selector
    language = st.selectbox("Select Language", ["English", "Tagalog", "Bisaya"])
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", ["Home", "Predictors of Leptospirosis", "Historical Outbreaks", "QnA Chatbot", "Medical Facility Locator"])
    
    # Navigation to sections
    if section == "Home":
        show_home(language)
    elif section == "Predictors of Leptospirosis":
        show_predictors(language)
    elif section == "Historical Outbreaks":
        show_outbreaks(language)
    elif section == "QnA Chatbot":
        show_chatbot(language)
    elif section == "Medical Facility Locator":
        show_locator(language)

# Home section
def show_home(language):
    if language == "English":
        st.write("Welcome to the Leptospirosis Risk and Response Tool.")
    elif language == "Tagalog":
        st.write("Maligayang pagdating sa Leptospirosis Risk and Response Tool.")
    elif language == "Bisaya":
        st.write("Malipayong pag-abot sa Leptospirosis Risk and Response Tool.")

# Predictors section placeholder
def show_predictors(language):
    st.write(f"Predictors of Leptospirosis (Language: {language})")

# Historical Outbreaks section
def show_outbreaks(language):
    # City Selector
    cities = lepto_df['adm3_en'].unique()
    selected_city = st.selectbox("Select a City", cities)

    # Filter data based on the selected city
    city_data = lepto_df[lepto_df['adm3_en'] == selected_city]

    # Visualization: Historical Outbreaks
    st.subheader(f"Historical Leptospirosis Outbreaks in {selected_city}")

    # Plotting the data
    fig, ax = plt.subplots()
    ax.plot(city_data['date'], city_data['case_total'], color='blue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Cases')
    ax.set_title(f'Leptospirosis Cases Over Time in {selected_city}')
    st.pyplot(fig)

# QnA Chatbot section placeholder
def show_chatbot(language):
    st.write(f"QnA Chatbot (Language: {language})")

# Medical Facility Locator section placeholder
def show_locator(language):
    st.write(f"Medical Facility Locator (Language: {language})")

if __name__ == "__main__":
    main()
