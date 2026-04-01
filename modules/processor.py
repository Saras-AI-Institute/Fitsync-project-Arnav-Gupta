import pandas as pd
from pandas.api.types import is_numeric_dtype
from datetime import datetime


def load_data():
    """
    Load and clean the health data from a CSV file.
    The function fills missing values intelligently and converts date strings to datetime objects.
    Returns:
        pd.DataFrame: Cleaned DataFrame with processed health data.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv('data/health_data.csv')

    # Fill missing Steps with the median value of Steps
    if 'Steps' in df.columns and is_numeric_dtype(df['Steps']):
        df['Steps'].fillna(df['Steps'].median(), inplace=True)

    # Fill missing Sleep_Hours with a default of 7.0
    if 'Sleep_Hours' in df.columns:
        df['Sleep_Hours'].fillna(7.0, inplace=True)

    # Fill missing Heart_Rate_bpm with a default of 68
    if 'Heart_Rate_bpm' in df.columns:
        df['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Fill missing values in all other numeric columns with their median
    for column in df.columns:
        if column not in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Date'] and is_numeric_dtype(df[column]):
            df[column].fillna(df[column].median(), inplace=True)

    # Convert 'Date' column to datetime objects if present
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Return the cleaned DataFrame
    return df


def calculate_recovery_score(df):
    """
    Add a 'Recovery_Score' column to the DataFrame.
    This score represents how well the person's body has recovered on a scale of 0 to 100.
    """

    # Initialize the Recovery_Score column with a base score
    df['Recovery_Score'] = 50

    # Adjust score based on Sleep_Hours
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_Score'] += 20  # Good sleep
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_Score'] -= 20  # Poor sleep

    # Adjust score based on Heart_Rate_bpm
    # Higher score benefit for lower heart rate, inverse scale linearly
    df['Recovery_Score'] += (95 - df['Heart_Rate_bpm']) * 0.2

    # Adjust score based on Steps
    # Moderate activity is good; too high steps can reduce score slightly
    df['Recovery_Score'] -= (df['Steps'] - 10000).clip(lower=0) * 0.001

    # Ensure Recovery_Score stays within bounds of 0 and 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(lower=0, upper=100)

    # Return the DataFrame with the new column
    return df

