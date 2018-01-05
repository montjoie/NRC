#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Python RPC Daemon
'''
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import subprocess
from configparser import SafeConfigParser
import argparse
import sys
import os.path

def read_config(conf_file,board_name, mapping_section,relayname):
    config = SafeConfigParser()
    config.read(conf_file)
    if check_section(mapping_section):                    # Check if the requested mapping exists in the cfg file
        mapping = config.get(boards_section,board_name)
        print( mapping )
    if check_option(config,mapping_section,relayname):                    # Check if the requested relay exists in the cfg file
        pinaddr = config.get(mapping_section, relayname)
        print ( pinaddr )
    return(mapping, pinaddr)

# Look for config file, if not: CLI calls are required
def check_conffile():
    if not os.path.isfile(args.configfile):                #check that config file exists
        print("configfile not found", args.configfile) 
    else:
        configfile = args.configfile
        board = args.useboard
        mapping = args.mapping
        relayname = args.relayname
        print("Using config file : ", configfile, mapping, board, relayname)
        servercfg,pinaddr = read_config(configfile, board,mapping,relayname)
        
        serveraddr = "%s:%d" % (servercfg, CONTROLLER_RPC_PORT)
        print ("connecting to : ", serveraddr)
        s = xmlrpc.client.ServerProxy("http://%s/ci" % serveraddr)

parser = argparse.ArgumentParser()

parser.add_argument("mapping", help="which relay mapping is required. To use with a configfile")
parser.add_argument("args", nargs='?', help="CONTROLLER Command Arguments")
parser.add_argument("-c", "--configfile", help="Guided mode : use a configfile",default="nrc.cfg")

args = parser.parse_args()

VERSION = "1.0"

if args.configfile:
    check_conffile()
else: 
    print("using default config file")

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/ci',)

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 6789), requestHandler=RequestHandler)
server.register_introspection_functions()

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

# Run the server's main loop
server.serve_forever()
