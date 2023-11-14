#!/usr/bin/env bash
#SGE_TASK_ID="12"
JAVA_HOME="/home/am5153/miniconda3/envs/java17"
export JAR_PATH="/nfs/informatics/data/am5153/bin/gatk-4.4.0.0/gatk-package-4.4.0.0-local.jar"
hdf5_or_tsv_coverageFile_list="$1"
hdf5_or_tsv="$(cat ${hdf5_or_tsv_coverageFile_list} | sed 's/^/-I /g' | tr '\n' ' ')"
# should be the output of PreprocessIntervals.1.sh -- padded exomeKit.bed file
scatter_file_list="$2"
interval_list=$(sed -n -e "$SGE_TASK_ID p" ${scatter_file_list}) # could be a filtered interval list, or a shard interval_list
contig_ploidy_calls_dir="$3"
out_dir="$(pwd)/00$SGE_TASK_ID"
out_prefix="$4"
# Select cram or bam
source ~/miniconda3/etc/profile.d/conda.sh
conda activate gatk_new
alias python=/home/am5153/miniconda3/envs/gatk_new/bin/python
# Running in Cohort Mode
echo ${JAVA_HOME}/bin/java -jar $JAR_PATH GermlineCNVCaller \
  --run-mode COHORT \
  -L ${interval_list} \
  --interval-merging-rule OVERLAPPING_ONLY \
  ${hdf5_or_tsv} \
  --contig-ploidy-calls ${contig_ploidy_calls_dir} \
  --output ${out_dir} \
  --output-prefix ${out_prefix} \
  --verbosity DEBUG > run_GermlineCNVCaller.5.${SGE_TASK_ID}.sh
bash run_GermlineCNVCaller.5.${SGE_TASK_ID}.sh
