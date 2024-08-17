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
})

# Load your dataset and filter for Iloilo
try:
    lepto_df = pd.read_csv('lepto_dfclean.csv')
    if lepto_df.empty:
        st.error("The dataset is empty. Please check the CSV file.")
    else:
        lepto_df['date'] = pd.to_datetime(lepto_df['date'])
        lepto_df['month'] = lepto_df['date'].dt.month
        lepto_df['year'] = lepto_df['date'].dt.year

        # Filter for Iloilo
        iloilo_data = lepto_df[lepto_df['adm3_en'] == 'Iloilo']

except FileNotFoundError:
    st.error("The file 'lepto_dfclean.csv' was not found. Please upload the correct file and ensure the path is correct.")
except pd.errors.EmptyDataError:
    st.error("The file 'lepto_dfclean.csv' is empty. Please check the contents of the file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

if 'iloilo_data' in locals() and not iloilo_data.empty:
    def main():
        st.title("Iloilo Insights")
        st.markdown("This section provides insights into leptospirosis cases in Iloilo.")

        # Visualization 1: Total Number of Cases
        st.subheader("Total Number of Cases per Month")
        monthly_cases = iloilo_data.groupby('month')['case_total'].sum().reset_index()

        # Plotting the data
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(monthly_cases['month'], monthly_cases['case_total'], color='#19535b')
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Number of Cases')
        st.pyplot(fig)

    if __name__ == "__main__":
        main()
