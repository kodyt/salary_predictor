import pandas as pd
import numpy as np

# Read the data from the CSV file
input_file = "last_combine.csv"
df = pd.read_csv(input_file)

# Group the data by the "job" and "location" columns
grouped_data = df.groupby(["job", "state"])["avg_salary"]

# Group the data by the "job" column
# grouped_data = df.groupby("job")["avg_salary"]

# Calculate the percentiles
percentiles = grouped_data.agg([lambda x: np.percentile(x, 12.5),
                                lambda x: np.percentile(x, 37.5),
                                lambda x: np.percentile(x, 50),
                                lambda x: np.percentile(x, 62.5),
                                lambda x: np.percentile(x, 87.5)])

# Rename the columns for better identification
percentiles.columns = ["0th", "25th", "50th", "75th", "100th"]

# Reset the index to make "job" a regular column
percentiles.reset_index(inplace=True)

# Count the number of values in each group and add a "count" column
group_counts = df.groupby(["job", "state"])["avg_salary"].count().reset_index()
percentiles = pd.merge(percentiles, group_counts, on=["job", "state"], how="inner")
percentiles.rename(columns={"avg_salary": "count"}, inplace=True)

# Write the result to a new CSV file
output_file = "output.csv"
percentiles.to_csv(output_file, index=False)

print("Data processing is complete. Results are saved in 'output.csv'.")