import pandas as pd
import glob
import os
from io import StringIO

# Specify the directory containing the JSON datasets
directory = 'C:/Users/User/Downloads/Compressed/archive'

# Get a list of all JSON files in the directory
all_files = glob.glob(os.path.join(directory, "*.json"))

# Initialize a dictionary to hold the dataframes, using filenames as keys
dfs = {}

# Function to clean the data
def clean_data(df):
    # Inspect the dataset
    print("Initial Inspection:")
    print(df.info())  # Check for null values and data types
    print(df.describe(include='all'))  # Summary of all columns
    print(df.head())  # Display the first few rows
    
    # Remove duplicates
    df = df.drop_duplicates()
    print("After removing duplicates:")
    print(df.info())
    
    # Handle irrelevant data (customize this step as per your criteria)
    # Example: Remove rows where a specific column has irrelevant values
    if 'irrelevant_column' in df.columns:
        df = df[df['irrelevant_column'] != 'irrelevant_value']
    
    # Handle corrupted data (customize this step as per your criteria)
    # Example: Remove rows with missing values in crucial columns
    crucial_columns = ['important_column1', 'important_column2']  # Update with your column names
    df = df.dropna(subset=crucial_columns)
    print("After handling corrupted data:")
    print(df.info())
    
    return df

# Function to provide a summary of the dataset
def summarize_dataset(df):
    summary = {}
    summary['column_names'] = df.columns.tolist()
    summary['num_rows'] = len(df)
    summary['num_columns'] = len(df.columns)
    summary['sample_data'] = df.head().to_dict(orient='records')
    return summary

# Iterate over the list of files and read each one into a dataframe
for file in all_files:
    # Extract the filename without the directory and extension
    file_name = os.path.basename(file).split('.')[0]
    
    # Read the JSON file line by line if it contains multiple JSON objects
    with open(file, 'r', encoding='utf-8') as f:
        json_lines = f.readlines()
    
    # Convert each JSON object into a DataFrame and concatenate
    df = pd.concat([pd.read_json(StringIO(line), lines=True) for line in json_lines], ignore_index=True)
    
    # Clean the dataframe
    df_cleaned = clean_data(df)
    # Store the cleaned dataframe
    dfs[file_name] = df_cleaned

# Now you can access each cleaned dataframe using the filename as the key
# Let's provide a summary for each dataset
for name, df in dfs.items():
    print(f"Summary for {name}:")
    dataset_summary = summarize_dataset(df)
    print(f"Column names: {dataset_summary['column_names']}")
    print(f"Number of rows: {dataset_summary['num_rows']}")
    print(f"Number of columns: {dataset_summary['num_columns']}")
    print(f"Sample data: {dataset_summary['sample_data'][:3]}")  # Display the first 3 rows as sample
    print("\n\n")
