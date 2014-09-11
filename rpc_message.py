import struct, binascii
from rpc_structs import *
from ctypes import *
from utils import *
from params import *


class RpcMessage:
	def __init__(self, event, reason, pid, tid, rpc_message):
		process = event.get_process()

		self.pid = pid
		self.tid = tid
		self.reason = reason

		self.rpc_struct = process.read_structure(rpc_message, RPCMem)
		
		self.buff = ""
		if self.rpc_struct.BufferLength > 0:
			self.buff = process.read(self.rpc_struct.Buffer , self.rpc_struct.BufferLength)

		self.transfer_syntax = process.read_structure(self.rpc_struct.TransferSyntax, TransferMem)

		self.inf_data = InterfaceInfo(process, self.rpc_struct.RpcInterfaceInformation, self.rpc_struct.ProcNum)


	def serialize(self):
		msg = struct.pack(">I", self.pid)
		msg += struct.pack(">I", self.tid)
		msg += struct.pack(">I", self.reason)

		transfer_serialized = self.transfer_syntax.serialize()
		inf_serialized = self.inf_data.serialize(self.rpc_struct.ProcNum)

		msg += self.rpc_struct.serialize(inf_serialized, transfer_serialized, self.buff)

		return msg

class InterfaceInfo:
	def __init__(self, process, inf_data, procnum):
		self.process = process

		self.inf_struct = process.read_structure(inf_data, InterfaceInfoMem)
		
		self.dispatch = process.read_structure(self.inf_struct.DispatchTable, DispatchTableMem)

		self.midl = process.read_structure(self.inf_struct.InterpreterInfo, MidlInfoMem)

	def serialize(self, procnum):
		msg = self.inf_struct.serialize()

		ptr_size = self.process.get_bits() / 8

		msg += self.dispatch.serialize(procnum, ptr_size)
		msg += self.midl.serialize(procnum, ptr_size)

		return msg

