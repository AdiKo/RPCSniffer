
from cal.cal_types import ProtocolBase, FieldItem, PyFunctionItem, Subtree, TextItem
from cal.ws_consts import *

SIZE_OF_GUID_STR = 38

REQ_SYNC 	= 0x0
REQ_ASYNC	= 0x1
RESPONSE_ASYNC  = 0x2
RESPONSE_SYNC   = 0x3

MSG_TYPES = {	REQ_SYNC: "Request (SYNC)",
		REQ_ASYNC:"Request (ASYNC)",
		RESPONSE_ASYNC: "Response From Server (ASYNC)",
		RESPONSE_SYNC: "Response From Server (SYNC)"}

class Protocol(ProtocolBase):
	def parse_raw_data(self, packet):
		self.set_next_dissector("DATA")

	def __init__(self):
		self._name = "LOCAL RPC PROTOCOL"
		self._filter_name = "localrpc"
#		self.set_next_dissector("dcerpc_winreg")
		self._short_name = "localrpc"
		self._items = [
			
			FieldItem("pid", FT_UINT32, "Process ID", display = BASE_HEX),
			FieldItem("tid", FT_UINT32, "Thread ID", display = BASE_HEX),
			FieldItem("reason", FT_UINT32, "Msg Reason", strings = MSG_TYPES ),
			FieldItem("procnum", FT_UINT32, "Procedure Number"),
			Subtree(
				TextItem("syntax", "Syntax"), 
				[FieldItem("guid", FT_STRING, "Guid", length = SIZE_OF_GUID_STR),
				FieldItem("rpc_major_ver", FT_UINT16, "RPC Major Version", display = BASE_HEX),
				FieldItem("rpc_minor_ver", FT_UINT16, "RPC Minor Version", display = BASE_HEX)]
				),
			Subtree(
				TextItem("interface", "Interface"),
				[FieldItem("guid", FT_STRING, "Guid", length = SIZE_OF_GUID_STR),
				FieldItem("dispatch_tbl_ptr", FT_UINT64, "Dispatch Table pointer", display = BASE_HEX),
				FieldItem("dispatch_tbl_size", FT_UINT32, "Dispatch Table size", display = BASE_HEX),
				FieldItem("dispatch_tbl_func_addr", FT_UINT64, "Dispatch Table Func Address", display = BASE_HEX),
				
				Subtree(
					TextItem("midl", "Midl"),
					[FieldItem("dispatch_ptr", FT_UINT64, "Dispatch Pointer", display = BASE_HEX),
					FieldItem("server_func_addr", FT_UINT64, "Server Function Address", display = BASE_HEX)]
					),
				]
				),
	
			FieldItem("rpc_flags", FT_UINT32, "RPC FLAGS", display = BASE_HEX),

			FieldItem("buffer.len", FT_UINT32, "Buffer Length", display = BASE_HEX),
#			PyFunctionItem(self.parse_raw_data, {}),
			]
		#self._register_under = { "udp.port": 0x2} 
		self._register_under = { "ethertype": 0x0806}




