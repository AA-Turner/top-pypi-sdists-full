#!/bin/bash
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

is_controller=%(is_controller)s

install_pkg() {
    pkg=$1
    cd %(dst_dir)s/upgrade
    tar -xzf $pkg
    dir=${pkg::-7}
    cd $dir
    python setup.py build
    python setup.py install
}

controller() {

    PKGS=%(dst_dir)s/upgrade/*
    for pkg in $PKGS
    do
        if [[ $pkg == *"networking-bigswitch"* ]]; then
            install_pkg $pkg
            neutron-db-manage upgrade heads
            systemctl enable neutron-server
            systemctl restart neutron-server
        fi
        if [[ $pkg == *"neutronclient"* ]]; then
            install_pkg $pkg
        fi
        if [[ $pkg == *"horizon-bsn"* ]]; then
            install_pkg $pkg
            systemctl restart httpd
        fi
        if [[ $pkg == *"neutron-bsn-lldp"* ]]; then
            install_pkg $pkg
            systemctl enable neutron-bsn-lldp
            systemctl restart neutron-bsn-lldp
        fi
    done
}

compute() {

    PKGS=%(dst_dir)s/upgrade/*
    for pkg in $PKGS
    do
        if [[ $pkg == *"networking-bigswitch"* ]]; then
            install_pkg $pkg
            systemctl enable neutron-bsn-lldp
            systemctl restart neutron-bsn-lldp
        fi
        if [[ $pkg == *"neutron-bsn-lldp"* ]]; then
            install_pkg $pkg
            systemctl enable neutron-bsn-lldp
            systemctl restart neutron-bsn-lldp
        fi
    done
}


set +e

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
    echo -e "Please run as root"
    exit 1
fi

# if bsnstacklib is installed, uninstall it
pip uninstall -y bsnstacklib || true

if [[ $is_controller == true ]]; then
    controller
else
    compute
fi

set -e

exit 0
