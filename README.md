# Copy Number Variant Analysis using GATK-gCNV pipeline on 425 Interstitial Cystitis samples

## Overview
This repository contains scripts and resources for Copy Number Variant (CNV) analysis on and Interstitial Cystitis Cohort (n=425) using the Genome Analysis Toolkit's germline CNV (GATK-gCNV) pipeline.
The GATK-gCNV pipeline could be used for other datasets.

![GATK-gCNV pipeline overview-1](tx-6278_IC/Slide4.jpg)  
![GATK-gCNV pipeline overview-2](tx-6278_IC/Slide6.jpg)
![GATK-gCNV pipeline overview-3](tx-6278_IC/Slide5.jpg)

## Repository Structure
- `README.md`: This file, containing detailed information about the project.
- `scripts/`: Directory containing scripts used in the GATK-gCNV pipeline.
- `tx-6278_IC/`: Directory containing specific resources and datasets and analysis(could be partial for lack of space on github) related to the Interstitial Cohort Project

## How the Pipeline was run
This section will provide step-by-step instructions on how to run the GATK-gCNV pipeline for CNV analysis. Some examples maybe given only one of
the kits used, it should be simple to extend the logic to other kits.

### 1. Run PreprocessIntervals to convert exomeKit bed file to interval_list file (with 250bp padding)
bash scripts/PreprocessIntervals.sh tx-6278_IC/data/IDT_xGen_Exome_Research_Panel_v1_all.bed

bash scripts/PreprocessIntervals.1.sh tx-6278_IC/data/Agilent_SureSelect_v6_all.bed

e.g. Agilent_SureSelect_v6_all.bed.targets.preprocessed.interval_list will be the output

### 2. CollectReadCounts and store read counts in hdf5 format

`SGE cluster run.`
`tx-6278_IC/IC_proband_and_affected.ATAV_CRAMS.symLinks.txt is a file containing paths to cram/bam`

qsub -S /bin/bash -cwd -V -N collectCountsExome -m bea -tc 240 -o . -e . -pe threaded 8 -t 1-1 scripts/CollectReadCounts.2.sh tx-6278_IC/IC_proband_and_affected.ATAV_CRAMS.symLinks.txt data/Agilent_SureSelect_v6_all.bed.targets.preprocessed.interval_list




### 3. Determine GermlineContigPloidy based on contig ploidy priors.

tx-6278_IC/PathToCounts.IDTERPv2.IC_proband_and_affected.txt contains path to hdf5CountsFile/sample generated in step2.

`bash scripts/DetermineGermlineContigPloidy.4.sh tx-6278_IC/PathToCounts.IDTERPv2.IC_proband_and_affected.txt data/IDTERPv2_all.bed.targets.preprocessed.interval_list`

HPC cluster sge mode run

`qsub -S /bin/bash -cwd -V -N DetermineGermlineContigPloidy -m bea -o . -e . -pe threaded 24 scripts/DetermineGermlineContigPloidy.4.sh tx-6278_IC/PathToCounts.agilentV6.IC_proband_and_affected.txt data/Agilent_SureSelect_v6_all.bed.targets.preprocessed.interval_list`

### 4. Scatter Files creation

### 5. GermlineCNVCallerCohort Mode




`qsub -S /bin/bash -cwd -V -N GermlineCNVCallerCohort -m bea -tc 240 -o . -e . -pe threaded 24 -t 1-24 scripts/GermlineCNVCaller.5.sh tx-6278_IC/PathToCounts.agilentV6.IC_proband_and_affected.txt tx-6278_IC/Agilent325/scatter_file_list.Agilent325.txt ploidy-calls Agilent325Cohort`







## Requirements
- [List of software and tools required]
- [Version details]
- [Any other dependencies]

*Fill in the details of the software, tools, and any other requirements needed to run your pipeline.*

## Usage
```bash
# Example command to run the pipeline
# Replace with actual commands and provide necessary explanations