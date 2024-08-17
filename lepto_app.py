import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    'axes.titlecolor': 'gray',  # Set chart title color to gray
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
        lepto_df['week'] = lepto_df['date'].dt.isocalendar().week

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

        # Layout for 3 columns
        col1, col2, col3 = st.columns(3)

        # Visualization 1: Average Monthly Cases
        with col1:
            monthly_data = city_data.groupby(['year', 'month'])['case_total'].sum().reset_index()
            monthly_avg = monthly_data.groupby('month')['case_total'].mean().reset_index()
            top_months = monthly_avg.sort_values(by='case_total', ascending=False).head(3)

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.plot(monthly_avg['month'], monthly_avg['case_total'], marker='o', color='#19535b')
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=8)
            ax.set_xlabel('Month')
            ax.set_ylabel('Average Number of Cases')
            ax.set_title('Average Monthly Cases', fontsize=14, color='gray')
            for _, row in top_months.iterrows():
                ax.plot(row['month'], row['case_total'], marker='o', color='#1477ea', markersize=8)
                month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month']) - 1]
                ax.text(row['month'], row['case_total'] + 5, month_abbr, color='#1477ea', ha='center', fontsize=10)  # Adjusted text position and color

            st.pyplot(fig)

        # Visualization 2: Total Number of Cases per Year (2008-2020)
        with col2:
            yearly_cases = city_data.groupby('year')['case_total'].sum().reset_index()

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.bar(yearly_cases['year'], yearly_cases['case_total'], color='#19535b')
            ax.set_xticks(range(2008, 2021))
            ax.set_xticklabels([str(year)[-2:] for year in range(2008, 2021)], fontsize=8)
            ax.set_xlabel('Year')
            ax.set_ylabel('Total Number of Cases')
            ax.set_title('Total Cases Per Year (2008-2020)', fontsize=14, color='gray')
            st.pyplot(fig)
        
        # Visualization 3: Weeks with Cases vs. Weeks without Cases
        with col3:
            case_counts = city_data['case_total'].apply(lambda x: 'With Case' if x > 0 else 'Without Case').value_counts()
            with_case_count = case_counts.get('With Case', 0)
            without_case_count = case_counts.get('Without Case', 0)

            # Prepare data for plotting
            weekly_counts = pd.DataFrame({
                'case_category': ['With Cases', 'Without Cases'],
                'count': [with_case_count, without_case_count]
            })

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.bar(weekly_counts['case_category'], weekly_counts['count'], color=['#19535b', '#3d3d3d'])
            ax.set_ylabel('Number of Weeks')
            ax.set_title('Weeks With/Without Cases', fontsize=14, color='gray')
            st.pyplot(fig)

    def show_chatbot(language):
        st.write(f"QnA Chatbot (Language: {language})")

    def show_locator(language):
        st.write(f"Medical Facility Locator (Language: {language})")

    if __name__ == "__main__":
        main()
