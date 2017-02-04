from tornado import websocket, web, ioloop
import json
import time
import os
import smbus
import pymongo
from pymongo import MongoClient

cl = []
bus = smbus.SMBus(1)
address = 0x04

client = MongoClient('localhost', 27017)
db = client['420bits']
data_log = db.data_log

def StringToBytes(val):
  retVal = []
  for c in val:
    retVal.append(ord(c))
  return retVal

def readBus():
  data = ""
  for i in range(0, 1):
          data += chr(bus.read_byte(address));
  print data

def notify_all_clients(data):
    for c in cl:
        c.write_message(data)

class SocketHandler(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

    def on_message(self, message):
        print "Received messaged: " + message

        if message == "read":
            print "just read"
        else:
            try:
                receivedObject = json.loads(message)

                if receivedObject.has_key("turn_on"):
                    deviceToTurnOn = receivedObject["turn_on"]
                    message = deviceToTurnOn + "1"
                    bus.write_i2c_block_data(address, 0, StringToBytes(message))
                    print message

                elif receivedObject.has_key("turn_off"):
                    deviceToTurnOff = receivedObject["turn_off"]
                    message = deviceToTurnOff + "0"
                    bus.write_i2c_block_data(address, 0, StringToBytes(message))
                    print message

            except:
                print("error parsing message:" + str(message))


class TimerHandler(web.RequestHandler):

    @web.asynchronous
    def post(self):
        pass

    @web.asynchronous
    def get(self, *args):
        self.finish()
        print "Received get request"

app = web.Application([
    (r'/ws', SocketHandler),
    (r'/timer', TimerHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
