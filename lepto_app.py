import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

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
        color: #3d3d3d;  /* Set the color to #3d3d3d */
        font-size: 4px;  /* Match font size with dropdowns */
        margin-bottom: 0px;  /* Bring labels closer to the dropdown */
    }
    .css-18e3th9 {
        color: white !important;
    }
    h1, p, h2, h3 {
        font-family: 'Arial', sans-serif;
    }
    h1 {
        color: #19535b !important;
        font-size: 36px;
        margin-top: -5px;  /* Reduced top margin to remove extra space above LeptoShield */
        margin-bottom: 0px;
        text-align: center;
    }
    p {
        color: #19535b;
        font-size: 10px;
        line-height: 1.4;
        margin-bottom: 5px;
        text-align: center;
    }
    h2 {
        color: #ffffff;
        font-size: 25px;
        margin-top: 10px;
        background-color: #19535b;
        padding: 2px 8px;
        padding-left: 25px;
        display: inline-block;
        border-radius: 3px;
    }
    h3 {
        text-decoration: underline;
        font-weight: bold;
        margin-top: 0px;  /* Reduce space above City Name */
        font-size: 14px;
        color: #3d3d3d;
    }
    .info {
        font-size: 14px;
        margin-top: -10px;  /* Reduce space between dropdowns and city info */
        margin-bottom: 0px;
        line-height: 1.6;
        color: #3d3d3d; /* Matching the color of the dropdowns */
    }
    .stMarkdown {
        margin-bottom: 0px;
    }
    .stSelectbox > div > div {
        background-color: #d9d9d9;  /* Set dropdown background color */
        color: #3d3d3d;  /* Set dropdown text color */
        height: 35px;  /* Slightly increased height to prevent text from being cropped */
        font-size: 12px;  /* Consistent font size inside dropdowns */
        border: none;  /* Remove the border */
        box-shadow: none;  /* Remove any shadow that may appear as a border */
    }

    </style>
""", unsafe_allow_html=True)

# Load your dataset and handle errors
try:
    lepto_df = pd.read_csv('lepto_dfclean.csv')
    city_summary = pd.read_csv('city_summary.csv')
    
    if lepto_df.empty or city_summary.empty:
        st.error("One or more datasets are empty. Please check the CSV files.")
    else:
        lepto_df['date'] = pd.to_datetime(lepto_df['date'])
        lepto_df['month'] = lepto_df['date'].dt.month
        lepto_df['year'] = lepto_df['date'].dt.year
        lepto_df['week'] = lepto_df['date'].dt.isocalendar().week

except FileNotFoundError:
    st.error("One or more files were not found. Please upload the correct files and ensure the paths are correct.")
except pd.errors.EmptyDataError:
    st.error("One or more files are empty. Please check the contents of the files.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

if 'lepto_df' in locals() and not lepto_df.empty and 'city_summary' in locals() and not city_summary.empty:
    def main():
        st.title("LeptoShield")
        # Display the app description and disclaimer
        description = """
        **This app analyzes key risk factors for leptospirosis. It aims to assist cities in implementing timely interventions, benefiting government agencies, communities, public health professionals, and medical personnel. For informational purposes only**
        """
        st.markdown(description)

        st.header("City Insights")
        
        # Arrange the selectors side by side without labels
        col1, col2 = st.columns(2)
        with col1:
            #Alphabetize the city names before passing them to the selectbox
            sorted_cities = sorted(lepto_df['adm3_en'].unique())
            selected_city = st.selectbox("", sorted_cities)
            
        # Filter data for the selected city
        city_data = lepto_df[lepto_df['adm3_en'] == selected_city]
        city_info = city_summary[city_summary['adm3_en'] == selected_city].iloc[0]  # Get city-specific information
        
        # Update placeholders with actual data from city_summary
        city_area = f"{int(city_info['city_area']):,} sq km"
        total_population = f"{int(city_info['pop_count_total']):,} people"
        population_density = f"{int(city_info['pop_density']):,} persons per sq km"
        total_cases = f"{int(city_info['case_total']):,}"

        # Display the city-specific information
        st.markdown(f"### {selected_city}")
        st.markdown(f"""
        <div class='info'><b>Total Area:</b> {city_area}<br>
        <b>Total Population:</b> {total_population}<br>
        <b>Population Density:</b> {population_density}<br>
        <b>Total Number of Recorded Cases:</b> {total_cases} (2008-2020)</div>
        """, unsafe_allow_html=True)

        # Placeholder for Leptospirosis Cases Summary
        st.markdown("### Leptospirosis Cases Summary")
        
        # Layout for 3 columns
        col1, col2, col3 = st.columns(3)

        # Set uniform figure size
        fig_size = (4, 4)

        # Visualization 1: Total Number of Cases per Year (2008-2020)
        with col1:
            yearly_cases = city_data.groupby('year')['case_total'].sum().reset_index()

            # Find the year with the maximum number of cases
            max_year = yearly_cases.loc[yearly_cases['case_total'].idxmax(), 'year']
            max_cases = yearly_cases['case_total'].max()

            fig, ax = plt.subplots(figsize=fig_size)

            # Color the bars based on whether they are the maximum year or not
            bar_colors = ['#19535b' if year == max_year else '#d9d9d9' for year in yearly_cases['year']]
    
            ax.bar(yearly_cases['year'], yearly_cases['case_total'], color=bar_colors)
            ax.set_xticks(range(2008, 2021))
            ax.set_xticklabels([str(year)[-2:] for year in range(2008, 2021)], fontsize=8)
            ax.set_title('Total Cases Per Year (2008-2020)', fontsize=14, color='gray')
            st.pyplot(fig)

        # Visualization 2: Average Monthly Cases
        with col2:
            # Grouping data by year and month, then calculating the monthly average
            monthly_data = city_data.groupby(['year', 'month'])['case_total'].sum().reset_index()
            monthly_avg = monthly_data.groupby('month')['case_total'].mean().reset_index()

            # Sorting to find the top 3 months with the highest average cases
            top_months_sorted = monthly_avg.sort_values(by='case_total', ascending=False).head(3)
    
            # Extracting the peak cases and formatting the top month names
            peak_cases = monthly_avg['case_total'].max()
            top_month_names = [
                ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month']) - 1]
                for _, row in top_months_sorted.iterrows()
            ]
            
            # Joining month names into a readable string
            top_months_str = ", ".join(top_month_names[:-1]) + ", and " + top_month_names[-1]
        
            # Plotting the data
            fig, ax = plt.subplots(figsize=fig_size)
            ax.plot(monthly_avg['month'], monthly_avg['case_total'], marker='o', color='#d9d9d9', markersize=6)
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=8)
            ax.set_title('Average Monthly Cases', fontsize=14, color='gray')
        
            # Highlighting the top 3 months
            for _, row in top_months_sorted.iterrows():
                ax.plot(row['month'], row['case_total'], marker='o', color='#19535b', markersize=6)
                month_abbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(row['month']) - 1]
                ax.text(row['month'] + 0.4, row['case_total'], month_abbr, color='#19535b', ha='left', fontsize=8)
        
            # Displaying the plot
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
            ax.set_title('No. of Weeks With/Without Cases', fontsize=14, color='gray')
            st.pyplot(fig)

        # Layout for 3 columns
        col1, col2, col3 = st.columns(3)

        # Set uniform figure size
        fig_size = (4, 4)
        with col1:
            st.markdown(f"The total number of cases peaked at **{max_cases}** in **{max_year}**")
        with col2:
            st.markdown(f"The average monthly cases peaked at **{int(peak_cases)}** and were highest in **{top_months_str}**.")
        with col3:
            st.markdown(f"From 2008-2020, there were {with_case_count} weeks **with cases** and {without_case_count} **weeks without cases**.")

        # Placeholder for Leptospirosis Cases Summary
        st.markdown("### Leptospirosis Risk Factors")
        # Layout for 2 columns in the second row
        col1, col2 = st.columns(2)
        
        # Dropdown for selecting the feature to overlay
        with col1:
            feature = st.selectbox(
                '',  # Empty label to remove the text above the dropdown
                options=['heat_index', 'rh', 'pr']
            )
        # Layout for 2 columns in the third row
        col1, col2 = st.columns(2)

        # Visualization 4: Overlay Selected Feature with Monthly Aggregation
        with col1:
            # Grouping data by year and month, then calculating the monthly average for case total and the selected feature
            monthly_data = city_data.groupby(['year', 'month']).agg({
                'case_total': 'sum',
                feature: 'mean'
            }).reset_index()
        
            # Averaging the same month throughout the years
            monthly_avg = monthly_data.groupby('month').agg({
                'case_total': 'mean',
                feature: 'mean'
            }).reset_index()
        
            # Scaling the features to overlay on the same scale
            scaler = MinMaxScaler()
            scaled_features = scaler.fit_transform(monthly_avg[[feature]])
            scaled_df = pd.DataFrame(scaled_features, columns=[feature])
            scaled_df['month'] = monthly_avg['month']
            scaled_df['case_total'] = scaler.fit_transform(monthly_avg[['case_total']])
        
            # Plotting the data with the scaled selected feature
            fig, ax = plt.subplots(figsize=fig_size)
            
            # Plotting case total and the selected feature
            ax.plot(scaled_df['month'], scaled_df['case_total'], marker='o', label='Case Total', color='#d9d9d9', markersize=6)
            ax.plot(scaled_df['month'], scaled_df[feature], marker='o', label=feature.replace('_', ' ').title(), color='#19535b', markersize=4)
            
            # Setting up x-axis labels and title
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=8)
            ax.set_title(f'Cases vs {feature.replace("_", " ").title()}', fontsize=10, color='gray')
            ax.legend(fontsize=8)
        
            # Displaying the plot
            st.pyplot(fig)

        
        # Placeholder for the second column
        with col2:
            # You can use st.empty() or a simple text placeholder
            st.empty()
    if __name__ == "__main__":
        main()
