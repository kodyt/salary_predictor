'''This file creates the multiplier/buckets for job titles based on a larger file of job titles'''
import pandas as pd
import numpy as np

# Read the data from the CSV file
input_file = "updated_file.csv"
df = pd.read_csv(input_file)

# Group the data by the "job" column
grouped_data = df.groupby("job")["avg_salary"]

# Calculate the median value
median_value = grouped_data.median()

# Calculate the percentiles
percentiles = grouped_data.agg([lambda x: np.percentile(x, 6.25),
                                lambda x: np.percentile(x, 18.75),
                                lambda x: np.percentile(x, 31.25),
                                lambda x: np.percentile(x, 43.75),
                                lambda x: np.percentile(x, 50),
                                lambda x: np.percentile(x, 56.25),
                                lambda x: np.percentile(x, 68.75),
                                lambda x: np.percentile(x, 81.25),
                                lambda x: np.percentile(x, 93.75)])

# Divide the percentiles by the median value
percentiles = percentiles.div(median_value, axis=0)

# Add a new column for the median value
percentiles["median"] = median_value.values

# Rename the columns for better identification
percentiles.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", 'median']

# Reset the index to make "job" a regular column
percentiles.reset_index(inplace=True)

# Count the number of values in each group and add a "count" column
group_counts = df.groupby("job")["avg_salary"].count().reset_index()
percentiles = pd.merge(percentiles, group_counts, on="job", how="inner")
percentiles.rename(columns={"avg_salary": "count"}, inplace=True)

replacement_values = [0.7, 0.775, 0.85, 0.925, 1, 1.075, 1.15, 1.225, 1.3]

# Modify the DataFrame where the '1' column contains the value '1.0'
percentiles.loc[percentiles['1'] == 1.0, ['1','2','3','4','5','6','7','8','9']] = replacement_values

# Write the result to a new CSV file
output_file = "output.csv"
percentiles.to_csv(output_file, index=False)

print("Data processing is complete. Results are saved in 'output.csv'.")
