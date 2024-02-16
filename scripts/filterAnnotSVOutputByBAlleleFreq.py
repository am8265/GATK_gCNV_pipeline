#!/usr/bin/env python
import csv
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description='Process a TSV file based on htz_hom_ratio.')

# Adding arguments
parser.add_argument('input_tsv_path', type=str, help='Path to the input TSV file')
parser.add_argument('output_tsv_path', type=str, help='Path to the output TSV file')

# Parsing arguments
args = parser.parse_args()

# User-specified filtering criteria for htz_hom_ratio
# Default is to check for 'NA' or 0. This can be adjusted as per user input
def htz_hom_ratio_filter(value):
    return value == 'NA' or float(value) == 0

# Function to process the TSV file
def process_tsv(input_path, output_path, htz_hom_ratio_filter):
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        
        for row in reader:
            samples = row['Samples_ID'].split(';')
            updated_samples = []
            
            for sample in samples:
                try:
                    # Fetch the Count_htz/allHom value for the current sample
                    count_htz_allHom_value = row[f'Count_htz/allHom({sample})']
                    # Apply the filtering criteria
                    if htz_hom_ratio_filter(count_htz_allHom_value):
                        updated_samples.append(sample)
                except KeyError:
                    # Handle case where specific Count_htz/allHom field does not exist for a sample
                    print(f"Warning: Count_htz/allHom field for {sample} not found in row.")
            
            # Update the Samples_ID field based on filtering outcome
            row['Samples_ID'] = ';'.join(updated_samples)
            writer.writerow(row)

# Execute the function with the command-line arguments
process_tsv(args.input_tsv_path, args.output_tsv_path, htz_hom_ratio_filter)



