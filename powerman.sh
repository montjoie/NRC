#!/bin/bash

if [ "$#" -ne 2 ]
 then
    echo "Wrong parameters : $#"
else
    while [ -n "$1" ]
    do
        case "$1" in
            -off) relay="$2" 
            COMMAND="off"
            shift ;;
            -on) relay="$2" 
            COMMAND="on"
            shift ;;
            -reset) relay="$2" 
            COMMAND="reset"
            shift ;;
            *) echo "Option $1 not recognized";;
        esac
        shift
    done

    cd /usr/local/bin/
    ls -l 
    python3 ci-client.py $COMMAND -c nrc.cfg -u bbb1 -r $relay 
fi

