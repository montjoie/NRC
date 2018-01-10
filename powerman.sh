#!/bin/bash


reset_board()
{
    print "python3 ci-client.py off -c nrc.cfg -u bbb1 -r $1"
    sleep 5
    print "python3 ci-client.py on -c nrc.cfg -u bbb1 -r $1"
}


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
ls   

if [ $COMMAND = "reset" ]
then
    reset_board $relay
else
    python3 ci-client.py $COMMAND -c nrc.cfg -u bbb1 -r $relay
fi

