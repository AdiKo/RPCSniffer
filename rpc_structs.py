import struct
from ctypes import *
from utils import get_guid
from params import *

class TransferMem(Structure):
	pass

class DispatchTableMem(Structure):
	pass

class InterfaceInfoMem(Structure):
	pass

class RPCMem(Structure):
	_fields_ = [	("Handle", c_void_p),
			("DataRepresentation", c_void_p),
			("Buffer", c_void_p),
			("BufferLength", c_uint32),
			("ProcNum", c_uint32), 
			("TransferSyntax", POINTER(TransferMem)),
			("RpcInterfaceInformation", c_void_p), 
			("ReservedForRuntime", c_void_p), 
			("ManagerEpv", c_void_p), 
			("ImportContext", c_void_p),
			("RpcFlags", c_uint32) ]

	def serialize(self, inf_serialized, transfer_serialized, raw_data):
		msg = struct.pack(">I", self.ProcNum)
		
		msg += transfer_serialized
		msg += inf_serialized
		msg += struct.pack(">I", self.RpcFlags)
		
		msg += struct.pack(">I", self.BufferLength)
		msg += raw_data
		return msg

class TransferMem(Structure):
	_fields_ = [("guid", c_uint8 * GUID_SIZE),
		("major_ver", c_uint16),
		("minor_ver", c_uint16)]

	def serialize(self):
		msg = struct.pack("%(GUID_STR_LEN)ss" % globals(), get_guid(self.guid))
		msg += struct.pack(">H", self.major_ver)
		msg += struct.pack(">H", self.minor_ver)
		return msg

class MidlInfoMem(Structure):
	_fields_ = [	("pStubDesc", c_void_p),
			("DispatchTable", c_void_p)]

	def serialize(self, procnum, ptr_size):
		msg = struct.pack(">Q", self.DispatchTable)

		server_func = self.DispatchTable + ptr_size * procnum
		msg += struct.pack(">Q", server_func)
		
		return msg

class InterfaceInfoMem(Structure):
	_fields_ = [	("Length", c_uint32),
			("InterfaceIdGuid", c_uint8 * GUID_SIZE),
			("InterfaceIdVersion", c_uint32),
			("TransferGuid", c_uint8 * GUID_SIZE),
			("TransferVersion", c_uint32),

			("DispatchTable", POINTER(DispatchTableMem)),
			("RpcProtseqEndpointCount", c_uint16),
			("RpcProtseqEndpoint", c_void_p),
			("DefaultManagerEpv", c_uint16),
			("InterpreterInfo", POINTER(MidlInfoMem))]

	def serialize(self):
		msg = struct.pack("%(GUID_STR_LEN)ss" % globals(), get_guid(self.InterfaceIdGuid))
		return msg

class DispatchTableMem(Structure):
	_fields_ = [	("DispatchTableCount", c_uint64),
			("DispatchTable", c_void_p)]
	
	def serialize(self, procnum, ptr_size):
		msg = struct.pack(">Q", self.DispatchTable)
		msg += struct.pack(">I", self.DispatchTableCount)
		
		func_addr = self.DispatchTable + ptr_size * procnum
		msg += struct.pack(">Q", func_addr)

		return msg

