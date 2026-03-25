import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

# Define the date range for one year starting from 2025-01-01
date_range = pd.date_range(start='2025-01-01', periods=365, freq='D')

# Generate realistic data using normal and uniform distributions
steps = np.random.normal(loc=8500, scale=3000, size=365).clip(3000, 18000).astype(int)
sleep_hours = np.random.normal(loc=7.2, scale=1, size=365).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=365).clip(48, 110).astype(int)
calories_burned = np.random.randint(1800, 4200, size=365)
active_minutes = np.random.randint(20, 180, size=365)

# Create a DataFrame
fitness_data = pd.DataFrame({
    'date': date_range,
    'steps': steps,
    'sleep_hours': sleep_hours,
    'heart_rate_bpm': heart_rate_bpm,
    'calories_burned': calories_burned,
    'active_minutes': active_minutes
})

# Introduce 5% NaN values randomly in each column
for column in fitness_data.columns[1:]:  # Exclude 'date' column
    fitness_data.loc[fitness_data.sample(frac=0.05).index, column] = np.nan

# Save the data to a CSV file
fitness_data.to_csv('data/health_data.csv', index=False)

print("Generated fitness data for 365 days and saved to 'data/health_data.csv'.")