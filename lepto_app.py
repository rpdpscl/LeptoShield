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
        color: #19535b;
        font-size: 12px;  /* Smaller font size for the description */
        line-height: 1.4;
        margin-bottom: 2px;  /* Reduce the space after the description */
        text-align: center;  /* Center the description text */
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h2 {
        color: #ffffff;  /* White text color for contrast */
        font-size: 25px;  /* Font size for the text */
        margin-top: 0px;  /* Reduce the space between description and City Insights */
        background-color: #19535b;  /* Solid background color */
        padding: 2px 8px;  /* Adjust padding to fit the background to the text */
        display: inline-block;  /* Ensures the background only covers the text */
        border-radius: 3px;  /* Rounded corners for a smoother look */
    }
    .stMarkdown {
        margin-bottom: 0px;  /* Adjust margin to reduce space between sections */
    }
    .stSelectbox > div > div {
        height: 30px;  /* Make the dropdowns thinner */
        font-size: 14px;  /* Adjust font size inside dropdowns */
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
        **This app predicts and prevents leptospirosis by analyzing risk factors and providing medical info via the LeptoGuide chatbot.**
        
        *Disclaimer: For informational purposes only. Always consult with a healthcare professional for medical advice, diagnosis, or treatment.*
        """
        st.markdown(description)

        st.header("City Insights")
        
        # Arrange the selectors side by side
        col1, col2 = st.columns(2)
        with col1:
            selected_city = st.selectbox("Select a City", lepto_df['adm3_en'].unique())
        with col2:
            language = st.selectbox("Select Language", list(language_codes.keys()))
        st.sidebar.title("Navigation")
        section = st.sidebar.radio("Go to", ["City Insights", "QnA Chatbot", "Medical Facility Locator"])
        
        if section == "City Insights":
            show_city_insights(selected_city, language)
        elif section == "QnA Chatbot":
            show_chatbot(language)
        elif section == "Medical Facility Locator":
            show_locator(language)
            
    def show_city_insights(selected_city, language):
        city_data = lepto_df[lepto_df['adm3_en'] == selected_city]

        # Layout for 3 columns
        col1, col2, col3 = st.columns(3)

        # Set uniform figure size
        fig_size = (4, 4)

        # Visualization 1: Average Monthly Cases
        with col1:
            monthly_data = city_data.groupby(['year', 'month'])['case_total'].sum().reset_index()
            monthly_avg = monthly_data.groupby('month')['case_total'].mean().reset_index()
            top_months = monthly_avg.sort_values(by='case_total', ascending=False).head(3)

            fig, ax = plt.subplots(figsize=fig_size)
            ax.plot(monthly_avg['month'], monthly_avg['case_total'], marker='o', color='#19535b')
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=8)
            ax.set_title('Average Monthly Cases', fontsize=14, color='gray')

            for _, row in top_months.iterrows():
                ax.plot(row['month'], row['case_total'], marker='o', color='#1477ea', markersize=8)
                month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month']) - 1]
                ax.text(row['month'] + 0.4, row['case_total'], month_abbr, color='#1477ea', ha='left', fontsize=8)

            st.pyplot(fig)

        # Visualization 2: Total Number of Cases per Year (2008-2020)
        with col2:
            yearly_cases = city_data.groupby('year')['case_total'].sum().reset_index()

            fig, ax = plt.subplots(figsize=fig_size)
            ax.bar(yearly_cases['year'], yearly_cases['case_total'], color='#19535b')
            ax.set_xticks(range(2008, 2021))
            ax.set_xticklabels([str(year)[-2:] for year in range(2008, 2021)], fontsize=8)
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

            fig, ax = plt.subplots(figsize=fig_size)
            ax.bar(weekly_counts['case_category'], weekly_counts['count'], color=['#19535b', '#d9d9d9'])
            ax.set_ylabel('Number of Weeks')
            ax.set_title('Weeks With/Without Cases', fontsize=14, color='gray')
            st.pyplot(fig)

    def show_chatbot(language):
        # Placeholder for chatbot section
        chatbot_text = "This is the chatbot section. You can ask questions about leptospirosis here."
        translated_chatbot_text = translate_text(chatbot_text, language)
        st.write(translated_chatbot_text)

    def show_locator(language):
        # Placeholder for medical facility locator section
        locator_text = "This section will help you locate the nearest medical facilities."
        translated_locator_text = translate_text(locator_text, language)
        st.write(translated_locator_text)

    if __name__ == "__main__":
        main()
