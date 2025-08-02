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


#-------------------------------------------------------------------------------
# Checks

# Check arguments

if [ $# -ne 2 ]; then

    echo "$0 <version> <comment>"
    echo "Example: $0 1 \"Bugs fixed\""

    exit 1

fi

# Check environment variables

if [ ! -d $LCIO ]; then

    echo "\$LCIO is not set or is not a directory"

    exit 1

fi

#-------------------------------------------------------------------------------
# Variables
#
# TARBALL_DIR = temporary dir where binaries and libraries are stored
# TARBALL_FILE = filename of the final tarball in the current directory

VERSION=$1
COMMENT=$2

TARBALL_NAME=lcio
TARBALL_DIR=`pwd`/${TARBALL_NAME}${VERSION}
TARBALL_FILE=`pwd`/${TARBALL_NAME}${VERSION}.tgz

RSYNC_EXCLUDE="--exclude='*CVS*' --exclude='*cmake*'"

#-------------------------------------------------------------------------------
# Prepare everything for the tar ball

mkdir -p $TARBALL_DIR

# Copy LCIO

rsync -avzL $RSYNC_EXCLUDE $LCIO/bin/*   $TARBALL_DIR/bin
rsync -avzL $RSYNC_EXCLUDE $LCIO/lib/*   $TARBALL_DIR/lib
rsync -avzL $RSYNC_EXCLUDE $LCIO/tools/* $TARBALL_DIR/tools

# Copy library files for all executables found in the bin directory

for FILE in $( find $TARBALL_DIR/bin -type f -perm -u+x ! -type d ); do

    LIBRARIES=$( ldd $FILE | grep "=>" | sed 's/.*=>//g' | sed "s/(.*)//g" )

    # Is $FILE a binary or not.

    if [ -z "$LIBRARIES" ]; then
        continue
    fi

    # Flatten the output of ldd to one line

    FILES=""

    for LINE in $LIBRARIES; do

        FILES="$FILES $LINE"

    done

    # Copy files

    echo "Copying files for $FILE"
    rsync -avzL $FILES $TARBALL_DIR/lib
    python $DIRAC/ILCDIRAC/Core/Utilities/PrepareLibs.py $TARBALL_DIR/lib
done

cd $TARBALL_DIR/
find . -type f -print0 | xargs -0 md5sum > md5_checksum.md5
cd -

# Make the tar ball

tar -czvf $TARBALL_FILE `basename $TARBALL_DIR`

#-------------------------------------------------------------------------------
# Add to Dirac CS

source /afs/cern.ch/eng/clic/software/DIRAC/bashrc
#
platform=`dirac-architecture`
#
dirac-proxy-init -g diracAdmin
dirac-ilc-add-software -P $platform -N $TARBALL_NAME -V $VERSION -C "$COMMENT"

