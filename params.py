

LOG_FNAME = "sniffer.log"
LOG_FMT = '%(asctime)s %(levelname)s %(message)s'


rpc_dll = "rpcrt4.dll"

request_sync_func = "NdrServerCall2"
request_sync_func_2 = "NdrServerCallAll"
request_async_func = "NdrAsyncServerCall"
response_async_func = "I_RpcSend"

ARP_PKT = '\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x08\x06' 

INITIAL_PCAP_HEADER = '\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x01\x00\x00\x00'

WIRESHARK_PIPE = r'\\.\pipe\RPCSniffer'


# Sizes
GUID_SIZE 				 = 0x10
GUID_STR_LEN 				 = 0x26

# Type of hook
REQUEST_SYNC			  	 = 0x0
REQUEST_ASYNC				 = 0x1
RESPONSE_AYNC				 = 0x2




