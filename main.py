import sys, pdb, argparse, logging
from winappdbg import Debug
from params import *
import event_handler
import utils

def set_logger():
	logger = logging.getLogger()
	handler = logging.FileHandler(LOG_FNAME)
	stdout_handler = logging.StreamHandler()

	formatter = logging.Formatter(LOG_FMT)
	handler.setFormatter(formatter)
	stdout_handler.setFormatter(formatter)

	logger.addHandler(handler) 
	logger.addHandler(stdout_handler)

	logger.setLevel(logging.DEBUG)
		

def parse_args():
	parser = argparse.ArgumentParser(description='RPCSniffer Program')

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-p','--pid', help='Pid of server process to sniff', type = int)
	group.add_argument('-n','--procname', help='Name of server process to sniff', type = str)

	args = vars(parser.parse_args())
	return args;


def get_pid(args):
	if args['procname'] != None:
		return utils.get_pid_by_name(args['procname'])

	return args['pid']


def main( ):
	
	set_logger()

	args = parse_args()	
	pid = get_pid(args)

	logging.debug( "about to connect to pid %(pid)s" % locals() )

	dbg = None
	try:

		dbg = Debug( event_handler.RPCEventHandler(), bKillOnExit = False)
		dbg.attach(pid)
		dbg.loop()

	finally:
		if dbg != None:
			logging.debug ("About to detach from pid %(pid)s" % locals() )
			dbg.detach(pid)
		
		logging.info("Finished")

if __name__ == "__main__":
	main()
