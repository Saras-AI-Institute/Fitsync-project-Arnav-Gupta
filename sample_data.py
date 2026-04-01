import pandas as pd

def load_and_describe_csv(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Print the first 5 rows
    print('First 5 rows of the dataset:')
    print(df.head())

    # Calculate and print the number of missing values in each column
    missing_values = df.isnull().sum()
    print('\nNumber of missing values in each column:')
    print(missing_values)

if __name__ == '__main__':
    # Path to the health_data.csv file
    csv_file_path = 'data/health_data.csv'
    
    # Load and describe the CSV file
    load_and_describe_csv(csv_file_path)
