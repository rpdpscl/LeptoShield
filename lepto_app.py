import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

        # Sum cases per month for each year
        monthly_data = city_data.groupby(['year', 'month'])['case_total'].sum().reset_index()

        # Calculate the average cases per month across all years
        monthly_avg = monthly_data.groupby('month')['case_total'].mean().reset_index()

        # Visualization: Monthly Average Summary of Cases
        st.subheader(f"Average Monthly Leptospirosis Cases in {selected_city}")

        # Plotting the data
        fig, ax = plt.subplots()
        ax.plot(monthly_avg['month'], monthly_avg['case_total'], marker='o', color='blue')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Number of Cases')
        ax.set_title(f'Average Monthly Leptospirosis Cases in {selected_city}')
        
        # Highlighting peak months
        max_cases_month = monthly_avg.loc[monthly_avg['case_total'].idxmax(), 'month']
        max_cases_value = monthly_avg['case_total'].max()
        ax.annotate('Peak', xy=(max_cases_month, max_cases_value), xytext=(max_cases_month, max_cases_value + 1),
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
