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

controller() {

    PKGS=/tmp/upgrade/*

    # the first four packages are applicable for RHOSP releases upto Pike
    # i.e. RHOSP 12
    for pkg in $PKGS
    do
        if [[ $pkg == *"python-networking-bigswitch"* ]]; then
            yum remove -y python-networking-bigswitch
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            neutron-db-manage upgrade heads
            systemctl enable neutron-server
            systemctl restart neutron-server
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"openstack-neutron-bigswitch-lldp"* ]]; then
            yum remove -y openstack-neutron-bigswitch-lldp
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl enable  neutron-bsn-lldp
            systemctl restart neutron-bsn-lldp
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"openstack-neutron-bigswitch-agent"* ]]; then
            yum remove -y openstack-neutron-bigswitch-agent
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl stop neutron-bsn-agent
            systemctl disable neutron-bsn-agent
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"python-horizon-bsn"* ]]; then
            yum remove -y python-horizon-bsn
            rpm -ivhU $pkg --force
            systemctl restart httpd
            break
        fi
    done
    # Following packages are applicable for Queens release i.e. RHOSP 13
    # and above
    for pkg in $PKGS
    do
        if [[ $pkg == *"neutron-bsn-lldp"* ]]; then
            yum remove -y neutron-bsn-lldp
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl enable  neutron-bsn-lldp
            systemctl restart neutron-bsn-lldp
            break
        fi
    done
}

compute() {

    PKGS=/tmp/upgrade/*
    for pkg in $PKGS
    do
        if [[ $pkg == *"python-networking-bigswitch"* ]]; then
            yum remove -y python-networking-bigswitch
            rpm -ivhU $pkg --force
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"openstack-neutron-bigswitch-agent"* ]]; then
            yum remove -y openstack-neutron-bigswitch-agent
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl enable neutron-bsn-agent
            systemctl restart neutron-bsn-agent
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"ivs-debuginfo"* ]]; then
            rpm -ivhU $pkg --force
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"ivs"* ]]; then
            if [[ $pkg == *"ivs-debuginfo"* ]]; then
                continue
            fi
            if [[ $pkg == *"-ivs"* ]]; then
                continue
            fi
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl enable ivs
            systemctl restart ivs
            break
        fi
    done

    # do the same as IVS for NFVSWITCH
    for pkg in $PKGS
    do
        if [[ $pkg == *"nfvswitch-debuginfo"* ]]; then
            rpm -ivhU $pkg --force
            break
        fi
    done

    for pkg in $PKGS
    do
        if [[ $pkg == *"nfvswitch"* ]]; then
            if [[ $pkg == *"nfvswitch-debuginfo"* ]]; then
                continue
            fi
            rpm -ivhU $pkg --force
            systemctl daemon-reload
            systemctl enable nfvswitch
            systemctl restart nfvswitch
            break
        fi
    done
}


set +e

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
    echo -e "Please run as root"
    exit 1
fi

if [[ $is_controller == true ]]; then
    controller
else
    compute
fi

set -e

exit 0

