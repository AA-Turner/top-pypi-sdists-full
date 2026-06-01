#!/bin/bash -eux
# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

get_version () {
    RPM=$1;
    B=${RPM##*/};
    B=${B%-*};
    V=${B##*-};
}

IVS_VERSION='NOT-FOUND'
COUNT="`ls -1 ./ivs-debug*. 2>/dev/null | wc -l`"
if [ $COUNT != 0 ]
then
    IVS_PKG="`ls ./ivs-debug*`"
    get_version $IVS_PKG
    IVS_VERSION=$V
fi

NETWORKING_BIGSWITCH_VERSION='NOT-FOUND'
COUNT="`ls -1 ./python-networking-bigswitch* 2>/dev/null | wc -l`"
if [ $COUNT != 0 ]
then
    BSNLIB_PKG="`ls ./python-networking-bigswitch*`"
    get_version $BSNLIB_PKG
    NETWORKING_BIGSWITCH_VERSION=$V
fi

HORIZON_BSN_VERSION='NOT-FOUND'
COUNT="`ls -1 ./python-horizon-bsn* 2>/dev/null | wc -l`"
if [ $COUNT != 0 ]
then
    HORIZON_PKG="`ls ./python-horizon-bsn*`"
    get_version $HORIZON_PKG
    HORIZON_BSN_VERSION=$V
fi


echo "ivs version is" $IVS_VERSION
echo "networking-bigswitch version is" $NETWORKING_BIGSWITCH_VERSION
echo "horizon-bsn version is" $HORIZON_BSN_VERSION

# IVS_VERSION_REVISION includes ivs version with its revision number, default = -1. redhat naming convention
# that needs to be adhered.
IVS_VERSION_REVISION="$IVS_VERSION""-1"

sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./customize.sh
sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./startup.sh
sed -i -e "s/\${networking_bigswitch_version}/$NETWORKING_BIGSWITCH_VERSION/" -e "s/\${horizon_bsn_version}/$HORIZON_BSN_VERSION/" -e "s/\${ivs_version}/$IVS_VERSION_REVISION/" ./README
