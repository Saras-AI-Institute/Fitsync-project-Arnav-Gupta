import streamlit as st
import pandas as pd
import plotly.express as px
from modules.processor import process_data

# Title
st.title("Trends and Insights")

# Sidebar filter
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select time range",
    options=["last 7 days", "last 30 days", "all time"],
    index=2
)

# Load data
@st.cache_data
def load_data():
    return process_data()

df = load_data()

# Filtered data for the selected time range
if 'Date' in df.columns:
    if time_range == "last 7 days":
        filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
    elif time_range == "last 30 days":
        filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]
    else:
        filtered_df = df

# Summary Statistics
st.write("## Summary Statistics")
summary_stats = filtered_df[['Recovery_Score', 'Sleep_hours', 'Steps', 'Calories_Burned']].agg(['mean', 'min', 'max'])
st.dataframe(summary_stats)

# Average Recovery Score Month Wise
st.write("## Average Recovery Score Per Month")
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
# Fix JSON serialization issue by converting periods to string
filtered_df['Month'] = filtered_df['Month'].astype(str)
avg_recovery_per_month = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()
# Ensure the conversion of Month to string happens before plotting
avg_recovery_per_month['Month'] = avg_recovery_per_month['Month'].astype(str)
line_chart = px.line(avg_recovery_per_month, x='Month', y='Recovery_Score',
                     title="Average Recovery Score Per Month")
st.plotly_chart(line_chart)

# Histograms
st.write("## Distribution Histograms")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Steps Distribution")
    steps_hist = px.histogram(filtered_df, x='Steps', nbins=20, 
                              title="Steps Distribution")
    st.plotly_chart(steps_hist)

    st.subheader("Recovery Score Distribution")
    recovery_hist = px.histogram(filtered_df, x='Recovery_Score', nbins=20, 
                                 title="Recovery Score Distribution")
    st.plotly_chart(recovery_hist)

with col2:
    st.subheader("Calories Burned Distribution")
    calories_hist = px.histogram(filtered_df, x='Calories_Burned', nbins=20, 
                                 title="Calories Burned Distribution")
    st.plotly_chart(calories_hist)

    st.subheader("Sleep Hours Distribution")
    sleep_hist = px.histogram(filtered_df, x='Sleep_hours', nbins=20, 
                              title="Sleep Hours Distribution")
    st.plotly_chart(sleep_hist)
