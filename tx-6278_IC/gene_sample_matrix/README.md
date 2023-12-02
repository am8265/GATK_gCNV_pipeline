# How to get deletion gene-by-sample matrix from  multi-sample annotSV file 


''' 
python getMatrices.py -h
usage: getMatrices.py [-h] [--qual_threshold QUAL_THRESHOLD]
                      [--cds_percent_range MIN MAX]
                      sample_names_file rare_output_file common_output_file
                      superset_output_file frequency_param data_files
                      [data_files ...]

Process annotSV data to create gene-sample matrices.

positional arguments:
  sample_names_file     File containing sample names.
  rare_output_file      Output TSV file for rare matrix.
  common_output_file    Output TSV file for common matrix.
  superset_output_file  Output TSV file for superset matrix.
  frequency_param       Frequency parameter for differentiating rare/common
                        genes.
  data_files            Path to one or more annotSV updated (1,3,4,5) files.

optional arguments:
  -h, --help            show this help message and exit
  --qual_threshold QUAL_THRESHOLD
                        QUAL value threshold for filtering.Default is 0.
  --cds_percent_range MIN MAX
                        Range of Overlapped_CDS_percent to consider. Default
                        is 100. e.g. you could use "--cds_percent_range 90
                        100" to imply Overlapped_CDS_percent to be within that
                        close interval range

'''

## Usage Examples

without **QUAL** filter

'''
python getMatrices.py samples.425.txt \
rare_geneMatrix.le4of425.tsv common_geneMatrix.gt4Of425.tsv all_geneMatrix.tsv \
4 \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg1.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg3.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg4.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg5.update.tsv
'''

with **QUAL** filter

--qual_threshold 20: QUAL (from GATK-gCNV vcf callset)> 20
samples.425.txt: .txt file containing list of sample names in the multi-sample VCF/AnnotSV file

rare_geneMatrix.le4of425.qual20.tsv: rare_output_file (freq <= 4/425 samples)
common_geneMatrix.gt4Of425.qual20.tsv: common_output_file ( freq > 4/425 samples)
all_geneMatrix.qual20.tsv: superset_output_file (rare_geneMatrix.le4of425.qual20.tsv + common_geneMatrix.gt4Of425.qual20.tsv)
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg{1,3,4,5}.update.tsv: input data_files (multi-sample annotSV files) 


'''
python getMatrices.py --qual_threshold 20 \
samples.425.txt \
rare_geneMatrix.le4of425.qual20.tsv common_geneMatrix.gt4Of425.qual20.tsv all_geneMatrix.qual20.tsv \
4 \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg1.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg3.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg4.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg5.update.tsv
'''

