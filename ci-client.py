#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Python Network Client
'''
import xmlrpc.client
import argparse
import time
from configparser import SafeConfigParser
import os.path

CONTROLLER_RPC_PORT = 6789

def read_config(conf_file,board_name, mapping_section,relayname):
    boards_section = "BOARDS"
    board_ip = "NONE"
    config = SafeConfigParser()
    config.read(conf_file)
    if check_section(config,boards_section):                    # Check if the board <section> exists in the cfg file
       if check_option(config,boards_section, board_name):                    # Check if the requested board <name> exists in the cfg file
            board_ip = config.get(boards_section,board_name)
    return(board_ip)

def check_section(parser, section):
    if not parser.has_section(section):
        print(section, "section not found in config file")
        return False
    else :
        return True

def check_option(parser,section, option):
    print ("APPEL DE check_option: ",section, " et ", option) 
    if not parser.has_option(section,option):
        print(option, "option not found in config file")
        return False
    else :
        return True

#args without '-' is mandatory
parser = argparse.ArgumentParser()

parser.add_argument("-c", "--configfile", help="Guided mode : use a configfile")
parser.add_argument("-m", "--mapping", help="which relay mapping is required. To use with a configfile")
parser.add_argument("-r", "--relayname", help="Guided mode : specify which relay will be used with the command instead of pinaddress. Usable only when using a config file")
parser.add_argument("-u", "--useboard", help="Guided mode : specify the board name to use. Required when using config file")
parser.add_argument("-s", "--server", help="Detailed mode : specify CONTROLLER Hostname.")
parser.add_argument("-p", "--pinaddress", help="Detailed mode : specify which pin to use")
parser.add_argument("command", help="CONTROLLER Command, use 'help' to get all commands")
parser.add_argument("-b", "--boardtype", help="request the board type")
parser.add_argument("-v", "--version", help="request the version number")
parser.add_argument("args", nargs='?', help="CONTROLLER Command Arguments")
args = parser.parse_args()

# if server address is provided from CLI
if args.server:
    serveraddr = "%s:%d" % (args.server, CONTROLLER_RPC_PORT)
    s = xmlrpc.client.ServerProxy("http://%s/ci" % serveraddr)

# Look for config file, if not: CLI calls are required
if args.configfile:
    if not os.path.isfile(args.configfile):                #check that config file exists
        print("configfile not found", args.configfile) 
    else:
        configfile = args.configfile
else:
        configfile = "nrc.cfg" 
        
board = args.useboard
mapping = args.mapping
relayname = args.relayname
print("Using config file : ", configfile, mapping, board, relayname)
servercfg = read_config(configfile, board,mapping,relayname)

if servercfg != "NONE":
    serveraddr = "%s:%d" % (servercfg, CONTROLLER_RPC_PORT)
    print ("connecting to : ", serveraddr)
    s = xmlrpc.client.ServerProxy("http://%s/ci" % serveraddr)

    if args.pinaddress:
        pinaddr = "%s" % (args.pinaddress)
    
    if args.boardtype:
        print(args.boardtype)
    
    if args.command == "version":
        print(s.version())
    
    if args.command == "on":
        print("Client on for:", pinaddr)
        print(s.on(pinaddr))
    
    if args.command == "off":
        print(s.off(pinaddr))
