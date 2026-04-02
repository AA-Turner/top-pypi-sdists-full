#!/bin/bash
##
## Copyright (c) 2009-2022 CERN. All rights nots expressly granted are
## reserved.
##
## This file is part of iLCDirac
## (see ilcdirac.cern.ch, contact: ilcdirac-support@cern.ch).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## In applying this licence, CERN does not waive the privileges and
## immunities granted to it by virtue of its status as an
## Intergovernmental Organization or submit itself to any jurisdiction.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##


### 
# This program will create a tar ball suitable for running the program on the grid with ILCDIRAC
# Needs the chrpath and readelf utilities
###

if [ $# -eq 0 ]; then
    echo " Please state the name of the Program! " 
    exit 1
fi

programname=$1
programpath=$(which ${programname})
echo "Getting libraries for $programpath"

TARBALLNAME=lib.tar.gz
LIBFOLDER=lib
mkdir -p $LIBFOLDER

if [ $(which ${programname}&>/dev/null) $? -eq 0 ]; then
    
    rsync -avzL $programpath $LIBFOLDER/
    string1=$(ldd $programpath | grep "=>" | sed 's/.*=>//g' | sed "s/(.*)//g")
    string=""
    for file in $string1; do
	string="$file $string"
    done
    rsync -avzL $string $LIBFOLDER
    echo -e "Creating Tarball, this might take some time"

    # for file in $( ls --color=never $LIBFOLDER/* ); do
    # 	chrpath -d $file
    # 	readelf -d $file | grep RPATH
    # 	if [ $? == 0 ]; then
    # 	    echo "FOUND RPATH Aborting!!"
    # 	    exit 1
    # 	fi
    # done

    for file in libc.so* libc-2.5.so* libm.so* libpthread.so* libdl.so* libstdc++.so* libgcc_s.so.1*; do
	rm $LIBFOLDER/$file 2> /dev/null
    done

    tar zcf $TARBALLNAME $LIBFOLDER/*
    exit 0
else
    echo -e "$programname not found, environment not set, Aborting!"
    exit 1
fi
