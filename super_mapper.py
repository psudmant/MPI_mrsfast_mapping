from add_positions_to_vect import *
import tables
from kitz_wssd.wssd_common_v2 import *
import traceback
from optparse import OptionParser
import subprocess as sub
import pysam
from collections import defaultdict
import threading
from multiprocessing import Process
import logging
import tempfile

import socket
import sys,os
from mpi4py import MPI
from sys import stderr
from sys import stdout
import time
from  time import sleep
import difflib
import subprocess as sub
import numpy as np
import glob
import gc


TAG_READY=1
TAG_DIE=2
TAG_DONE_JOB=3
TAG_DONE_COPY=4
TAG_RUN_JOB=5
TAG_ERROR=6
TAG_RUNNER_READY=7
TAG_READER_READY=8
TAG_READER_REQUEST_RUNNER=9
TAG_NO_FREE_RUNNERS = 10
TAG_FREE_RUNNER = 11
TAG_TRANSFER = 12
TAG_SEND_MAPPINGS = 13
TAG_FINISH = 14


READ_BLOCK_SIZE = int(10e6) ###this ist he basepair chunk
SEND_BLOCK_SIZE = int(2e6)
#MAX_COPY_PROCS=40
dt = np.dtype('a37') ###NEED ONE EXTRA!!! for the \0


def mkdir(dir,file):
    ls_dir = os.listdir(dir)
    if(not(file_exists(ls_dir,file))):
        command = "mkdir %s/%s"%(dir,file)
        os.system(command)
    return "%s/%s"%(dir,file)

def unlink_all(to_unlink):
    for f in to_unlink:
        os.unlink(f)

def do_command(type,rank,proc_name,cmd):
    #print "CLIENT: cmd - %s"%(cmd)
    p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
    output,errors = p.communicate()
    print "%s %s: rank %d, o: %s e:%s\n%s"%(type,proc_name,rank,output,errors,cmd)
    ret_code = p.returncode
    if ret_code != 0: print "".join(["********************\n" for i in xrange(1)])

    return ret_code

def READER_host_loop(comm,icomm_to_RUNNER,my_rank,n_procs,proc_name,input_file,icomm_to_WRANGLER,chr=None):
    
    chunk_size=READ_BLOCK_SIZE
    
    all_chunks = []
    """
    code to get the contigs  for subdividing the read processes up - 
    turns out simple lineage run through is more than reasonable, 
    thus, "ALL"
    """

    ####
    all_chunks =  [["ALL",-1,01]]

    ##OK, now, gather up your babies, and give'm work
    
    status=MPI.Status()
    
    l_READER_ranks_ready = []
    l_RUNNER_ranks_ready = []
    ALL_CHUNKS_READ = False

    ####FIRST get ALL THE READERS
    n_readers = n_procs - 1 ##all but the host
    for i in xrange(1,n_procs):
        data = comm.recv(source = i,tag=TAG_READER_READY,status=status)
        print "READER HOST %s: %d ready, %s, with data: %s"%(proc_name,i,status,data)
        node=data["proc_name"]
        l_READER_ranks_ready.append(i)
    
    print "READER HOST - ALL READERS READY TO ROLL -  ranks:", l_READER_ranks_ready
    
    ####THEN GET ALL THE RUNNERS

    print "READER HOST - waiting for RUNNER heartbeats - icomm rank: %d:"%(icomm_to_RUNNER.Get_rank())
    n_runners =    icomm_to_RUNNER.Get_remote_group().Get_size()
    for i in xrange(0,n_runners):
        print "WAITING TO RECEIVE from RUNNERs..."
        data = icomm_to_RUNNER.recv(source=i,tag=MPI.ANY_TAG)
        status=MPI.Status()    
        print i, status.source
        #node=data["proc_name"]
        l_RUNNER_ranks_ready.append(i)
        print "RUNNER rank %d ready, %s, with data: %s"%(i,status.source,data)

    print "READER HOST - ALL RUNNERS READY TO ROLL -  ranks:", l_RUNNER_ranks_ready
    
    for rank in l_READER_ranks_ready:
        if len(all_chunks)==0:
            break
        chunk=all_chunks.pop(0)
        print "HOST %s: rank %d sending data (%s:%d-%d) to %d"%(proc_name,my_rank,chunk[0],chunk[1],chunk[2],rank)
        comm.send(chunk,tag=TAG_RUN_JOB,dest=rank)
        
    #while len(all_chunks)>0:
    while 1:
        comm_msg = comm.Iprobe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
        if comm_msg:
            status = MPI.Status()
            data = comm.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            
            if status.tag == TAG_DONE_JOB:    
                rank = status.source
                print "HOST %s: rank %d recieved a message - JOB DONE from %d"%(proc_name,my_rank,status.source)
                if len(all_chunks)>0:
                    chunk=all_chunks.pop(0)
                    print "HOST %s: rank %d sending data (%s:%d-%d) to %d"%(proc_name,my_rank,chunk[0],chunk[1],chunk[2],status.source)
                    comm.send(chunk,tag=TAG_RUN_JOB,dest=status.source)
                    print "HOST %s: rank %d - %d chunks left to read in"%(proc_name,my_rank,len(all_chunks))
                else:
                    print "HOST %s: rank %d - all chunks read in!"%(proc_name,my_rank)
                    ALL_CHUNKS_READ = True    
                    
            elif status.tag==TAG_READER_REQUEST_RUNNER:
                print "HOST %s: rank %d - got comm message from %d "%(proc_name,my_rank, status.source)
                if status.tag == TAG_READER_REQUEST_RUNNER:
                    #if RUNNER
                    if len(l_RUNNER_ranks_ready)>0:
                        rank = l_RUNNER_ranks_ready.pop(0)
                        print "HOST %s: rank %d - sending FREE RUNNER rank %d to  %d "%(proc_name,my_rank, rank, status.source)
                        comm.send(rank,tag=TAG_FREE_RUNNER,dest=status.source)
                    else:
                        print "HOST %s: rank %d - sending NO_FREE_RUNNERS to  %d "%(proc_name,my_rank, status.source)
                        comm.send(-1,tag=TAG_NO_FREE_RUNNERS,dest=status.source)

        icomm_msg = icomm_to_RUNNER.Iprobe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
        if icomm_msg:
            status = MPI.Status()
            data = icomm_to_RUNNER.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            if status.tag == TAG_RUNNER_READY:
                rank = status.source
                print "READER HOST GOT MESSAGE RUNNER READY with rank: %d"%rank
                l_RUNNER_ranks_ready.append(rank)
        
        if ALL_CHUNKS_READ and (len(l_RUNNER_ranks_ready) == n_runners) and (len(l_READER_ranks_ready) == n_readers):
            print "HOST %s: rank %d - ALL CHUNKS READ AND - ALL READERS READY - ALL RUNNERS READER - DONE  "%(proc_name,my_rank)
            break
    
    
    ##
    #TELL THE WRANGLER TO OUTPUT
    icomm_to_WRANGLER.send(None,dest=0,tag=TAG_FINISH)
    #SHUT DOWN THE RUNNERS
    
    for i in xrange(0,n_runners):
        print "shutting down RUNNER %d..."%(i)
        icomm_to_RUNNER.send(dest=i,tag=TAG_DIE)
    #WAIT FOR THE WRANGLER TO FINISH

    icomm_to_WRANGLER.recv(None,source=0,tag=TAG_DONE_JOB)
    #SHUT DOWN
    print "HOST %s: rank %d ALL WORKER THREADS DONE"%(proc_name,my_rank)
    print "HOST %s: rank %d SHUTTING DOWN"%(proc_name,my_rank)



def READER_client_SEND_READS(reads_block,n_reads,proc_name,myrank,comm,icomm_to_RUNNER):

        print "READER CLIENT %s: %d requested RUNNER..."%(proc_name,myrank)
        comm.send(tag=TAG_READER_REQUEST_RUNNER,dest=0)
        status = MPI.Status()
        msg = comm.recv(source=0,tag=MPI.ANY_TAG,status=status)
        print "READER CLIENT %s: %d got message with TAG %d"%(proc_name,myrank,status.tag)
        
        while status.tag != TAG_FREE_RUNNER:
            print "READER CLIENT %s: %d requested FAILED"%(proc_name,myrank)
            sleep(1)
            comm.send(tag=TAG_READER_REQUEST_RUNNER,dest=0)
            status = MPI.Status()
            msg = comm.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            print "READER CLIENT %s: %d requested RUNNER..."%(proc_name,myrank)
        RUNNER_rank = msg
        print "READER CLIENT %s: %d got RUNNER rank %d"%(proc_name,myrank,msg)
        print "READER CLIENT %s: %d no will send data to RUNNER... rank %d"%(proc_name,myrank,msg)
        icomm_to_RUNNER.send(n_reads,dest=RUNNER_rank,tag=TAG_RUN_JOB)
        icomm_to_RUNNER.Send([reads_block,MPI.CHAR],dest=RUNNER_rank,tag=TAG_TRANSFER)
        del reads_block
        print "READER CLIENT %s: %d done sendiing data to RUNNER... rank %d"%(proc_name,myrank,msg)

def READER_client_extract_reads_from_bam(chr,start,end,bamfile,proc_name,myrank,comm,icomm_to_RUNNER):
    
    #### THIS READS IN EACH BLOCK then SENDS it to the RUNNER
    ###
    #reads_block = np.empty(SEND_BLOCK_SIZE,dtype = dt)
    reads_block = np.empty(SEND_BLOCK_SIZE,dtype = dt)

    print "READER CLIENT %s: %d ready to read %s:%d-%d "%(proc_name,myrank,chr,start,end)
    t=time.time()
    curr_pos = 0
    s_sz=36    
    if chr=="ALL":
        total_read_in = 0
        for l in bamfile.fetch(until_eof=True):
            #print l
            total_read_in+=1
            n_to_do=l.rlen/s_sz
            
            ##!!
            #n_to_do = 1

            for k in xrange(n_to_do):
                reads_block[curr_pos]=l.seq[(k*s_sz):(k*s_sz+s_sz)]
                curr_pos+=1
                if curr_pos==SEND_BLOCK_SIZE: break
            if curr_pos==SEND_BLOCK_SIZE:
                print "READER CLIENT %s: %d read in %d reads "%(proc_name,myrank,total_read_in)
                print reads_block
                curr_pos=0
                READER_client_SEND_READS(reads_block,SEND_BLOCK_SIZE,proc_name,myrank,comm,icomm_to_RUNNER)
                ##!!
                #    break
        
        if curr_pos!=0:
            small_reads_block = np.empty(curr_pos,dtype = dt)
            small_reads_block[:] = reads_block[:curr_pos]
            READER_client_SEND_READS(small_reads_block,curr_pos,proc_name,myrank,comm,icomm_to_RUNNER)
    
    else:
        for l in bamfile.fetch(chr,start,end):
            #print l
            n_to_do=l.rlen/36
            for k in xrange(n_to_do):
                reads_block[curr_pos]=l.seq[k*s_sz:k*s_sz+s_sz]
                curr_pos+=1
                if curr_pos==SEND_BLOCK_SIZE: break
            if curr_pos==SEND_BLOCK_SIZE:
                curr_pos=0
                READER_client_SEND_READS(reads_block,SEND_BLOCK_SIZE,proc_name,myrank,comm,icomm_to_RUNNER)
        
        if curr_pos!=0:
            small_reads_block = np.empty(curr_pos,dtype = dt)
            small_reads_block[:] = reads_block[:curr_pos]
            READER_client_SEND_READS(small_reads_block,curr_pos,proc_name,myrank,comm,icomm_to_RUNNER)

    ### make a new little block and copy stuff into it then send out
    #assert True

    print "READER CLIENT %s: %d FINISHED READING %s:%d-%d in %f seconds"%(proc_name,myrank,chr,start,end,time.time()-t)
    

def READER_client_loop(comm,icomm_to_RUNNER,my_rank,n_procs,proc_name,input_file,chr=None):
    
    comm.send({"rank":my_rank,"proc_name":proc_name},dest=0, tag=TAG_READER_READY)
    done_running=False

    bamfile=pysam.Samfile(input_file,'rb')
    
    while not done_running: 
        msg = comm.Iprobe(source=0,tag=MPI.ANY_TAG)
        sleep(1)
        print "CLIENT %s: rank %d waiting for instructions..."%(proc_name,my_rank)
        if msg:
            status = MPI.Status()
            data = comm.recv(source=0,tag=MPI.ANY_TAG,status=status)
            print "READER CLIENT %s: rank %d recieved a message - data: %s"%(proc_name,my_rank,data)
        
            if status.tag==TAG_DIE:
                print "CLIENT %s: rank %d dying..."%(proc_name,my_rank)
                comm.Barrier()
                done_running=True
                exit(0)
            elif status.tag==TAG_RUN_JOB:
                print "READER CLIENT %s: rank %d will now run job - data: %s"%(proc_name,my_rank,data)
                chr,start,end=data
                READER_client_extract_reads_from_bam(chr,start,end,bamfile,proc_name,my_rank,comm,icomm_to_RUNNER)
                comm.send(dest=0,tag=TAG_DONE_JOB)
        #msg = comm.Iprobe(source=0,tag=MPI.ANY_TAG)
        #if msg:
        #    status = MPI.Status()
        #    data = comm.recv(source=0,tag=MPI.ANY_TAG,status=status)
        #    print "CLIENT %s: rank %d recieved a message - data: %s"%(proc_name,myrank,data)
    

def READER(comm,my_rank,n_procs,proc_name,input_file,chr=None):

    ###CREATE SOCKET
    reader_info = MPI.INFO_NULL
    runner_info = MPI.INFO_NULL
    RUNNER_port = None
    service=None
    if my_rank==0:
        service = "READER"
        print "READER RANK 0 got here"
        RUNNER_port = MPI.Open_port(runner_info)
        print "READER got port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
        #print "SRSLY_READER got port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
        #print "UNPUBLISHED got port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
        MPI.Publish_name(service, runner_info, RUNNER_port)
        print "READER published  port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
    else:
        RUNNER_port = None

    print "READER waiting to accept %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
    icomm_to_RUNNER = comm.Accept(RUNNER_port,runner_info,0)
    #RUNNER_comm = icomm_to_RUNNER.Get_remote_group()
    print "READER accepted communication (%d - %s)"%(my_rank,proc_name)
    print "READER icomm_size %d icomm_rank %d (%d - %s)"%(comm.Get_size(),comm.Get_rank(),my_rank,proc_name)
    
    ###CONNECT TO WRANGLER
    WRANGLER_port = None
    service= None
    wrangler_info = MPI.INFO_NULL
    if my_rank==0:
        service = "WRANGLER_from_READER"
        WRANGLER_port = MPI.Open_port(wrangler_info)
        print "READER got another port %s (%d - %s)"%(WRANGLER_port, my_rank,proc_name)
        MPI.Publish_name(service, wrangler_info, WRANGLER_port)
    else:
        WRANGLER_port = None
    print "READER waiting to accept %s (%d - %s)"%(WRANGLER_port, my_rank,proc_name)
    icomm_to_WRANGLER = comm.Accept(WRANGLER_port,wrangler_info,0)
    #RUNNER_comm = icomm_to_RUNNER.Get_remote_group()
    print "READER accepted communication (%d - %s)"%(my_rank,proc_name)

    if my_rank ==0:
        READER_host_loop(comm,icomm_to_RUNNER,my_rank,n_procs,proc_name,input_file,icomm_to_WRANGLER,chr=None)
    else:
        READER_client_loop(comm,icomm_to_RUNNER,my_rank,n_procs,proc_name,input_file,chr=None)
        #NOW THE READEr has COMMS to the Runner
        ##HERE, determine given K readers, what each will do... 

    if my_rank==0:
        MPI.Unpublish_name('READER',reader_info,RUNNER_port)
        MPI.Close_port(RUNNER_port)
        
        MPI.Unpublish_name('WRANGLER_from_READER',wrangler_info,WRANGLER_port)
        MPI.Close_port(WRANGLER_port)
        print "READER closed port and unpublished (%d - %s)"%(my_rank,proc_name)
###comm in an intracommunicator, com is an intercomunicatior
    exit(0)

def reads_block_to_string(reads_block,n_elems):
    breaks=np.empty(n_elems,dtype=np.dtype('|S1'))
    breaks[:] = '\n'
    carrots=np.empty(n_elems,dtype=np.dtype('|S1'))
    carrots[:] = '>'
    header=np.array(np.arange(n_elems),dtype=np.dtype('|S10'))
    output= np.char.add(carrots,np.char.zfill(header,10))
    output= np.char.add(output,breaks)
    output= np.char.add(output,reads_block)
    output= np.char.add(output,breaks)
    outstr= output.tostring()
    return outstr

def map_reads(fn_fifo_reads,fn_fifo_out,index,mrsfast_binary,mrsfast_opts,rank,proc_name):
    cmd = "%s --search %s %s --seq1 %s -o %s -u /dev/null"%(mrsfast_binary,index,mrsfast_opts,fn_fifo_reads,fn_fifo_out) 
    print "RANK %d proc %s doing commend: %s"%(rank,proc_name,cmd)
    do_command("MAP",rank,proc_name,cmd)

def write_reads(fn,reads_str,my_rank,proc_name):
    print "%s: rank %d planning on writing to %s"%(proc_name,my_rank,fn)
    try:
        F=open(fn,'w')
    except Exception,e:
        print "EXCEPTION!!, proc: %s rank: %d %s"%(proc_name,my_rank,e)

    print "%s: rank %d opened %s"%(proc_name,my_rank,fn)
    F.write(reads_str)
    print "%s: rank %d now writing %s"%(proc_name,my_rank,fn)
    F.close()

def RUNNER(comm,my_rank,n_procs,proc_name,work_dir,index,mrsfast_binary,mrsfast_opts,contigs,chop_chr):
    
    chr_by_idx = {}
    idx_by_chr = {}
    chr_idx = 0    
    for ln in open(contigs):
        chr,l  = ln.rstrip().split()
        if chop_chr: chr = chr.replace("chr","")
        chr_by_idx[chr_idx] = chr
        idx_by_chr[chr] = chr_idx
        chr_idx +=1
        print chr, chr_idx
        
    root=0
    runner_info = MPI.INFO_NULL
    
    if my_rank==0:
        while(1):
            sleep(1)
            print "IN THE SLEEP LOOP"
            print "RUNNER is trying to lookup port... (%d - %s)"%(my_rank,proc_name)
            try:    
                print "RUNNER is trying to lookup port... (%d - %s)"%(my_rank,proc_name)
                READER_port = MPI.Lookup_name("READER",MPI.INFO_NULL)
                break
            except Exception, e:
                print "EXCEPTION:", e 
                #traceback.print_exc()
                pass
        
        RUNNER_port = MPI.Open_port()
        print "RUNNER got port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
        MPI.Publish_name('RUNNER', runner_info, RUNNER_port)
        print "RUNNER published  port %s (%d - %s)"%(RUNNER_port, my_rank,proc_name)
    else:
        READER_port = None
        RUNNER_port = None
    
    reader_info=MPI.INFO_NULL
    print "RUNNER waiting to connect to READER... (%d - %s)"%(my_rank,proc_name)
    icomm_to_READER = comm.Connect(READER_port, reader_info, 0)
    #READER_comm = icomm_to_READER.Get_remote_group()

    #comm = MPI.COMM_WORLD.Accept(port, info, root)
    print "RUNNER connected to READER (%d - %s)"%(my_rank,proc_name)
    print "RUNNER icomm_size %d icomm_rank %d (%d - %s)"%(comm.Get_size(),comm.Get_rank(),my_rank,proc_name)

    #print "!!!!!!!!!!!RUNNER REMOVE THIS LINE!!!!"
    #do_command('RUNNER',my_rank,proc_name,'rm /dev/shm/*')
    
    comm.Barrier() #WHAT for all runners to  clean out their shm
    
    print "RUNNER waiting to connect to WRANGER... (%d - %s)"%(my_rank,proc_name)
    icomm_to_WRANGLER = comm.Accept(RUNNER_port, runner_info, 0)
    WRANGLER_group = icomm_to_WRANGLER.Get_remote_group()
    print "RUNNER  connected to WRANGER... (%d - %s)"%(my_rank,proc_name)
    print "WRANGLER_group_SIZE is...%d (%d - %s)"%(WRANGLER_group.Get_size(),my_rank,proc_name)
    
    ####send to the READER 0 that you are ready
    print "RUNNER  sending heartbeat to READER (%d - %s), icomm rank %d"%(my_rank,proc_name,icomm_to_READER.Get_rank())
    icomm_to_READER.send({"rank":my_rank,"proc_name":proc_name},dest=0, tag=TAG_RUNNER_READY)
    print "RUNNER  sending heartbeat finished (%d - %s), icomm rank %d"%(my_rank,proc_name,icomm_to_READER.Get_rank())
        
    while(1):
        ###NOW the runner has coms to the READER and to the WRANGLER
        sleep(1)
        #print "RUNNER rank: %d  %s waiting for  a message..."%(my_rank,proc_name)
        msg = icomm_to_READER.Iprobe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
        if msg:
            print "RUNNER rank: %d got a message..."%(my_rank)
            status = MPI.Status()
            n_elems = icomm_to_READER.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            if status.tag == TAG_RUN_JOB:
                reads_block = np.empty(n_elems,dtype = dt)
                t = time.time()
                print "RUNNER rank: %d starting TRANSFER"%(my_rank)
                icomm_to_READER.Recv([reads_block,MPI.CHAR],source=status.source,tag=TAG_TRANSFER)
                print "RUNNER rank: %d TRANSFER TIME %f seconds"%(my_rank,time.time()-t)
                
                tempd=tempfile.NamedTemporaryFile(prefix="rank_%d"%my_rank,dir=work_dir).name
                os.mkdir(tempd)
                #print reads_block,n_elems
                t = time.time()
                #work_dir
                fn_fifo_reads='%s/fifo_reads'%tempd
                fn_fifo_output='%s/fifo_output'%tempd
                try:
                    F_fifo_reads = os.mkfifo(fn_fifo_reads)
                    F_fifo_output = os.mkfifo(fn_fifo_output)
                    #F_fifo_out_W = open(fn_fifo_output,'w')
                except OSError, e:
                    print "RUNNER rank: %d failed FIFO construction"%(my_rank)
                
                reads_str = reads_block_to_string(reads_block,n_elems)
                read_proc = Process(target=write_reads,args = [fn_fifo_reads,reads_str,my_rank,proc_name])
                read_proc.start()
                map_proc  = Process(target=map_reads,args = [fn_fifo_reads,fn_fifo_output,index,mrsfast_binary,mrsfast_opts,my_rank,proc_name])
                map_proc.start()
                try:
                    F_fifo_out = open(fn_fifo_output)
                except Exception, e:
                    print "EXCEPTION", e
                

                chr_idxs = []
                poses = []
                edits = []    
                t2 = time.time()
                gc.disable()
                n_mappings=0
                for l in F_fifo_out:
                    nothing,nothing,chr,pos,rest =l.split("\t",4)
                    rest,ed,cig = rest.rsplit("\t",2)
                    chr_idx = idx_by_chr[chr]
                    chr_idxs.append(chr_idx)
                    poses.append(pos)
                    edits.append(ed[-1])
                    n_mappings+=1
                    #print chr, chr_idx, pos, ed[-1]
                
                chr_idxs = np.array(chr_idxs,dtype=np.uint8)
                poses = np.array(poses,dtype = np.uint32)
                edits = np.array(edits,dtype = np.uint8)
                #print chr_idxs,poses,edits, time.time()-t2
                print "RUNNER rank: %d %s requesing wrangler and sending..."%(my_rank,proc_name)
                icomm_to_WRANGLER.send(n_mappings,dest=0,tag=TAG_SEND_MAPPINGS)

                icomm_to_WRANGLER.Send([chr_idxs,MPI.UNSIGNED_CHAR],dest=0,tag=TAG_TRANSFER)
                icomm_to_WRANGLER.Send([poses,MPI.UNSIGNED],dest=0,tag=TAG_TRANSFER)
                icomm_to_WRANGLER.Send([edits,MPI.UNSIGNED_CHAR],dest=0,tag=TAG_TRANSFER)
                print "RUNNER rank: %d %s is done sending to  wrangler"%(my_rank,proc_name)

                del chr_idxs
                del poses
                del edits 
                del reads_block

                gc.enable()

                #cleanup
                os.unlink(fn_fifo_reads)
                os.unlink(fn_fifo_output)
                os.rmdir(tempd)
                print "RUNNER rank: %d finished in  %f seconds"%(my_rank,time.time()-t)
                ##SEND TO WRANGLER
                read_proc.join()
                map_proc.join() ###MAKE SURE THESE ARE DONE!
                icomm_to_READER.send({"rank":my_rank,"proc_name":proc_name},dest=0,tag=TAG_RUNNER_READY)
                
            elif status.tag == TAG_DIE:
                break

    print "RUNNER rank: %d, CPU: %s, finished, cleaning up, dying"%(my_rank,proc_name)
    comm.Barrier()
    #if my_rank==0:

    #    print "RUNNER rank 0 about to unblish!"
    #    MPI.Unpublish_name('RUNNER',runner_info,RUNNER_port)
    #    print "RUNNER rank 0 unpublished, about to close!"
    #    MPI.Close_port(RUNNER_port)
    #    print "RUNNER rank 0  closed!"
        
    exit(0)

def WRANGLER(comm,my_rank,n_procs,proc_name,contigs,outdir,chop_chr):
    RUNNER_port = None
    if my_rank==0:
        while(1):
            sleep(1)
            try:    
                print "WRANGLER is trying to find a port... (%d - %s)"%(my_rank,proc_name)
                RUNNER_port = MPI.Lookup_name("RUNNER")
                break
            except Exception:
                pass
        print "WRANGLER got port %s (%d - %s)"%(RUNNER_port,my_rank,proc_name)
    else:
        RUNNER_port = None
    
    root=0
    runner_info = MPI.INFO_NULL
    print "WRANGLER waiting to connect to RUNNER... (%d - %s)"%(my_rank,proc_name)
    icomm_to_RUNNER = comm.Connect(RUNNER_port, runner_info, 0)
    #RUNNER_comm = icomm_to_RUNNER.Get_remote_group()
    print "WRANGLER  connected to RUNNER... (%d - %s)"%(my_rank,proc_name)
    

    READER_port = None
    if my_rank==0:
        while(1):
            sleep(1)
            try:    
                print "WRANGLER is trying to find a port...to the reader (%d - %s)"%(my_rank,proc_name)
                READER_port = MPI.Lookup_name("WRANGLER_from_READER")
                break
            except Exception:
                pass
        print "WRANGLER got port %s (%d - %s)"%(READER_port,my_rank,proc_name)
    else:
        RUNNER_port = None
    
    wrangler_info = MPI.INFO_NULL
    print "WRANGLER waiting to connect to READER... (%d - %s)"%(my_rank,proc_name)
    icomm_to_READER = comm.Connect(READER_port, wrangler_info, 0)
    #RUNNER_comm = icomm_to_RUNNER.Get_remote_group()
    print "WRANGLER  connected to READER... (%d - %s)"%(my_rank,proc_name)


    wssd_by_chr = {}    
    chr_by_idx = {}    
    chr_idx = 0    
    l_by_chr = {}
    for ln in open(contigs):
        chr,l  = ln.rstrip().split()
        print "WRANGLER (%d - %s) setting up %s..."%(my_rank,proc_name,chr)
        if chop_chr: chr = chr.replace("chr","")
        l = int(l)
        a = np.zeros((l,3),dtype=np.uint16)    
        wssd_by_chr[chr] = a
        l_by_chr[chr] = l
        chr_by_idx[chr_idx] = chr
        chr_idx +=1
        print chr, chr_idx
    

    while(1):
        ##NOW THE WRANGLER HAS COMMs to the RUNNER  
        sleep(1)
        
        msg = icomm_to_RUNNER.Iprobe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
        if msg:
            status = MPI.Status()
            data = icomm_to_RUNNER.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            if status.tag == TAG_SEND_MAPPINGS:    
                rank = status.source
                print "WRANGLER %s: rank %d ready to rcv %d items from %d"%(proc_name,my_rank,data,status.source)
                n_elems = data
                chr_idxs = np.empty(n_elems,dtype = np.uint8)
                poses = np.empty(n_elems,dtype = np.uint32)
                edits = np.empty(n_elems,dtype = np.uint8)

                print "WRANGLER rank: %d  %s starting TRANSFER with %d"%(my_rank,proc_name,status.source)
                t=time.time()
                icomm_to_RUNNER.Recv([chr_idxs,MPI.UNSIGNED_CHAR],source=status.source,tag=TAG_TRANSFER)
                icomm_to_RUNNER.Recv([poses,MPI.UNSIGNED],source=status.source,tag=TAG_TRANSFER)
                icomm_to_RUNNER.Recv([edits,MPI.UNSIGNED_CHAR],source=status.source,tag=TAG_TRANSFER)
                print "WRANGLER rank: %d  %s done TRANSFER  with %d in %fs "%(my_rank,proc_name,status.source,time.time()-t)
                
                t=time.time()
                for idx,chr in chr_by_idx.iteritems():
                    w = np.where(chr_idxs==idx)
                    #print idx, chr, wssd_by_chr[chr].shape, np.amax(poses[w])
                    add_positions_to_vect(wssd_by_chr[chr],poses[w],edits[w])
                    #wssd_by_chr[chr][poses[w],edits[w]]+=1
                del chr_idxs
                del poses
                del edits 
                print "WRANGLER rank: %d  %s done writing to array in %fs "%(my_rank,proc_name,time.time()-t)

        reader_msg = icomm_to_READER.Iprobe(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG)
        if reader_msg:
            status = MPI.Status()
            data = icomm_to_READER.recv(source=MPI.ANY_SOURCE,tag=MPI.ANY_TAG,status=status)
            if status.tag == TAG_FINISH:    
                print "WRANGLER rank: %d  %s finishing up"%(my_rank,proc_name)
                break
    
    fnWssd = "%s/wssd_out_file"%(outdir)
    wssd = WssdFile( contigs,
                                     fnWssd,
                                     overwrite = True,
                                     openMode = 'w',
                                     compression = True,
                                     datatype=tables.UInt32Atom())
    wssd.addTrackSet('wssd')    
    
    width=36
    for idx,chr in chr_by_idx.iteritems():
        print "WRANGLER rank: %d  %s outputting %s..."%(my_rank,proc_name,chr)
        for ed in xrange(3):
            #wssd.depth['wssd'][chr][:,1,ed] = wssd_by_chr[chr][:,1,ed] 
            wssd.depth['wssd'][chr][:,ed,1] = wssd_by_chr[chr][:,ed] 
            #poses = np.where(wssd_by_chr[chr][:,ed] !=0)[0]
            #    dummy[pos:(pos+width)] += wssd_by_chr[chr][pos,ed] 
            dummy = np.copy(wssd_by_chr[chr][:,ed])
            for j in xrange(1,width):
                dummy[j:] += wssd_by_chr[chr][:-j,ed] 
            wssd.depth['wssd'][chr][:,ed,0] = dummy
            del dummy
            
    icomm_to_READER.send(None,dest=0,tag=TAG_DONE_JOB)
    print "WRANGLER rank: %d  %s finished"%(my_rank,proc_name)
    exit(0)

if __name__=="__main__":

    opts = OptionParser()
    opts.add_option('','--task',dest='task',default=None)
    opts.add_option('','--chr',dest='chr',default=None)
    opts.add_option('','--src_type',dest='src_type',default="BAM")
    opts.add_option('','--input',dest='input',default=None)
    opts.add_option('','--work_dir',dest='work_dir',default='/var/tmp/')
    opts.add_option('','--index',dest='index',default=None)
    opts.add_option('','--mrsfast_binary',dest='mrsfast_binary',default=None)
    opts.add_option('','--mrsfast_opts',dest='mrsfast_opts',default=None)
    opts.add_option('','--contigs',dest='contigs',default=None)
    opts.add_option('','--outdir',dest='outdir',default=None)

    #opts.add_option('','--source',dest='source',default=None)
    #opts.add_option('','--dest',dest='dest',default=None)
    #opts.add_option('','--pre_sync_commands',dest='pre_sync_commands',default=None)
    #opts.add_option('','--post_sync_commands',dest='post_sync_commands',default=None)
    ###LESS STRINGENT PRIMATE OPTS = -q 15 -n 0.01

    (o, args) = opts.parse_args()
    if not o.task:
        print stderr, "NO task defined! are you a reader, runner or wrangler!"
        exit(1)
    
    chop_chr=False
    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    n_procs = comm.Get_size()
    proc_name = MPI.Get_processor_name()
    print  "rank %d has started on proc %s"%(my_rank,proc_name)    
        
    if o.task.upper()=="READER":
        print "I AM A READER (%d - %s)"%(my_rank,proc_name)
        READER(comm,my_rank,n_procs,proc_name,o.input,chr=o.chr)
    
    if o.task.upper()=="RUNNER":
        print "I AM A RUNNER (%d - %s)"%(my_rank,proc_name)
        RUNNER(comm,my_rank,n_procs,proc_name,o.work_dir,o.index,o.mrsfast_binary,o.mrsfast_opts,o.contigs,chop_chr)
    
    if o.task.upper()=="WRANGLER":
        print "I AM A WRANGLER (%d - %s)"%(my_rank,proc_name)
        WRANGLER(comm,my_rank,n_procs,proc_name,o.contigs,o.outdir,chop_chr)

    exit(0)



    if myrank==0:
        host_loop(comm,myrank,proc_name,n_procs)
    else:
        client_loop(comm,myrank,proc_name,n_procs,o.source,o.dest,o.pre_sync_commands,o.post_sync_commands)
