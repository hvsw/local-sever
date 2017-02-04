import websocket
import threading
import thread
import time

def on_message(ws, message):
	print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
    	ws.send("{\"register\": \"aaa\"}")
        #ws.close()
    thread.start_new_thread(run, ())

if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("ws://ec2-52-34-138-21.us-west-2.compute.amazonaws.com:8888/ws",on_message=on_message,on_error=on_error,on_close=on_close)
	#ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",on_message=on_message,on_error=on_error,on_close=on_close)
	ws.on_open = on_open

	wst = threading.Thread(target=ws.run_forever)
	wst.daemon = True
	wst.start()

	while True:
		if ws is not None and ws.sock.connected:
			if ws.sock.connected:
				ws.send("{\"from_device\": \"aaa\"}")
			print "Hello"
		else:
			print "Bye"
		time.sleep(3)