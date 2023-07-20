"""Location Normalization"""

import csv
import re
import time


# Paths to files
input_file = 'JT-norm.csv'
output_file = './loc-norm-6-29/output_norm_gd_ind.csv'

state_mapping_file = './loc-norm-6-29/loc_lib.csv'
city_state_mapping_file = './loc-norm-6-29/top-500-cities.csv'

col_name = "location"

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
    elif city == 'st louis' or city == 'st louis missouri' or city == 'saint louis' or city == 'saint louis missouri':
        return 'st. louis missouri'


    if city in city_state_mapping:
        state = city_state_mapping[city]
        location = f"{location} {state}".replace('.','')
    return location.lower()


def main():
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

    # Open the input CSV file
    with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
        csv_reader = csv.DictReader(in_file)
        fieldnames = csv_reader.fieldnames

        # Create a list to hold the updated rows
        updated_rows = []

        # Iterate over each row in the input CSV
        for row in csv_reader:
            location = row[col_name]
            normalized_location = normalize_location(location, state_mapping, city_state_mapping).replace('united states','')
            row[col_name] = normalized_location.replace(',', '').replace('"','').strip()

            updated_rows.append(row)

        # Write the updated data back to the CSV file
        out_file = csv.DictWriter(out_file, fieldnames=fieldnames)
        out_file.writeheader()
        out_file.writerows(updated_rows)
    return

if __name__ == '__main__':
    start = time.time()

    main()

    print(f"Output printed to {output_file}")
    # Timing
    print(f"Time taken: {time.time() - start}")
    


