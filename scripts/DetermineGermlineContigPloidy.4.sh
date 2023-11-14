#!/usr/bin/env bash
export JAVA_HOME="/home/am5153/miniconda3/envs/java17/bin"
export JAR_PATH="/nfs/informatics/data/am5153/bin/gatk-4.4.0.0/gatk-package-4.4.0.0-local.jar"
contig_ploidy_priors_file_hg19="/nfs/tx/in/CNV_WGS/data/hg19.contig_ploidy_priors_homo_sapiens.tsv"
hdf5_or_tsv_coverageFile_list="$1"
hdf5_or_tsv="$(cat ${hdf5_or_tsv_coverageFile_list} | sed 's/^/-I /g' | tr '\n' ' ')"
# should be the output of PreprocessIntervals.1.sh -- padded exomeKit.bed file
interval_list="$2" # could be a filtered interval list
contig_ploidy_priors_file="${3:-$contig_ploidy_priors_file_hg19}"
out_dir="${4:-$(pwd)}"
# Select cram or bam
source ~/miniconda3/etc/profile.d/conda.sh
conda activate gatk_new
alias python=/home/am5153/miniconda3/envs/gatk_new/bin/python
$JAVA_HOME/java -jar $JAR_PATH DetermineGermlineContigPloidy \
  -L ${interval_list} \
  --interval-merging-rule OVERLAPPING_ONLY \
  ${hdf5_or_tsv} \
  --contig-ploidy-priors ${contig_ploidy_priors_file} \
  --output $out_dir \
  --output-prefix ploidy \
  --verbosity DEBUG
