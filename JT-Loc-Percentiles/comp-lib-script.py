import pandas as pd

def get_zone(salary, q1, q2, q3, q4):
    if salary <= q1:
        return 1
    elif salary <= q2:
        return 2
    elif salary <= q3:
        return 3
    elif salary <= q4:
        return 4
    else:
        return 5

def main():
    # Replace 'input.csv' with your CSV file's name and path
    input_file = 'comp_salary.csv'
    # Replace 'output.csv' with the desired output file's name and path
    output_file = 'company_lib_out.csv'

    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Calculate quintiles (20th, 40th, 60th, and 80th percentiles)
    q1 = df["Average Salary"].quantile(0.20)
    q2 = df["Average Salary"].quantile(0.40)
    q3 = df["Average Salary"].quantile(0.60)
    q4 = df["Average Salary"].quantile(0.80)

    # Create a new DataFrame to store the results
    result_df = pd.DataFrame(columns=["Company", "Zone"])

    # Iterate through the rows, determine the zone, and add to the result DataFrame
    for _, row in df.iterrows():
        company = row["Company"]
        salary = row["Average Salary"]
        zone = get_zone(salary, q1, q2, q3, q4)
        result_df = pd.concat([result_df, pd.DataFrame({"Company": [company], "Zone": [zone]})], ignore_index=True)

    # Save the resulting DataFrame to a new CSV file
    result_df.to_csv(output_file, index=False)

    main()
