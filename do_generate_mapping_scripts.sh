contigs=~/genomes/contigs/hg19_contigs.txt
src_copy=/net/eichler/vol7/home/psudmant/genomes/index_files/mrsfast_hg19
index=/var/tmp/psudmant/mrsfast_hg19/hg19_masked

dir=/net/eichler/vol19/projects/apes/nobackups/psudmant/ancient_genomes/UstIshim/mapping
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/kidd8/mapping
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/hg19_1kg/

#contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/sequence_index_generation/contigs/merged_PB_gaps.contigs
#src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/sequence_index_generation/additional_sequence/merged_PB_gaps
#index=/var/tmp/psudmant/merged_PB_gaps/merged_PB_gaps.fa
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_PB_gaps

#contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/PB_gap_alternate_sequence_STR/contigs/merged_pacbio_gaps.contigs
#src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/PB_gap_alternate_sequence_STR/indexes/merged_pacbio_gaps_STR
#index=/var/tmp/psudmant/merged_pacbio_gaps_STR/merged_pacbio_gaps.fasta
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_PB_gaps_STR/

contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/NHP_alternate_sequence/contigs/merged_nhp.contigs
src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/NHP_alternate_sequence/indexes/merged_NHP
index=/var/tmp/psudmant/merged_NHP/merged_nhp.fasta
dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_NHP/

#dir=~/ev20/projects/human_diversity_sequencing/nobackups/C_team/mapping
#dir=/net/eichler/vol7/home/psudmant/ev19/projects/apes/nobackups/psudmant/sequence/GAGP_phase_II/Gorillas/mapping/
#dir=/net/eichler/vol7/home/psudmant/ev19/projects/apes/nobackups/psudmant/ancient_genomes/Loschbour/mapping
#dir=/net/eichler/vol7/home/psudmant/ev13/psudmant/sequence/CHM1
#dir=~/ev19/projects/apes/nobackups/psudmant/ape_mappings_to_species_refs/GORILLA/
#dir=/net/eichler/vol19/projects/apes/nobackups/psudmant/ancient_genomes/Loschbour/mapping
#/net/eichler/vol22/projects/kidd8/nobackups/bam_samples

#for bam in `find $dir -name *.bam | egrep "Motala12"`
#for bam in `find ~/ev19/projects/apes/nobackups/psudmant/ape_mappings_to_species_refs/GORILLA/ | egrep "Gorilla_gorilla_gorilla-9752_Suzie.bam|Gorilla_gorilla_gorilla-A962_Amani.bam|Gorilla_gorilla_gorilla-B642_Akiba_Beri.bam|Gorilla_gorilla_gorilla-B643_Choomba.bam"`

#bam_list=`cat /net/eichler/vol19/projects/apes/nobackups/psudmant/ancient_genomes/UstIshim/all_reads/all_bams.txt | tr '\n' ':'`

bam_list=`find ~/ev23/projects/human_diversity/nobackups/archaics_full_bams/ -name *.bam | egrep "ARC_Stuttgart|ARC_Loschbour"`

(for bam in $bam_list 
do

    g=`echo $bam | awk -F '/' '{print $(NF)}' | sed 's/.bam//g'`
    #g="ARC_UstIshim"
    g="ARC_${g}"
    outdir=$dir/$g/$g
    mkdir -p $outdir
	ompi_server_file=$outdir/ompi_server_file.txt
	python generate_mapping_scripts.py --contigs $contigs --src_copy $src_copy  --index $index --input_bam $bam --ompi_server_file $ompi_server_file --outdir $outdir --RUNNER_slots "100-100" --RUNNER_mfree "6G" --WRANGLER_mfree "15G"

	#python generate_mapping_scripts.py --contigs $contigs --src_copy $src_copy  --index $index --input_bam $bam --ompi_server_file $ompi_server_file --outdir $outdir --RUNNER_slots "50-100" --RUNNER_mfree "5G" --WRANGLER_mfree "20G"
	pushd $outdir; bash do_map.sh; popd
done) | egrep -v "EEE_Lab"

