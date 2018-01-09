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

VERSION = "1.2"

import Adafruit_BBIO.GPIO as GPIO    

def read_config(conf_file, mapping_section,relayname=""):
    conf_parser = SafeConfigParser()
    conf_parser.read(conf_file)
    boardtype = "NONE"
    pinaddr = "NONE"

    if check_section(conf_parser,mapping_section):                                      # Check if the requested mapping exists in the cfg file
        if check_board(conf_parser, mapping_section):                                   # Look for the board type in section
            boardtype = conf_parser.get(mapping_section,"boardtype")
            if relayname and  check_option(conf_parser,mapping_section,relayname):                     # Check if the requested relay exists in the cfg file
                pinaddr = conf_parser.get(mapping_section, relayname)
        else:
            print ("boardtype definition not found in ", mapping_section)
    return(boardtype, pinaddr)    

#clumzy
def import_boardtype(boardtype):
    if boardtype == "BBB":
        import Adafruit_BBIO.GPIO as GPIO    
    else:                                    
        print ("boardtype: ", boardtype)     
        import Adafruit_PI.GPIO as GPIO      
    
#Look for board definition within a section
def check_board(parser, map_section):
    if not parser.has_option(map_section, "boardtype"):
        return False
    else:
        return True

# Look for config file, if not: CLI calls are required
def check_conffile():
    if not os.path.isfile(args.configfile):                #check that config file exists
        print("configfile not found", args.configfile) 
    else:
        global configfile
        configfile = args.configfile
        global mapping 
        mapping = args.mapping
        # relayname = args.relayname
#        relayname="relay1"                                  #DEBUG
        print("Using config file : ", configfile)
        boardtype, pinaddr = read_config(configfile, mapping)       
#        import_boardtype(boardtype)
        
def check_section(parser, section):
    if not parser.has_section(section):
        print(section, "section not found in config file")
        return False
    else :
        return True

def check_option(parser,section, option):
    if not parser.has_option(section,option):
        print(option, "option not found in config file from ", section)
        return False
    else :
        return True

parser = argparse.ArgumentParser()

parser.add_argument("mapping", help="which relay mapping is required. To use with a configfile")
parser.add_argument("args", nargs='?', help="CONTROLLER Command Arguments")
parser.add_argument("-c", "--configfile", help="Guided mode : use a configfile",default="nrc.cfg")

args = parser.parse_args()
        
if args.configfile:
    check_conffile()
else: 
    print("no specific config file provided, using default")

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/ci',)

# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 6789), requestHandler=RequestHandler)
server.register_introspection_functions()

def version():
    return VERSION
server.register_function(version)

def on(relayname):
    boardtype, pin_address = read_config(configfile, mapping,relayname)       
    GPIO.setup( (pin_address) , GPIO.OUT)
    return ("on sent for ", (pin_address))

server.register_function(on)

def off(relayname):
    boardtype, pin_address = read_config(configfile, mapping,relayname)       
    GPIO.setup(pin_address,GPIO.IN)
    return ("off sent for ", pin_address)

server.register_function(off)

# Run the server's main loop
server.serve_forever()
