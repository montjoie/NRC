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

VERSION = "1.3"


import RPi.GPIO as GPIO
# For BeagleBone Black, replace previous line by : import Adafruit_BBIO.GPIO as GPIO    

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
        boardtype == "PI"                                                               # default is PI
        print ("boardtype: ", boardtype)     
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
    
#Look for board definition within a section
def check_board(parser, map_section):
    if not parser.has_option(map_section, "boardtype"):
        return False
    else:
        return True

# Look for config file, if not: CLI calls are required
def check_conffile(configfile, mapping):
#        global mapping 
    if not os.path.isfile(configfile):                #check that config file exists
         print("config file not found: ", configfile ) 
         os._exit(1)
    
    boardtype, pinaddr = read_config(configfile, mapping)
        
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

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/ci',)

def version():
    return VERSION

def on(relayname):
    boardtype, pin_address = read_config(configfile, mapfile,relayname)       
    if boardtype == "PI":
        GPIO.setup( int(pin_address) , GPIO.OUT)
        GPIO.setup( int(pin_address) , False)
    else:
        GPIO.setup( pin_address , GPIO.OUT)

    return ("on sent for ", (pin_address))

def off(relayname):
    boardtype, pin_address = read_config(configfile, mapfile,relayname)       
    if boardtype == "PI":
        GPIO.setup( int(pin_address) , GPIO.OUT)
        GPIO.setup( int(pin_address) , True)
    else:
        GPIO.setup(pin_address,GPIO.IN)

    return ("off sent for ", pin_address)


if __name__ == '__main__':

    # Create server
    server = SimpleXMLRPCServer(("0.0.0.0", 6789), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_function(on)
    server.register_function(off)
    server.register_function(version)

    #required only for PI -------------------------
    GPIO.setmode(GPIO.BCM)
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("mapping", help="which relay mapping is required. To use with a configfile")
    parser.add_argument("args", nargs='?', help="CONTROLLER Command Arguments")
    parser.add_argument("-c", "--configfile", help="Guided mode : use a configfile")
    
    args = parser.parse_args()
    mapfile = args.mapping
    
    if args.configfile:
        configfile = args.configfile
    else:
        configfile = "nrc.cfg"
    
    check_conffile(configfile, mapfile)
    
    try:   
         print ('Server is now running, press Ctrl-C to quit.')
       # Run the server's main loop
         server.serve_forever()
    finally:
         GPIO.cleanup()
