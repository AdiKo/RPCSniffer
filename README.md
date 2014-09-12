
RPCSniffer
==========
RPCSniffer sniffs RPC messages in a given RPC server process.

![sniffing example in spoolsv process](https://github.com/AdiKo/RPCSniffer/blob/master/sample_screenshot.png)

General Information
-------------------
With RPCSniffer you can explore RPC Messages that present on Microsoft system.
    The data given for each RPC message contains the following details:
* Type (Async/Sync , Request/Response)
* Process number
* Thread number
* Procedure number
* Transfer Info
    * GUID
	* RPC minor version
	* RPC major version
* Interface Info
	* GUID
	* Dispatch table pointer
	* Dispatch table size
	* Dispatch table function pointer
* Midl Info
    * Dispatch pointer
    * Server function address
* RPC Flags
* RPC Data


## Install steps

1. Install [python 2.7](https://www.python.org/download/releases/2.7/) (64 bit)

2. Install the latest [Winappdbg](http://winappdbg.sourceforge.net/) python package

3. Install [Wireshark](https://www.wireshark.org/download.html)

4. Intsall the latest [Pyreshark](https://github.com/ashdnazg/pyreshark) python module for wireshark

5. grab the file _"pyreshark_rpc_dissector/rpc_protocol.py"_ to _"c:\Program Files\Wireshark\python\protocols\"_

## Run

1. Start Wireshark from cmd and prepare it to use rpcsniffer's pipe

```
	"C:\Program Files\Wireshark\Wireshark.exe" -i \\.\pipe\RPCSniffer
```

2. Run python main.py with the server process to listen
    
```
    python main.py --help
    usage: main.py [-h] (-p PID | -n PROCNAME)
    main.py: error: one of the arguments -p/--pid -n/--procname is required
 ```
    
3. go back to wireshark and click "start"
4. from now you'll get all rpc messages in wireshark

## Implementation

Check the wiki for more info.


## TODO

	
This project is a POC for now, but you can help me add some stunning features that will allow us to really understand RPC internals. 
- Dissect the rpc raw data (maybe by using the RPCView decompiler and find a MIDL-dissector?)
- Integrate it with the wireshark midl-dissector itself
- Retreive more data from the rpc message (I used [REACTOS](https://www.reactos.org/) to parse the RPC MESSAGE). Can you find more usefull data from this windows struct?
- ALPC sniffing
- Record all RPC messages for fun and fuzzing

Anyway, I'd be more than happy to receive bug reports, suggestions and anything else.


## Some Comments

- It's very usefull to use the powerful and free tool called RPCView for finding interesting RPC server processes, decompile its interfaces and more. Take a look at
	http://rpcview.org/index.html




