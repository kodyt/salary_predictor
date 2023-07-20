import pandas as pd

# Read the CSV file into a pandas DataFrame
input_file = 'comp_salary.csv'
output_file = 'comp_salary_with_value.csv'
df = pd.read_csv(input_file)

# Sort the DataFrame by salary in descending order
df = df.sort_values(by='Average Salary', ascending=False)

# Calculate the number of rows in the DataFrame
total_rows = len(df)

# Determine the number of rows for each group (20% each)
group_size = int(total_rows * 0.2)

# Assign the value based on the group they belong to
df['Value'] = 0
for i in range(1, 6):
    start_idx = (i - 1) * group_size
    end_idx = i * group_size
    df.loc[start_idx:end_idx, 'Value'] = 6- i

# Sort the DataFrame back to its original order
df = df.sort_index()

# Select the 'Company' and 'Value' columns and create a new DataFrame
result_df = df[['Company', 'Value']]

# Save the result DataFrame to a new CSV file
result_df.to_csv(output_file, index=False)

print("Output file created successfully!")
