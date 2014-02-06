#!/bin/zsh

if [ ! -d $2 ]
then
	mkdir -p $2
fi

touch $2/$(basename $1)
cd $(dirname $1)
cvs update -C -p $(basename $1) > "$2/$(basename $1)"
opendiff "$(basename $1)" "$2/$(basename $1)"
