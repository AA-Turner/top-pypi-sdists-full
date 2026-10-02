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

wget -O dirac-install -np https://raw.githubusercontent.com/DIRACGrid/management/master/dirac-install.py  --no-check-certificate
chmod +x dirac-install
./dirac-install -V ILCDIRAC

source bashrc
dirac-proxy-init -x

vo=ilc
setup=ILC-Production
csserver=dips://voilcdiracconfig.cern.ch:9135/Configuration/Server

dirac-configure -V $vo -S $setup -C $csserver -d --SkipCAChecks
echo ""
echo "To get the proper environment, run source bashrc"
echo ""
echo "You can now obtain a dirac proxy by running"
echo "dirac-proxy-init"
