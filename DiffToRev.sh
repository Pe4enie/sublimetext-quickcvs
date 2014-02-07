#!/bin/sh

if [ ! -d $3 ]
then
	mkdir -p $3
fi

touch $3/$(basename $2)
cd $(dirname $2)
cvs update -C -r $1 -p $(basename $2) > "$3/$(basename $2)"
opendiff "$(basename $2)" "$3/$(basename $2)"
