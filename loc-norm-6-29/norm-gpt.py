# want to separate the job title from the location and then normalize the location\
import csv 
import re
import time

input_file = "./join-data-sal/gpt_location.csv"
output_file = "./loc-norm-6-29/output_norm_gpt.csv"

state_mapping_file = './loc-norm-6-29/loc_lib.csv'
city_state_mapping_file = './loc-norm-6-29/top-500-cities.csv'
title_file = "./loc-norm-6-29/title_names_lib.csv"
column_name = 'job'

def read_titles():
    # Create an empty set to store the rows
    rows_set = []

    # Open the CSV file
    with open(title_file, 'r') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Assuming the 'Title' column is in the first column (index 0)
            title = row[0]
            
            # Add the title to the set
            rows_set.append(title)
    return rows_set


def normalize_location(location, state_abbreviations_mapping, city_state_mapping):
    location = location.replace('"', '')  # Remove quotation marks
    location = location.strip()  # Remove leading and trailing spaces
    # Check if location contains a state abbreviation
    for abbrev, full_name in state_abbreviations_mapping.items():
        if abbrev in location:
            location = re.sub(r'\b{}\b'.format(abbrev), full_name, location, flags=re.IGNORECASE)
            return location.lower().replace(',', '')  # Remove commas
    
    # If state abbreviation not found, check city-state mapping
    city = location.lower()
    if city == 'washington d.c.':
        return 'washington district of columbia'
    elif city == 'st louis missouri' or city == 'saint louis missouri' or city == 'st louis':
        return 'st. louis missouri'
    
    if city in city_state_mapping:
        state = city_state_mapping[city]
        location = f"{city} {state}"
    return location.lower()



def main(job_titles_set):

    # Read state mapping from a CSV file
    state_mapping = {}
    with open(state_mapping_file, 'r') as state_file:
        csv_reader = csv.reader(state_file)
        for row in csv_reader:
            state_mapping[row[0]] = row[1]
    

    # Read city-state mapping from a CSV file
    city_state_mapping = {}
    with open(city_state_mapping_file, 'r') as city_state_file:
        csv_reader = csv.reader(city_state_file)
        for row in csv_reader:
            city_state_mapping[row[0].lower()] = row[1]
    

    # Open the input CSV file as a dictionary reader
    with open(input_file, 'r') as file:
        # Create a CSV reader
        csv_reader = csv.DictReader(file)
        
        # Get the fieldnames from the reader
        fieldnames = csv_reader.fieldnames
        
        # Append 'location' to the fieldnames
        fieldnames.append('location')

        updated_rows = []
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Get the job_location value
            job_location = row[column_name]

            # Find the longest matching job title from the set
            matched_title = ''
            for title in job_titles_set:
                if title.lower() in job_location.lower() and len(title) > len(matched_title):
                    matched_title = title.lower()
            # print(matched_title)

            # Extract the location by removing the matched title from the string
            location = job_location.lower().replace(matched_title, '').strip()
            # print(location)

            # Update the 'job' value in the row with the new job title
            row[column_name] = matched_title
            
            row['location'] = normalize_location(location, state_mapping, city_state_mapping).replace(',', '').replace('"','')
            
            # Append the updated row to the list
            updated_rows.append(row)
            
    
    # Write the updated data to the output CSV file
    with open(output_file, 'w', newline='') as file:
        # Create a CSV writer
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header
        csv_writer.writeheader()
        
        # Write the updated rows
        csv_writer.writerows(updated_rows)

    return


if __name__ == '__main__':
    start = time.time()

    titles = read_titles()

    main(titles)

    print(f"Output printed to {output_file}")
    # Timing
    print(f"Time taken: {time.time() - start}")
    
