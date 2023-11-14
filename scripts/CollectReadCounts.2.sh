#!/usr/bin/env bash
export JAVA_HOME="/home/am5153/miniconda3/envs/java17/bin"
export JAR_PATH="/nfs/informatics/data/am5153/bin/gatk-4.4.0.0/gatk-package-4.4.0.0-local.jar"
bam_or_cram_list="$1"
bam_or_cram="$(sed -n -e "$SGE_TASK_ID p" ${bam_or_cram_list})"
# should be the output of PreprocessIntervals.1.sh -- padded exomeKit.bed file
interval_list="$2"
out_dir="${3:-$(pwd)}"
# Select cram or bam
if [[ ${bam_or_cram} == *.bam ]]; then
  sample=$(basename ${bam_or_cram} '.bam')

elif [[ ${bam_or_cram} == *.cram ]]; then
  sample=$(basename ${bam_or_cram} '.cram')
fi

$JAVA_HOME/java -jar $JAR_PATH CollectReadCounts \
  -L ${interval_list} \
  -R /nfs/tx/in/CNV_WGS/BWA_INDEX_hs37d5/hs37d5.fa \
  -imr OVERLAPPING_ONLY \
  -I ${bam_or_cram} \
  --format HDF5 \
  -O ${out_dir}/${sample}".hdf5"
