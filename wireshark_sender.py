import win32pipe, win32file, struct, time, logging
from params import ARP_PKT, INITIAL_PCAP_HEADER, WIRESHARK_PIPE

class WiresharkSender:
	def __init__(self):
		self.pipe_h = win32pipe.CreateNamedPipe(
			WIRESHARK_PIPE,
			win32pipe.PIPE_ACCESS_OUTBOUND,
			win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
			1, 65536, 65536,
			300,
			None)

		logging.info("Waiting for wireshark to connect to pipe '%(WIRESHARK_PIPE)s'" % globals()) 

		win32pipe.ConnectNamedPipe(self.pipe_h, None)
		win32file.WriteFile(self.pipe_h, INITIAL_PCAP_HEADER)


	def send_rpc_packet_to_wireshark(self, data):
		packet = ARP_PKT + data

		curr_sec = struct.pack("<L", time.time())
		micro_sec = struct.pack("<L", 0)
		pcap_header = curr_sec + micro_sec + 2 * struct.pack("<L",len(packet))
		
		#logging.debug("About to send rpc msg to wireshark")
		win32file.WriteFile(self.pipe_h, pcap_header + packet)
