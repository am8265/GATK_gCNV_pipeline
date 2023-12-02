import sys
import csv
import argparse

def read_sample_names(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_multiple_files(file_paths, sample_names, qual_threshold, cds_percent_range):
    """ read the input annotv files """
    def process_file(file_path):
        with open(file_path, 'r') as file:
            header = file.readline().strip().split('\t')
            cols = {col: header.index(col) for col in ['AnnotSV_ID', 'SV_chrom', 'SV_start', 'SV_end', 'Samples_ID', 
                                                       'QUAL', 'Gene_name', 'Overlapped_CDS_percent', 'SV_type', 
                                                       'Annotation_mode']}
            data = []
            for line in file:
                values = line.strip().split('\t')
                
                if (values[cols['SV_type']] == 'DEL' and values[cols['Annotation_mode']] == 'split'):
                    qual_value = float(values[cols['QUAL']])
                    cds_percent = float(values[cols['Overlapped_CDS_percent']])
                    if (qual_value > qual_threshold and (cds_percent_range[0] <= cds_percent <= cds_percent_range[1])):
                      samples = values[cols['Samples_ID']].split(';')
                      for sample in samples:
                        if sample in sample_names:
                            row = {key: values[index] for key, index in cols.items() if key not in ['SV_type', 'Annotation_mode']}
                            data.append(row)
            return data

    all_data = []
    for file_path in file_paths:
        all_data.extend(process_file(file_path))

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
    parser.add_argument('data_files', nargs='+', help='Path to one or more annotSV updated (1,3,4,5) files.')

    args = parser.parse_args()

    sample_names = read_sample_names(args.sample_names_file)
    extracted_data = read_multiple_files(args.data_files, sample_names, args.qual_threshold, args.cds_percent_range)
    create_rare_common_matrices(extracted_data, sample_names, args.frequency_param, args.rare_output_file, args.common_output_file, args.superset_output_file)

if __name__ == '__main__':
    main()
