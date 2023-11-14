#!/usr/bin/env bash
export JAVA_HOME="/home/am5153/miniconda3/envs/java17/bin"
export JAR_PATH="/nfs/informatics/data/am5153/bin/gatk-4.4.0.0/gatk-package-4.4.0.0-local.jar"
# should be the output of PreprocessIntervals.1.sh -- padded exomeKit.bed file
sample_file_list="$1"
sample_hdf5OrTSV=$(sed -n -e "$SGE_TASK_ID p" ${sample_file_list}) # could be a filtered interval list, or a shard interval_list
# for hdf5
sample_name=$(basename ${sample_hdf5OrTSV} '.realn.recal.hdf5')
sample_index=$(expr $SGE_TASK_ID - 1)
contig_ploidy_calls_dir="$2"
shard_ct="$3"
model_shard=$(seq 1 ${shard_ct} | while read -r shard; do echo --model-shard-path /nfs/tx/in/CNV_WES/GATK-gCNV/tx-6278_IC/Agilent325/00${shard}/Agilent325Cohort-model; done)
calls_shard=$(seq 1 ${shard_ct} | while read -r shard; do echo --calls-shard-path /nfs/tx/in/CNV_WES/GATK-gCNV/tx-6278_IC/Agilent325/00${shard}/Agilent325Cohort-calls; done) 
#out_dir="$(pwd)/00$SGE_TASK_ID"
#out_prefix="$4"
# Select cram or bam

#source ~/miniconda3/etc/profile.d/conda.sh
#conda activate gatk_new
#alias python=/home/am5153/miniconda3/envs/gatk_new/bin/python
mkdir -p ${sample_name}
# Running in Cohort Mode
$JAVA_HOME/java -jar $JAR_PATH PostprocessGermlineCNVCalls \
  ${model_shard} \
  ${calls_shard} \
  --allosomal-contig X --allosomal-contig Y \
  --contig-ploidy-calls ${contig_ploidy_calls_dir} \
  --sample-index ${sample_index} \
  --output-genotyped-intervals ${sample_name}/genotyped-intervals.${sample_name}.vcf.gz \
  --output-genotyped-segments ${sample_name}/genotyped-segments.${sample_name}.vcf.gz \
  --output-denoised-copy-ratios ${sample_name}/denoised-copy-ratios.${sample_name}.tsv \
  --sequence-dictionary /nfs/tx/in/CNV_WGS/BWA_INDEX_hs37d5/hs37d5.dict 
