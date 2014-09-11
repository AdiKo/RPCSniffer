import struct, binascii, os, pdb
from winappdbg import System

def get_pid_by_name(name):
	system = System()
	for process in system:
		exe_path = process.get_image_name()
		if exe_path == None:
			continue

		procname = os.path.basename(exe_path)
		if procname == name:
			return process.get_pid()

	raise Exception("No Process named %(name)s is found" % locals())

def reverse(data):
	return data[6:8] + data[4:6] + data[2:4] + data[0:2]

def get_guid(data):
	data = binascii.hexlify(data)
	guid = "{"
	guid += reverse(data[0:8])+ "-"
	guid += reverse(data[8:12])+ "-"
	guid += reverse(data[12:16])+ "-"
	guid += (data[16:20])+ "-"
	guid += (data[20:32])+ "}"
	return guid

