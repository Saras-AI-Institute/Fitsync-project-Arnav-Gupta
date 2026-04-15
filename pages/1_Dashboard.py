import streamlit as st
import pandas as pd
import plotly.express as px
from modules.processor import process_data

# Title
st.title("FitSync - Personal Health Analytics")

# Sidebar filter
st.sidebar.header("Filters")

time_range = st.sidebar.selectbox(
    "Select time range",
    options=["last 7 days", "last 30 days", "all time"],
    index=2
)

# Load data
df = process_data()

# Filtered data for the selected time range
if 'Date' in df.columns:
    if time_range == "last 7 days":
        filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
    elif time_range == "last 30 days":
        filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]
    else:
        filtered_df = df

# Metrics using filtered data
average_steps = filtered_df['Steps'].mean()
average_sleep_hours = filtered_df['Sleep_hours'].mean()
average_recovery_score = filtered_df['Recovery_Score'].mean()

# Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Steps", f"{average_steps:.0f}")

with col2:
    st.metric("Average Sleep Hours", f"{average_sleep_hours:.1f}")

with col3:
    st.metric("Average Recovery Score", f"{average_recovery_score:.1f}")

# Charts
left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Recovery Score & Sleep Trend")
    # Dual Line Chart for Recovery Score and Sleep Hours
    line_chart = px.line(filtered_df, x='Date', y=['Recovery_Score', 'Sleep_hours'],
                         labels={'value': 'Scores', 'variable': 'Type'},
                         title="Recovery Score & Sleep Trend")
    st.plotly_chart(line_chart)

with right_col:
    st.subheader("Recovery Score vs Daily Steps")
    # Scatter Plot for Recovery Score vs Steps colored by Sleep Hours
    scatter_plot = px.scatter(filtered_df, x='Steps', y='Recovery_Score', color='Sleep_hours',
                              labels={'Sleep_hours': 'Sleep Hours'},
                              title="Recovery Score vs Daily Steps")
    st.plotly_chart(scatter_plot)

# Below the charts
bottom_left_col, bottom_right_col = st.columns(2)
with bottom_left_col:
    st.subheader("Recovery Score vs Resting Heart Rate")
    # Scatter Plot: Recovery Score vs Heart Rate
    heart_rate_scatter = px.scatter(filtered_df, x='Heart_Rate_bpm', y='Recovery_Score',
                                    title="Recovery Score vs Resting Heart Rate")
    st.plotly_chart(heart_rate_scatter)

with bottom_right_col:
    st.subheader("Daily Calories Burned Trend")
    # Line Chart for Calories Burned over time
    calories_line_chart = px.line(filtered_df, x='Date', y='Calories_Burned',
                                  title="Daily Calories Burned Trend")
    st.plotly_chart(calories_line_chart)

# Ensure DataFrame is shown
st.write("## Processed Health Data")
st.dataframe(filtered_df)
