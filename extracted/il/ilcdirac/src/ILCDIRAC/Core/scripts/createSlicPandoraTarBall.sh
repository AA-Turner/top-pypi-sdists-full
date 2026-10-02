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

programname=PandoraFrontend
LD_LIBRARY_PATH_TEMP=$LD_LIBRARY_PATH
source /afs/cern.ch/eng/clic/software/DIRAC/bashrc
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LD_LIBRARY_PATH_TEMP
platform=`dirac-architecture`

if [ $# -eq 0 ]; then
    echo "Please Specify the version of the tarball e.g. 0108 and comment e.g. \"added new processor\"" 
    exit 1
else
    version=$1
    comment=$2 
    if [ $(which $programname &>/dev/null) $? -eq 0 ]; then
	progdir=$(which ${programname})
	directoryname=SLICPandora$version
	mkdir -p $directoryname/Executable
	mkdir -p $directoryname/LDLibs 
	mkdir -p $directoryname/Settings

	rsync -avzL $progdir $directoryname/Executable/${programname}
	
	if [ -e $PANDORASETTINGS ]; then
	    echo "PANDORASETTINGS Found " 
	    rsync -avzL $PANDORASETTINGS/*.xml $directoryname/Settings/
	else
	    echo "PandoraSettings.xml not found! Aborting"
	    exit 1
	fi

    ##Dealing with the libraries for Marlin
#	ldd $progdir | grep "=>" | sed 's/.*=>/rsync -avzL /g' | sed 's/(.*)/$directoryname\/LDLibs/g'  > lddLog.sh
#	source lddLog.sh
	readelf -d $progdir | grep RPATH
	if [ $? == 0 ]; then
	    echo "FOUND RPATH Aborting!!"
	    exit 1
	fi
	string1=$(ldd $progdir | grep "=>" | sed 's/.*=>//g' | sed "s/(.*)//g")
	string=""
	for file in $string1; do
	    string="$file $string"
	done
	rsync -avzL $string $directoryname/LDLibs
	python $DIRAC/ILCDIRAC/Core/Utilities/PrepareLibs.py $directoryname/LDLibs
	echo -e "\E[034mComputing md5 checksum\E[030m"
	cd $directoryname
	find . -type f -print0 | xargs -0 md5sum > md5_checksum.md5
	cd ..

	echo -e "\E[034mCreating Tarball, this might take some time\E[030m"
	tar czf $directoryname.tgz $directoryname/*
	
	#echo -e "\E[031mCopying the file to clic/data/software"
	#cp -i $directoryname.tgz /afs/cern.ch/eng/clic/data/software/$directoryname.tgz
	echo -e "Adding to Dirac CS and copying to final location"
	dirac-proxy-init -g ilc_prod
	dirac-ilc-add-software --platform=$platform --name=SLICPandora --version=$version --comment="$comment"
	echo -e "\E[030m"
	exit 0
    else
	echo -e "\E[031mCan't find PandoraFrontend, environment not set: Aborting\E[030m"
	exit 1
    fi
fi
