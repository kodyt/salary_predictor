'''This script will take a csv file that contains either state or company with salary information. It will then average/median all of the salaries by state/company and output it to a new file'''
import pandas as pd
import time

# number of counts to output
count = 10
input = 'updated_file.csv'


def read_csv(filename):


    # Read the CSV file into a DataFrame
    data = pd.read_csv(filename)

    # Remove 
    # data['avg_salary'] = data['avg_salary'].str.replace(',', '').str.replace('$','')

    # Convert the 'Clean Salary' column to numeric values, handling non-conforming values
    data['avg_salary'] = pd.to_numeric(data['avg_salary'], errors='coerce')

    # Convert the 'Company' column to lowercase and remove leading/trailing spaces
    data['Company'] = data['Company'].str.strip().str.lower()

    data['Company'] = data['Company'].str.replace('..','').str.replace('salary','').str.strip()

    # Group the data by company and calculate the average salary and count
    grouped_data = data.groupby('Company')['avg_salary'].agg(['mean', 'median', 'count'])
    grouped_data = grouped_data.rename(columns={'mean': 'Average Salary', 'median': 'Median Salary', 'count': 'Count'})

    # Remove leading space in the 'Company' column
    grouped_data.index = grouped_data.index.str.strip()

    # Filter out values with less than 5 companies
    grouped_data = grouped_data[grouped_data['Count'] >= count]

    # Sort the data by descending average salary
    grouped_data = grouped_data.sort_values(by='Median Salary', ascending=False)

    # Save the grouped data to a new CSV file
    grouped_data.to_csv('comp_salary.csv', header=True)

    print(f"Grouped data with average salary, median salary, and count (with a minimum of {count} companies) saved to comp_salary.csv")
    return

if __name__ == "__main__":
    start = time.time()

    # Find/Replace function 
    read_csv(input)

    # Timing
    print(time.time() - start)
