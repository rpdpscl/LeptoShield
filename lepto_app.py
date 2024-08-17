import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
lepto_df = pd.read_csv('lepto_dfclean.csv')

# Convert the date column to datetime format
lepto_df['date'] = pd.to_datetime(lepto_df['date'])

# Extract the month from the date
lepto_df['month'] = lepto_df['date'].dt.month

# Set up the main structure of the app
def main():
    # Header section
    st.title("Leptospirosis Risk and Response Tool")
    st.markdown("This app helps you understand and predict leptospirosis risks based on environmental factors and historical data.")
    
    # Language selector
    language = st.selectbox("Select Language", ["English", "Tagalog", "Bisaya"])
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", ["City Insights", "QnA Chatbot", "Medical Facility Locator"])
    
    # Navigation to sections
    if section == "City Insights":
        show_city_insights(language)
    elif section == "QnA Chatbot":
        show_chatbot(language)
    elif section == "Medical Facility Locator":
        show_locator(language)

# City Insights section (formerly Historical Outbreaks)
def show_city_insights(language):
    # City Selector
    cities = lepto_df['adm3_en'].unique()
    selected_city = st.selectbox("Select a City", cities)

    # Filter data based on the selected city
    city_data = lepto_df[lepto_df['adm3_en'] == selected_city]

    # Aggregate data by month
    monthly_summary = city_data.groupby('month')['case_total'].sum().reset_index()

    # Visualization: Monthly Summary of Cases
    st.subheader(f"Monthly Leptospirosis Case Summary in {selected_city}")

    # Plotting the data
    fig, ax = plt.subplots()
    ax.plot(monthly_summary['month'], monthly_summary['case_total'], marker='o', color='blue')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Cases')
    ax.set_title(f'Monthly Leptospirosis Cases in {selected_city}')
    
    # Highlighting peak months
    max_cases_month = monthly_summary.loc[monthly_summary['case_total'].idxmax(), 'month']
    max_cases_value = monthly_summary['case_total'].max()
    ax.annotate('Peak', xy=(max_cases_month, max_cases_value), xytext=(max_cases_month, max_cases_value + 100),
                arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12, color='red')
    
    st.pyplot(fig)

# QnA Chatbot section placeholder
def show_chatbot(language):
    st.write(f"QnA Chatbot (Language: {language})")

# Medical Facility Locator section placeholder
def show_locator(language):
    st.write(f"Medical Facility Locator (Language: {language})")

if __name__ == "__main__":
    main()
