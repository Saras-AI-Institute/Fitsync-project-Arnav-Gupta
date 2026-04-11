import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Set parameters
num_days = 365
start_date = datetime(2025, 1, 1)

# Generate date range
dates = [start_date + timedelta(days=i) for i in range(num_days)]

# Generate realistic fitness data
steps = np.random.normal(loc=8500, scale=1500, size=num_days).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1.0, size=num_days).clip(4.5, 9.5)
heart_rate = np.random.normal(loc=68, scale=10, size=num_days).clip(48, 110)
calories_burned = np.random.normal(loc=3000, scale=600, size=num_days).clip(1800, 4200)
active_minutes = np.random.normal(loc=90, scale=40, size=num_days).clip(20, 180)

# Create DataFrame
data = pd.DataFrame({
    'Date': dates,
    'Steps': steps.astype(int),
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate.astype(int),
    'Calories_Burned': calories_burned.astype(int),
    'Active_Minutes': active_minutes.astype(int)
})

# Introduce 5% missing values (NaN) randomly in each column
for column in data.columns[1:]:  # Exclude 'Date' column
    data.loc[data.sample(frac=0.05).index, column] = np.nan

# Save to CSV
data.to_csv('data/health_data.csv', index=False)
