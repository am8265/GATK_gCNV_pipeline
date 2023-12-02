# Overview

This documentation provides guidance on how to use the `getMatrices.py` script. The script generates deletion gene-by-sample matrix from  multi-sample annotSV file
 
```
 
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

```
## Usage example with **QUAL** filter

## Parameters and File Descriptions

- `--qual_threshold 20`: Sets the QUAL filter threshold. The script will consider only those entries from the GATK-gCNV vcf callset where QUAL is greater than 20.
- `samples.425.txt`: A text file containing a list of sample names. These samples are part of the multi-sample VCF/AnnotSV file.

### Output Files

- `rare_geneMatrix.le4of425.qual20.tsv`: This is the rare output file. It includes frequencies that are less than or equal to 4 out of 425 samples.
- `common_geneMatrix.gt4Of425.qual20.tsv`: The common output file. It contains frequencies greater than 4 out of 425 samples.
- `all_geneMatrix.qual20.tsv`: The superset output file. It combines data from `rare_geneMatrix.le4of425.qual20.tsv` and `common_geneMatrix.gt4Of425.qual20.tsv`.

### Input Data Files

- `AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg{1,3,4,5}.update.tsv`: These are the input data files. They consist of multi-sample AnnotSV files for different ACMG categories.


```
python getMatrices.py --qual_threshold 20 \
samples.425.txt \
rare_geneMatrix.le4of425.qual20.tsv common_geneMatrix.gt4Of425.qual20.tsv all_geneMatrix.qual20.tsv \
4 \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg1.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg3.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg4.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg5.update.tsv
```

## Usage example without **QUAL** filter

```
python getMatrices.py samples.425.txt \
rare_geneMatrix.le4of425.tsv common_geneMatrix.gt4Of425.tsv all_geneMatrix.tsv \
4 \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg1.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg3.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg4.update.tsv \
AnnotSV/Agilent325PlusIDTERPv2100Cohort.sv/Agilent325PlusIDTERPv2100Cohort.sv.acmg5.update.tsv
```


