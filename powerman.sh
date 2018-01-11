#!/bin/bash


reset_board()
{
    /usr/local/bin/ci-client.py off -u bbb1 -p $1
    sleep 5
    /usr/local/bin/ci-client.py on -u bbb1 -p $1
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

cd /usr/local/bin

if [ $COMMAND = "reset" ]
then
    reset_board $relay
else
    /usr/local/bin/ci-client.py $COMMAND -u bbb1 -p $relay
fi

