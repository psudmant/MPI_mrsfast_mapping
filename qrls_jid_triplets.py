from optparse import OptionParser

if __name__=="__main__":
	
	opts = OptionParser()
	opts.add_option('','-n',default='7',type=int)
	opts.add_option('','--fn_triplets')
	(o,opt) = opts.parse_args()

	last_runners = [-1 for i in xrange(o.n)]

	for l in open(o.fn_triplets):
		read,run,wran = l.rstrip().split()
		last_runner=last_runners.pop(0)
		if last_runner==-1:
			print "qrls %s,%s,%s"%(read,run,wran)
		else:
			print "qalter -hold_jid %s %s"%(last_runner, read)	
			print "qalter -hold_jid %s %s"%(last_runner, run)	
			print "qalter -hold_jid %s %s"%(last_runner, wran)	
			print "qrls %s,%s,%s"%(read,run,wran)
		last_runners.append(run)


