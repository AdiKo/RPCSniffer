from params import *
from winappdbg import *
from rpc_message import RpcMessage
from wireshark_sender import WiresharkSender

g_wireshark = None

REQ_SYNC 	= 0x0
REQ_ASYNC	= 0x1
RESPONSE_ASYNC  = 0x2
RESPONSE_SYNC   = 0x3

class RPCEventHandler( EventHandler ):

	def __init__(self):
		super(RPCEventHandler, self).__init__()

		global g_wireshark
		g_wireshark = WiresharkSender()


	def load_dll( self, event ):
		module = event.get_module()
		if module.match_name(rpc_dll):

			pid = event.get_pid()
			
			event.debug.hook_function( pid, request_sync_func, RPCEventHandler.bp_req_sync, RPCEventHandler.bp_respone_sync)
			event.debug.hook_function( pid, request_sync_func_2, RPCEventHandler.bp_req_sync, RPCEventHandler.bp_respone_sync)

			RPCEventHandler.add_bp_on_func(pid, event, request_async_func, RPCEventHandler.bp_req_async)

			RPCEventHandler.add_bp_on_func(pid, event, response_async_func, RPCEventHandler.bp_response_async)
			

	@staticmethod
	def add_bp_on_func(pid, event, func_name, cb):
		module = event.get_module()
		address = module.resolve( func_name) 
		event.debug.break_at( pid, address, cb)

	@staticmethod
	def bp_response_async( event ):
		thread  = event.get_thread()
		rpc_message = thread.get_register("Rcx")
		RPCEventHandler.handle_rpc_message(event, RESPONSE_ASYNC, rpc_message)

	@staticmethod
	def bp_req_async( event ):
		thread  = event.get_thread()
		rpc_message = thread.get_register("Rcx")
		RPCEventHandler.handle_rpc_message(event, REQ_ASYNC, rpc_message)

	@staticmethod
	def bp_req_sync( event, ra ):
		thread  = event.get_thread()
		rpc_message = thread.get_register("Rcx")
		RPCEventHandler.handle_rpc_message(event, REQ_SYNC, rpc_message)
	
	@staticmethod
	def bp_respone_sync( event, ra ):
		thread  = event.get_thread()
		rpc_message = thread.get_register("Rdi")
		RPCEventHandler.handle_rpc_message(event, RESPONSE_SYNC, rpc_message)

	@staticmethod
	def handle_rpc_message(event, reason, rpc_message):
		pid = event.get_pid()
		tid = event.get_tid()
		
		msg = RpcMessage(event, reason, pid, tid, rpc_message)
		serialized = msg.serialize()	
		g_wireshark.send_rpc_packet_to_wireshark(serialized)

