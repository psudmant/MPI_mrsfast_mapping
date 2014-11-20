#!/bin/bash

# Define reference that reads will be mapped to.
contigs=~psudmant/genomes/contigs/hg19_contigs.txt
src_copy=/net/eichler/vol7/home/psudmant/genomes/index_files/mrsfast_hg19
index=/var/tmp/psudmant/mrsfast_hg19/hg19_masked

# Get options from the user.
while getopts :c:s:i: OPTION
do
  case $OPTION in
    c)
      contigs=$OPTARG
      ;;
    s)
      src_copy=$OPTARG
      ;;
    i)
      index=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

shift $(($OPTIND-1))

if [[ "$#" -ne "2" ]]
then
    echo -e "Usage: $0 bam_list output_dir > job_id_triplets.txt\n"
    echo -e "\tbam_list: GENOME_NAME FULL_PATH_TO_BAM"
    echo -e "\toutput_dir: FULL_PATH_TO_OUTPUT_DIR"
    exit 1
fi

# Define path to list of BAMs.
bam_list=$1

# Define the output directory for wssd_out_files.
dir=$2

# Get the location of this script.
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Loop through a file of absolute paths to BAMs and generate a script for each
# path. Scripts and output will be grouped by BAM name in the output directory.
while read line
do
    set -- $line
    sample=$1
    bam=$2
    g=`echo $bam | awk -F '/' '{print $(NF)}' | sed 's/.bam//g'`
    outdir=$dir/$sample/$g
    mkdir -p $outdir
	ompi_server_file=$outdir/ompi_server_file.txt
	python ~psudmant/EEE_Lab/projects/new_mapping_pipeline/generate_mapping_scripts.py --template_dir ${script_dir}/templates --contigs $contigs --src_copy $src_copy  --index $index --input_bam $bam --ompi_server_file $ompi_server_file --outdir $outdir --RUNNER_slots "20-50" --RUNNER_mfree "6G" --WRANGLER_mfree "40G"
	pushd $outdir; bash do_map.sh; popd
done < ${bam_list} | egrep "^([0-9]+){3}"
