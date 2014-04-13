#contigs=~/genomes/contigs/hg19_contigs.txt
#src_copy=/net/eichler/vol7/home/psudmant/genomes/index_files/mrsfast_hg19
#index=/var/tmp/psudmant/mrsfast_hg19/hg19_masked
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/hg19_1kg/

#contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/sequence_index_generation/contigs/merged_PB_gaps.contigs
#src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/sequence_index_generation/additional_sequence/merged_PB_gaps
#index=/var/tmp/psudmant/merged_PB_gaps/merged_PB_gaps.fa
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_PB_gaps

contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/PB_gap_alternate_sequence_STR/contigs/merged_pacbio_gaps.contigs
src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/PB_gap_alternate_sequence_STR/indexes/merged_pacbio_gaps_STR
index=/var/tmp/psudmant/merged_pacbio_gaps_STR/merged_pacbio_gaps.fasta
dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_PB_gaps_STR/

#contigs=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/contigs/NHP.contigs
#src_copy=/net/eichler/vol7/home/psudmant/public_html/WorldWide_SD_diversity/mapping_to_alternate_sequences/additional_sequence/NHP
#index=/var/tmp/psudmant/NHP/NHP.fa
#dir=/net/eichler/vol20/projects/human_diversity_sequencing/nobackups/mapping_to_additional_sequence/mapping_to_NHP_seq

#dir=/net/eichler/vol19/projects/human_population_sequencing/nobackups/psudmant/human_diversity/mapping/Reich_11_A_team
#dir=/net/eichler/vol19/projects/human_population_sequencing/nobackups/psudmant/human_diversity/mapping/Reich_14_B_team
#dir=/net/eichler/vol7/home/psudmant/ev19/projects/apes/nobackups/psudmant/sequence/GAGP_phase_II/Gorillas/mapping/
#dir=/net/eichler/vol7/home/psudmant/ev20/projects/human_diversity_sequencing/nobackups/malay_genomes/mapping
#dir=/net/eichler/vol23/projects/human_diversity/nobackups/PCR_free_genomes/mapping

#dir=~/ev20/projects/human_diversity_sequencing/nobackups/C_team/mapping
#dir=/net/eichler/vol7/home/psudmant/ev19/projects/apes/nobackups/psudmant/sequence/GAGP_phase_II/Gorillas/mapping/
#dir=/net/eichler/vol7/home/psudmant/ev19/projects/apes/nobackups/psudmant/ancient_genomes/Loschbour/mapping
#dir=/net/eichler/vol7/home/psudmant/ev13/psudmant/sequence/CHM1
#dir=~/ev19/projects/apes/nobackups/psudmant/ape_mappings_to_species_refs/GORILLA/
#dir=/net/eichler/vol19/projects/apes/nobackups/psudmant/ancient_genomes/Loschbour/mapping
#/net/eichler/vol22/projects/kidd8/nobackups/bam_samples

#FAILURES
#"LP6005519-DNA_A12|LP6005519-DNA_B08|LP6005519-DNA_C11|LP6005519-DNA_D10|LP6005519-DNA_E10|LP6005519-DNA_E11|LP6005519-DNA_F11|LP6005519-DNA_G02|LP6005519-DNA_G11|LP6005519-DNA_H04|LP6005592-DNA_C01|LP6005592-DNA_C02|LP6005592-DNA_C05|LP6005592-DNA_D03|LP6005592-DNA_E02|LP6005592-DNA_F03|LP6005592-DNA_G03|LP6005592-DNA_G05|LP6005592-DNA_H01|LP6005592-DNA_H03|LP6005619-DNA_B01|LP6005677-DNA_A02|LP6005677-DNA_A04|LP6005677-DNA_C04|LP6005677-DNA_D04|LP6005677-DNA_E03|LP6005677-DNA_F01|NA12878|NA18956|NA19238"
#LP6005519-DNA_A12 LP6005519-DNA_B08 LP6005519-DNA_C11 LP6005519-DNA_D10 LP6005519-DNA_E10 LP6005519-DNA_E11 LP6005519-DNA_F11 LP6005519-DNA_G02 LP6005519-DNA_G11 LP6005519-DNA_H04 LP6005592-DNA_C01 LP6005592-DNA_C02 LP6005592-DNA_C05 LP6005592-DNA_D03 LP6005592-DNA_E02 LP6005592-DNA_F03 LP6005592-DNA_G03 LP6005592-DNA_G05 LP6005592-DNA_H01 LP6005592-DNA_H03 LP6005619-DNA_B01 LP6005677-DNA_A02 LP6005677-DNA_A04 LP6005677-DNA_C04 LP6005677-DNA_D04 LP6005677-DNA_E03 LP6005677-DNA_F01 NA12878 NA18956 NA19238

#for bam in `cat /net/eichler/vol19/projects/apes/nobackups/psudmant/ancient_genomes/Loschbour/bams` 
#for bam in `find /net/eichler/vol22/projects/kidd8/nobackups/bam_samples/ -name *.bam | egrep "NA12878|NA18956|NA19238"`
#for bam in `find /net/eichler/vol22/projects/kidd8/nobackups/bam_samples/ -name *.bam | egrep "NA19238"`
#for bam in `find /net/eichler/vol7/home/psudmant/ev20/projects/human_diversity_sequencing/nobackups/C_team_batch2_85 -name *.bam | egrep "LP6005519-DNA_A12|LP6005519-DNA_B08|LP6005519-DNA_C11|LP6005519-DNA_D10|LP6005519-DNA_E10|LP6005519-DNA_E11|LP6005519-DNA_F11|LP6005519-DNA_G02|LP6005519-DNA_G11|LP6005519-DNA_H04|LP6005592-DNA_C01|LP6005592-DNA_C02|LP6005592-DNA_C05|LP6005592-DNA_D03|LP6005592-DNA_E02|LP6005592-DNA_F03|LP6005592-DNA_G03|LP6005592-DNA_G05|LP6005592-DNA_H01|LP6005592-DNA_H03|LP6005619-DNA_B01|LP6005677-DNA_A02|LP6005677-DNA_A04|LP6005677-DNA_C04|LP6005677-DNA_D04|LP6005677-DNA_E03|LP6005677-DNA_F01|NA12878|NA18956|NA19238"`
#for bam in `find $dir -name *.bam | egrep "Gorilla_beringei_beringei_Zirikana|Gorilla_beringei_beringei_Imfura|Gorilla_beringei_beringei_Tuck|Gorilla_beringei_graueri_Itebero|Gorilla_beringei_graueri_Ntabwoba|Gorilla_beringei_beringei_Kaboko"`
#for bam in `find $dir -name *.bam | egrep "Tumani|Serufuli|Maisha|Tuck|Umurimo"`
#for bam in `find $dir -name *.bam | egrep "Turimaso|Pinga|Dunia"`
#for bam in `find $dir -name *.bam | egrep "Motala12"`
#for bam in `find ~/ev19/projects/apes/nobackups/psudmant/ape_mappings_to_species_refs/GORILLA/ | egrep "Gorilla_gorilla_gorilla-9752_Suzie.bam|Gorilla_gorilla_gorilla-A962_Amani.bam|Gorilla_gorilla_gorilla-B642_Akiba_Beri.bam|Gorilla_gorilla_gorilla-B643_Choomba.bam"`
(
#for bam in `find /net/eichler/vol23/projects/human_diversity/nobackups/PCR_free_genomes/20140203_broad_high_cov_pcr_free_BAMs -name *.bam`
#for bam in `find /net/eichler/vol23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams -name *.bam | grep ADM_ACB_HG01879_M`
#for bam in `find  /net/eichler/vol7/home/psudmant/ev20/projects/human_diversity_sequencing/nobackups/symlinked_bams/renamed_bams/ -name *.bam`
#for bam in /net/eichler/vol19/projects/CHM1_project/nobackups/UWIllumina/chm1.bam
#for bam in /net/eichler/vol20/projects/human_diversity_sequencing/nobackups/hg19_1kg/bam/hg19_36x.bam
#for bam in /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_ACB_HG01879_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_ASW_NA19625_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_CLM_HG01112_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_MXL_NA19648_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_PEL_HG01565_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/ADM_PUR_HG01051_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_ESN_HG02922_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_GWD_HG02568_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_LWK_NA19017_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_MSL_HG03052_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_YRI_NA19238_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_YRI_NA19239_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/AFR_YRI_NA19240_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/EA_CDX_HG00759_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/EA_CHB_NA18525_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/EA_CHS_HG00419_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/EA_JPT_NA18939_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/EA_KHV_HG01595_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/SA_BEB_HG03006_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/SA_GIH_NA20845_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/SA_ITU_HG03742_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/SA_PJL_HG01583_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/SA_STU_HG03642_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_CEU_NA12878_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_CEU_NA12891_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_CEU_NA12892_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_FIN_HG00268_F.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_GBR_HG00096_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_IBS_HG01500_M.bam /net/eichler/vol7/home/psudmant/ev23/projects/human_diversity/nobackups/PCR_free_genomes/symlinked_bams/WEA_TSI_NA20502_F.bam  /net/eichler/vol7/home/psudmant/ev20/projects/human_diversity_sequencing/nobackups/hg19_1kg/bam/hg19_36x.bam /net/eichler/vol7/home/psudmant/ev20/projects/human_diversity_sequencing/nobackups/CHM1_washU/bam/washU_CHM1.bam /net/eichler/vol19/projects/CHM1_project/nobackups/UWIllumina/chm1.bam
do
    g=`echo $bam | awk -F '/' '{print $(NF)}' | sed 's/.bam//g'`
    outdir=$dir/$g/$g
    mkdir -p $outdir
	ompi_server_file=$outdir/ompi_server_file.txt
	#bam=`ls $dir/$g/$g/BAMs/*.bam`
	python generate_mapping_scripts.py --contigs $contigs --src_copy $src_copy  --index $index --input_bam $bam --ompi_server_file $ompi_server_file --outdir $outdir --RUNNER_slots "50-50" --RUNNER_mfree "5G" --WRANGLER_mfree "20G"
	#python generate_mapping_scripts.py --contigs $contigs --src_copy $src_copy  --index $index --input_bam $bam --ompi_server_file $ompi_server_file --outdir $outdir --RUNNER_slots "50-100" --RUNNER_mfree "5G" --WRANGLER_mfree "20G"
	#echo 'sleep 2; pushd '$outdir'; bash do_map.sh; popd'
	#echo 'pushd '$outdir'; bash do_map.sh; popd'
	pushd $outdir; bash do_map.sh; popd
done) | egrep -v "EEE_Lab"
