#!/usr/bin/env bash
export JAVA_HOME="/home/am5153/miniconda3/envs/java17/bin"
export JAR_PATH="/nfs/informatics/data/am5153/bin/gatk-4.4.0.0/gatk-package-4.4.0.0-local.jar"
exomeKit_bed="$1"
$JAVA_HOME/java -jar $JAR_PATH PreprocessIntervals \
  -R /nfs/tx/in/CNV_WGS/BWA_INDEX_hs37d5/hs37d5.fa \
  -L ${exomeKit_bed} \
  --bin-length 0 \
  --padding 250 \
  -imr OVERLAPPING_ONLY \
  --output ${exomeKit_bed}".targets.preprocessed.interval_list"
