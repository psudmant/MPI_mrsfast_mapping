module load openmpi/1.5.3    
q='all.q'

rm ./log/*
#rm ./comm_sock.socket
rm -f ./ompi_server_file.txt*
#killall ompi-server
ompi-server -r ./ompi_server_file.txt &
echo $! >./ompi_server_file.txt_proc

ret1=`qsub -h -q $q -l h_vmem=%(READER_mfree)s ./mpi_READER.sh | grep job| awk '{print $3}'`
ret2=`qsub -h -q $q -l h_vmem=%(RUNNER_mfree)s ./mpi_RUNNER.sh | grep job|awk '{print $3}'`
ret3=`qsub -h -q $q -l h_vmem=%(WRANGLER_mfree)s ./mpi_WRANGLER.sh |grep job| awk '{print $3}'`
echo $ret1 $ret2 $ret3
