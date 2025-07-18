import pandas as pd

# Read the CSV file
df = pd.read_csv('data/f1_final_dataset_with_driverform_top3.csv')

# Get unique values from a column named 'column_name'
unique_values = df['Circuit'].unique()

# Print the unique values
print(unique_values)
