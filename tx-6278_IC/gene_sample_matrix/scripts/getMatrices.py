import sys
import csv
import argparse
import re

#Testing braches
# Testing 2
def filter_by_exons(exon_count_cutoff, total_exon_count, location, location2):
    """
    Return True if the number of exons overlapped is >= exon_count_cutoff.
    
    Parameters:
    exon_count_cutoff (int): The minimum number of exons to be overlapped.
    total_exon_count (int): Total number of exons.
    location (str): The location string to be checked.
    location2 (str): Secondary location string for additional check.

    Returns:
    bool: True if conditions are met, False otherwise.
    """
    # Reject if location2 is in reject regions
    reject_regions = ['UTR', '5\'UTR', '3\'UTR']
    if location2 in reject_regions:
        return False

    if location == 'txStart-txEnd':
        return True

    # Pre-compile regular expressions
    patterns = {
        'exon_txEnd': re.compile(r'exon(\d+)-txEnd'),
        'txStart_exon': re.compile(r'txStart-exon(\d+)'),
        'intron_txEnd': re.compile(r'intron(\d+)-txEnd'),
        'txStart_intron': re.compile(r'txStart-intron(\d+)'),
        'exon_exon': re.compile(r'exon(\d+)-exon(\d+)'),
        'intron_intron': re.compile(r'intron(\d+)-intron(\d+)'),
        'exon_intron': re.compile(r'exon(\d+)-intron(\d+)'),
        'intron_exon': re.compile(r'intron(\d+)-exon(\d+)')
    }

    for pattern in patterns.values():
        match = pattern.search(location)
        if match:
            groups = [int(g) for g in match.groups() if g]
            exons_overlapped = 0

            if pattern == patterns['exon_txEnd']:
                exons_overlapped = (total_exon_count - groups[0]) + 1
            elif pattern == patterns['txStart_exon']:
                exons_overlapped = groups[0]
            elif pattern == patterns['intron_txEnd']:
                exons_overlapped = (total_exon_count - (groups[0] + 1)) + 1
            elif pattern == patterns['txStart_intron']:
                exons_overlapped = groups[0]
            elif pattern == patterns['exon_exon']:
                exons_overlapped = groups[1] - groups[0] + 1
            elif pattern == patterns['intron_intron']:
                exons_overlapped = groups[1] - (groups[0] + 1) + 1
            elif pattern == patterns['exon_intron']:
                exons_overlapped = groups[1] - groups[0] + 1
            elif pattern == patterns['intron_exon']:
                exons_overlapped = groups[1] - (groups[0] + 1) + 1

            if exons_overlapped >= exon_count_cutoff:
                return True
            break  # Exit loop if a match was found

    return False

def read_sample_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def parse_line(line, cols):
    """ Parses a single line from the file and returns a dictionary of values. """
    values = line.strip().split('\t')
    return {key: values[index] for key, index in cols.items()}

def process_samples(samples, sample_names, parsed_line, data):
    """ Process samples and add to data if conditions are met. """
    for sample in samples.split(';'):
        if sample in sample_names:
            row = {key: value for key, value in parsed_line.items() if key not in ['SV_type', 'Annotation_mode']}
            data.append(row)

def filter_data(parsed_line, qual_threshold, cds_percent_range, exon_count_cutoff, sample_names, data):
    """ Filters data based on various conditions and processes samples. """
    if parsed_line['SV_type'] != 'DEL' or parsed_line['Annotation_mode'] != 'split':
        return

    qual_value = float(parsed_line['QUAL'])

    if qual_value <= qual_threshold:
        return

    if exon_count_cutoff is not None:
        if filter_by_exons(exon_count_cutoff, int(parsed_line['Exon_count']), parsed_line['Location'], parsed_line['Location2']):
            process_samples(parsed_line['Samples_ID'], sample_names, parsed_line, data)
    else:
        cds_percent = float(parsed_line['Overlapped_CDS_percent'])
        if cds_percent_range[0] <= cds_percent <= cds_percent_range[1]:
            process_samples(parsed_line['Samples_ID'], sample_names, parsed_line, data)

def read_multiple_files(file_paths, sample_names, qual_threshold, cds_percent_range, exon_count_cutoff):
    """ Reads multiple files and processes them. """
    all_data = []
    cols_to_extract = ['AnnotSV_ID', 'SV_chrom', 'SV_start', 'SV_end', 'Samples_ID', 'QUAL', 'Gene_name', 
                       'Overlapped_CDS_percent', 'Exon_count', 'Location', 'Location2', 'SV_type', 'Annotation_mode']

    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                header = file.readline().strip().split('\t')
                cols = {col: header.index(col) for col in cols_to_extract}
                data = []
                
                for line in file:
                    parsed_line = parse_line(line, cols)
                    filter_data(parsed_line, qual_threshold, cds_percent_range, exon_count_cutoff, sample_names, data)
                
                all_data.extend(data)
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")

    return all_data


def create_rare_common_matrices(extracted_data, sample_names, rare_threshold, rare_output, common_output, superset_output):
    
    total_samples = len(sample_names)
    #rare_cutoff = rare_threshold / total_samples


    gene_names = set(row['Gene_name'] for row in extracted_data)

    # Initialize dictionaries for rare, common, and superset gene data
    rare_genes = {gene: {sample: 0 for sample in sample_names} for gene in gene_names}
    common_genes = {gene: {sample: 0 for sample in sample_names} for gene in gene_names}
    superset_genes = {gene: {sample: 0 for sample in sample_names} for gene in gene_names}

    # Count occurrences and classify as rare, common, or part of the superset
    for row in extracted_data:
        gene = row['Gene_name']
        #for sample in sample_names: # try to change for faster processing 
        for sample in row['Samples_ID'].split(';'):
            superset_genes[gene][sample] = 1

    # Filter out from superset_genes 
    # Filter out genes for rare matrix where all samples have '0'
    rare_genes = {gene: counts for gene, counts in superset_genes.items() if sum(counts.values()) <= rare_threshold and sum(counts.values()) > 0}
    
    # Remove genes from common matrix that fall below the threshold
    common_genes = {gene: counts for gene, counts in superset_genes.items() if sum(counts.values()) > rare_threshold}

    # Write matrices to TSV files
    for output_file, gene_data in zip([rare_output, common_output, superset_output], [rare_genes, common_genes, superset_genes]):
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(['Gene_name'] + sample_names)
            for gene, sample_values in gene_data.items():
                writer.writerow([gene] + [sample_values[sample] for sample in sample_names])

# Main section to parse command line arguments
def main():

    parser = argparse.ArgumentParser(description='Process annotSV data to create gene-sample matrices.')
    parser.add_argument('sample_names_file', type=str, help='File containing sample names.')
    parser.add_argument('rare_output_file', type=str, help='Output TSV file for rare matrix.')
    parser.add_argument('common_output_file', type=str, help='Output TSV file for common matrix.')
    parser.add_argument('superset_output_file', type=str, help='Output TSV file for superset matrix.')
    parser.add_argument('--qual_threshold', type=float, default=0, help='QUAL value threshold for filtering.Default is 0.')
    parser.add_argument('frequency_param', type=float,help='Frequency parameter for differentiating rare/common genes.')
    parser.add_argument('--cds_percent_range', nargs=2, type=float, default=[100, 100], 
                        metavar=('MIN', 'MAX'), help='Range of Overlapped_CDS_percent to consider. Default is 100. e.g. you could use "--cds_percent_range 90 100" to imply Overlapped_CDS_percent to be within that close interval range')
    parser.add_argument('--exon_count_cutoff', type=int, help='minimum no. of exons fully overlapped by the CNV, when this option is used cds_percent_rage is switched off')
    parser.add_argument('data_files', nargs='+', help='Path to one or more annotSV updated (1,3,4,5) files.')

    args = parser.parse_args()

    sample_names = read_sample_names(args.sample_names_file)

       
    extracted_data = read_multiple_files(args.data_files, sample_names, args.qual_threshold, args.cds_percent_range, args.exon_count_cutoff)
    create_rare_common_matrices(extracted_data, sample_names, args.frequency_param, args.rare_output_file, args.common_output_file, args.superset_output_file)

if __name__ == '__main__':
    main()
