#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Python RPC Daemon
'''
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--boardtype", help="Specify which board the daemon will run on")
parser.add_argument("args", nargs='?', help="CONTROLLER Command Arguments")
args = parser.parse_args()

if args.boardtype =="BBB":
    import Adafruit_BBIO.GPIO as GPIO
    BOARD="BBB"
elif args.boardtype == "PI":
    import Adafruit_PI.GPIO as GPIO
    BOARD="PI"
else:
    print("Board not supported yet: currently availalbe boards are BBB or PI")
    sys.exit() 

VERSION = "1.0"

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/ci',)

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 6789), requestHandler=RequestHandler)
server.register_introspection_functions()

def boardtype():
    return BOARD
server.register_function(boardtype)

def version():
    return VERSION
server.register_function(version)

def on(pin_address):
    print(type(pin_address))
    GPIO.setup( (pin_address) , GPIO.OUT)
    return ("on sent for ", (pin_address))

server.register_function(on)

def off(pin_address):
    GPIO.setup(pin_address,GPIO.IN)
    return ("off sent for ", pin_address)

server.register_function(off)

print ("Starting with : ", BOARD)
# Run the server's main loop
server.serve_forever()
