import csv
import re
import time
from fuzzywuzzy import fuzz
import pandas as pd 

#############CHANGE INFORMATION BELOW THIS LINE#################

# File name of the job titles to be normalized
file_name = 'dice_job.csv'

# Library files
find_library_name = 'find_lib.csv'
title_lib = 'title_lib.csv'

output_file = 'JT-norm.csv'

# Column name that you want normalized
column_name = 'job'

##########################ABOVE HERE############################

# Linkedin  normalization stop words
stopwords = ["staff",]

# Find/replace changes library
changes = {
    "seniority": "senior",
    "soft": "software",
    "eng": "engineer",
    "enig": "engineering",
    "deev": "development",
    "dev": "developer",
    "testing": "test",
    "cloudcloud": "cloud"
}

## Fuzzy Matching helper Functions
def remove_changes(title):
    for key, value in changes.items():
        if key in title:
            title = title.replace(key, value)

    # Dev ops title fix
    return title.replace("developerelopment", "development")


important = ["seniority", "junior", "principal"]
def important_titles(before, after):
    print
    if 'data' in after and 'data' not in before: # and 'with' in before
        return before
    if 'seniority eng' == before:
        return before
    if 'eng manager' == after and 'eng' not in before:
        return before
    if 'project manager' == after and 'project' not in before:
        return before
    for imp in important:
        if imp in before and imp not in after:
            after = imp + " " + after
    return after



## Fuzzy matching
def compare_titles_and_save():

    # FIND AND REPLACE
    df = pd.read_csv(file_name)
    lib = pd.read_csv(find_library_name)

    new_title = 'new_title'
    
    # Create a new column 'new_title' in the DataFrame to store the changed titles
    df[new_title] = df[column_name]

    for row in lib['Words']:
        row = row.lower()
        find = row.split('|')[0]
        find = find.strip()

        replace = row.split('|')[1]
        replace = replace.strip()

        df[new_title] = df[new_title].str.lower().replace(find, replace, regex=True)
    # removes the stop words
    df[new_title] = df[new_title].astype(str) .apply(lambda x: ' '.join(word for word in x.split() if word not in stopwords))
    # removes company names
    df[new_title] = df[new_title].apply(lambda x: re.sub(r'\bat.+', '', x))

    # END FIND AND REPLACE


    # Read the title_lib
    # Initialize an empty list to store the titles
    titles_list = []

    # Open the CSV title list file
    with open(title_lib, 'r') as file:
        reader = csv.reader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Assuming the title is in the first column (index 0)
            title = row[0]
            
            # Append the title to the list
            titles_list.append(title)

    # Create a new column 'new_title' in the DataFrame to store the changed titles
    # df['new_title'] = df[column_name]

    number = 0
    same = 0

    for i, title in enumerate(df[new_title]):
        if title in titles_list:
            same = same + 1
            df.at[i, new_title] = remove_changes(title)
        else:
            if "intern" in title:
                same = same + 1
                df.at[i, new_title] = remove_changes(title)
                continue

            match = max(titles_list, key=lambda x: fuzz.token_set_ratio(title, x))
            similarity_score = fuzz.partial_token_set_ratio(title, match)
            if similarity_score >= 80:
                number = number + 1
                match = important_titles(title, match)
                df.at[i, new_title] = remove_changes(match)
            else:
                df.at[i, new_title] = remove_changes(title)

    df.to_csv(output_file, index=False)

    print(f"Percentage of titles changed: {float(number) / len(df[new_title])} ")
    print(f"Percentage of titles already normalized: {float(same) / len(df[new_title])}")
    print(f"Percentage of titles not changed: { 1 - float(number) / len(df[new_title]) - float(same) / len(df[new_title])}")

if __name__ == "__main__":
    start = time.time()

    # Fuzzy Matching
    compare_titles_and_save()

    # Timing
    print(time.time() - start)