import os
from optparse import OptionParser



if __name__=="__main__":
    
    opts = OptionParser()
    opts.add_option('','--contigs',dest='contigs',default=None)
    opts.add_option('','--ompi_server_file',dest='ompi_server_file',default=None)
    opts.add_option('','--src_copy',dest='src_copy',default=None)
    #opts.add_option('','--dest_copy',dest='dest_copy',default=None)
    opts.add_option('','--index',dest='index',default=None)
    opts.add_option('','--input_bam',dest='input_bam',default=None)
    opts.add_option('','--outdir',dest='outdir',default=None)
    opts.add_option('','--template_dir',dest='template_dir',default='/net/eichler/vol7/home/psudmant/EEE_Lab/projects/new_mapping_pipeline/templates')
    
    opts.add_option('','--RUNNER_slots',dest='RUNNER_slots',default="35-50")
    opts.add_option('','--RUNNER_mfree',dest='RUNNER_mfree',default="8G")
    opts.add_option('','--READER_mfree',dest='READER_mfree',default="4G")
    opts.add_option('','--WRANGLER_mfree',dest='WRANGLER_mfree',default="30G")
    
    (o,args) = opts.parse_args()
     
    template_dir=o.template_dir 

    reader_template=open('%s/mpi_READER.sh'%template_dir).read()
    runner_template=open('%s/mpi_RUNNER.sh'%template_dir).read()
    wrangler_template=open('%s/mpi_WRANGLER.sh'%template_dir).read()
    do_map_template=open('%s/do_map.sh'%template_dir).read()
    
    dict_hash={'ompi_server_file':o.ompi_server_file,'bam_files':o.input_bam,'src':o.src_copy,'index':o.index,'contigs':o.contigs,'outdir':o.outdir}
    
    RUNNER_dict = dict_hash.copy()
    RUNNER_dict["slots_range"] = o.RUNNER_slots 

    DOMAP_dict = {"RUNNER_mfree":o.RUNNER_mfree,
                   "READER_mfree":o.READER_mfree,
                   "WRANGLER_mfree":o.WRANGLER_mfree}
    
    F_READER=open('%s/mpi_READER.sh'%o.outdir,'w')
    F_RUNNER=open('%s/mpi_RUNNER.sh'%o.outdir,'w')
    F_WRANGLER=open('%s/mpi_WRANGLER.sh'%o.outdir,'w')
    F_DOMAP=open('%s/do_map.sh'%o.outdir,'w')

    F_READER.write(reader_template%dict_hash)
    F_RUNNER.write(runner_template%RUNNER_dict)
    F_WRANGLER.write(wrangler_template%dict_hash)
    F_DOMAP.write(do_map_template%DOMAP_dict)

    F_READER.close()
    F_RUNNER.close()
    F_WRANGLER.close()
    F_DOMAP.close()
    
    try:
        os.mkdir('%s/log'%o.outdir)
    except Exception,e:
        #print "log folder already made"
        pass
    #print reader_template%dict_hash

