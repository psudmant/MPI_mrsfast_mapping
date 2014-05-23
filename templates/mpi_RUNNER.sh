#!/bin/bash
# Specify the shell for this job
#$ -S /bin/bash 
#ulimit -c 0
 # Tell Sun Grid Engine to send an email when the job begins
 # and when it ends.

. /etc/profile.d/modules.sh

unset LD_LIBRARY_PATH; unset PYTHONPATH

if test ! -z $MODULESHOME; then
		  module purge
		  module load modules modules-init modules-gs
			module load zlib/1.2.6
			module load hdf5/1.8.8
			module load lzo/2.06
			module load python/2.7.2 
			module load pytables/2.3.1_hdf5-1.8.8    
			
			export PYTHONPATH=$PYTHONPATH:/net/eichler/vol7/home/psudmant/EEE_Lab/1000G/1000genomesScripts
			export PYTHONPATH=$PYTHONPATH:/net/eichler/vol7/home/psudmant/EEE_Lab/1000G/1000genomesScripts/cython_apis
			export PYTHONPATH=$PYTHONPATH:/net/eichler/vol7/home/psudmant/EEE_Lab/projects/common_code

       if [ "$MODULES_REL" = "RHEL6" ]; then
							 module load numpy/1.6.1 scipy/0.10.0
               module load openmpi/1.5.3
               echo "Loaded openmpi/1.5.3 for $MODULES_REL"
       elif [ "$MODULES_REL" = "RHEL5" ]; then
               module load openmpi/1.4.4
               echo "Loaded openmpi/1.4.4 for $MODULES_REL"
       else
               echo "No valid OpenMPI available for ${MODULES_REL}" >&2
               exit 2
       fi
fi


#$ -V #export environment
#$ -pe orte %(slots_range)s
#$ -cwd
# Specify the location of the output
#$ -o ./log
#$ -e ./log

pversion=`which python`
echo "Got $NSLOTS slots" 
echo "PATH=$PATH" 
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
echo "P4_RSHCOMMAND=$P4_RSHCOMMAND" 
echo "machine_file=$TMPDIR/machines" 
echo "JOB_ID=$JOB_ID" 
echo "TEMDPIR=$TMPDIR" 
echo "HOSTNAME=$HOSTNAME"
echo "WHICH_PYTHON=$pversion"

echo "running mpirun...next output should be from batch_node_copy.py"



ompi_server_file=%(ompi_server_file)s

src=%(src)s
index=%(index)s
contigs=%(contigs)s


#contigs=~/genomes/contigs/hg19_contigs.txt
#src=/net/eichler/vol7/home/psudmant/genomes/index_files/mrsfast_hg19
#index=/var/tmp/psudmant/mrsfast_hg19/hg19_masked
#src=/net/eichler/vol7/home/psudmant/genomes/index_files/mrsfast_smalltest
#index=/var/tmp/psudmant/mrsfast_smalltest/chrY.fa.masked

mpirun -x PATH -x LD_LIBRARY_PATH --prefix $MPIBASE -mca plm ^rshd -mca btl ^openib -n $NSLOTS python /net/eichler/vol7/home/psudmant/EEE_Lab/projects/batch_node_copy/code/batch_node_copy.py  --source $src --dest /var/tmp/psudmant --pre_sync_commands "mkdir /var/tmp/psudmant; chgrp -R eichlerlab /var/tmp/psudmant; chmod g+rw -R /var/tmp/psudmant" --post_sync_commands "chgrp -R eichlerlab /var/tmp/psudmant;chmod g+w -R /var/tmp/psudmant"

echo "running mpirun...next output should be from super_mapper.py"
mpirun -x PATH -x LD_LIBRARY_PATH --prefix $MPIBASE -mca plm ^rshd -mca btl ^openib -n $NSLOTS --ompi-server file:$ompi_server_file    python /net/eichler/vol7/home/psudmant/EEE_Lab/projects/new_mapping_pipeline/super_mapper.py --task RUNNER --index $index --mrsfast_binary /net/eichler/vol7/home/psudmant/EEE_Lab/projects/mrsfast/READ_PATCHED_mrsfast-2.5.0.4/mrsfast --mrsfast_opts "-n 0 -e 2 --crop 36" --contigs $contigs 

