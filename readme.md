# Network Relays Control #

A project to use with Lava CI. Based on //Lavamini//, this adaptation was made to use any board to control
relays during Lava test jobs.

## Why this ##

To use the client with the distant daemon I've thought it would be nice to have it
open to any board. In that sense, it's the client's job to manage the IOs, ie:  init., setting pins on and off, etc.

## Usage ##

Therefore, pin address and commands are sent through rpc from the client side, that way:

1) start the daemon by telling which board you intend to use (BBB and PI are provided as examples)

     ./ci-daemon.py -b BBB
     
2) Client side : sending a command

   From this point you have 2 options :

   ### Detailed mode ####

   python3 ci-client.py -s 192.168.1.2 on -p P8_45

   which does all the job. The same applies for initialization so at the end it's only matter of setting pins on and off.

   ### Guided mode ###

   In this mode, the client relies on a config file that keeps all the internal details, like :
      - board ip : where you give only the name so the ip will be deduced automatically
      - relays pin mapping is read from the server side : simplifies the way to address relays, instead of having the pin address for a dedicated board you just ask for relay.

   This configfile is the ini format.

   Thus, with the previous example we can send a "on" command like this :

   python3 ci-client.py -u bbb1 -p relay1 on



## Requirements ##
This project is using the Adafruit GPIO libs which you need to have before running.
The installation is well documented but it's just a matter of either :

For Raspberry:
    pip3 install RPi.GPIO

or

For BeagleBone Black:
    pip3 install Adafruit_BBIO

 :warning: No lib seems to work for OrangePI 

## Boards ##
### BeagleBone Black ###

According to the official cape expansion headers, the BBB fred the HDMI pins by usig dedicated overlay

![alt text](https://raw.githubusercontent.com/dlewin/NRC/master/Docs/NRC_BBB.png)
  
