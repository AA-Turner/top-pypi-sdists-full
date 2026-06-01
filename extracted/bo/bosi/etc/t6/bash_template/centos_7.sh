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

install_bsnstacklib=%(install_bsnstacklib)s
install_ivs=%(install_ivs)s
install_all=%(install_all)s
deploy_dhcp_agent=%(deploy_dhcp_agent)s
ivs_version=%(ivs_version)s
is_controller=%(is_controller)s
fuel_cluster_id=%(fuel_cluster_id)s
openstack_release=%(openstack_release)s
skip_ivs_version_check=%(skip_ivs_version_check)s
pip_proxy=%(pip_proxy)s
offline_dir=%(dst_dir)s/offline


controller() {

    echo 'Stop and disable metadata agent, dhcp agent, l3 agent'
    systemctl stop neutron-l3-agent
    systemctl disable neutron-l3-agent
    systemctl stop neutron-dhcp-agent
    systemctl disable neutron-dhcp-agent
    systemctl stop neutron-metadata-agent
    systemctl disable neutron-metadata-agent
    systemctl stop neutron-bsn-agent
    systemctl disable neutron-bsn-agent

    # if offline directory does not exist, install neutron-bsn-lldp for
    # controller nodes
    if [[ -d $offline_dir ]]; then
        elif [[ $pip_proxy == false ]]; then
            pip install --upgrade "neutron-bsn-lldp>=1.0.0,<1.1.0"
        else
            pip --proxy $pip_proxy  install --upgrade "neutron-bsn-lldp>=1.0.0,<1.1.0"
        fi
    fi

    # deploy bcf
    puppet apply --modulepath /etc/puppet/modules %(dst_dir)s/%(hostname)s.pp

    # bsnstacklib installed and property files updated. now perform live db migration
    echo "Performing live DB migration for Neutron.."
    if [[ $openstack_release == 'kilo' || $openstack_release == 'kilo_v2' ]]; then
        neutron-db-manage --service bsn_service_plugin upgrade head
    else
        neutron-db-manage upgrade heads
    fi

    # deploy bcf horizon patch to controller node
    cp /usr/lib/python2.7/site-packages/horizon_bsn/enabled/* /usr/share/openstack-dashboard/openstack_dashboard/enabled/
    systemctl restart httpd
    keystone-manage token_flush

    echo 'Restart neutron-server'
    rm -rf /var/lib/neutron/host_certs/*
    systemctl restart neutron-server
}

compute() {

    systemctl stop neutron-l3-agent
    systemctl disable neutron-l3-agent
    systemctl stop neutron-dhcp-agent
    systemctl disable neutron-dhcp-agent
    systemctl stop neutron-metadata-agent
    systemctl disable neutron-metadata-agent

    # install os-vif-bigswitch on compute nodes
    if [[ -d $offline_dir ]]; then
        elif [[ $pip_proxy == false ]]; then
            pip install --upgrade "os-vif-bigswitch>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        else
            pip --proxy $pip_proxy  install --upgrade "os-vif-bigswitch>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        fi
    fi

    # install ivs
    if [[ $install_ivs == true ]]; then
        # check ivs version compatability
        pass=true
        ivs --version
        if [[ $? == 0 ]]; then
            old_version=$(ivs --version | awk '{print $2}')
            old_version_numbers=(${old_version//./ })
            new_version_numbers=(${ivs_version//./ })
            if [[ "$old_version" != "${old_version%%$ivs_version*}" ]]; then
                pass=true
            elif [[ $old_version > $ivs_version ]]; then
                pass=false
            elif [[ $((${new_version_numbers[0]}-1)) -gt ${old_version_numbers[0]} ]]; then
                pass=false
            fi
        fi

        if [[ $pass == true ]]; then
            rpm -ivhU --force %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                rpm -ivhU --force %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        elif [[ $skip_ivs_version_check == true ]]; then
            rpm -ivhU --force %(dst_dir)s/%(ivs_pkg)s
            if [[ -f %(dst_dir)s/%(ivs_debug_pkg)s ]]; then
                rpm -ivhU --force %(dst_dir)s/%(ivs_debug_pkg)s
            fi
        else
            echo "ivs upgrade fails version validation"
        fi
    fi
    systemctl stop ivs

    # full installation
    if [[ $install_all == true ]]; then
        cp /usr/lib/systemd/system/neutron-openvswitch-agent.service /usr/lib/systemd/system/neutron-bsn-agent.service

        # stop ovs agent, otherwise, ovs bridges cannot be removed
        systemctl stop neutron-openvswitch-agent
        systemctl disable neutron-openvswitch-agent

        # remove ovs, example ("br-storage" "br-prv" "br-ex")
        declare -a ovs_br=(%(ovs_br)s)
        len=${#ovs_br[@]}
        for (( i=0; i<$len; i++ )); do
            ovs-vsctl del-br ${ovs_br[$i]}
            brctl delbr ${ovs_br[$i]}
            ip link del dev ${ovs_br[$i]}
        done

        # delete ovs br-int
        while true; do
            systemctl stop neutron-openvswitch-agent
            systemctl disable neutron-openvswitch-agent
            ovs-vsctl del-br %(br-int)s
            ip link del dev %(br-int)s
            sleep 1
            ovs-vsctl show | grep %(br-int)s
            if [[ $? != 0 ]]; then
                break
            fi
        done

        #bring down all bonds
        declare -a bonds=(%(bonds)s)
        len=${#bonds[@]}
        for (( i=0; i<$len; i++ )); do
            ip link del dev ${bonds[$i]}
        done

        # deploy bcf
        puppet apply --modulepath /etc/puppet/modules %(dst_dir)s/%(hostname)s.pp

        #reset uplinks to move them out of bond
        declare -a uplinks=(%(uplinks)s)
        len=${#uplinks[@]}
        for (( i=0; i<$len; i++ )); do
            ip link set ${uplinks[$i]} down
        done
        sleep 2
        for (( i=0; i<$len; i++ )); do
            ip link set ${uplinks[$i]} up
        done

        # assign default gw
        bash /etc/rc.d/rc.local

    fi

    if [[ $deploy_dhcp_agent == true ]]; then
        echo 'Restart neutron-metadata-agent and neutron-dhcp-agent'
        systemctl restart neutron-metadata-agent
        systemctl enable neutron-metadata-agent
        systemctl restart neutron-dhcp-agent
        systemctl enable neutron-dhcp-agent
    fi

    systemctl restart ivs

    echo 'Restart neutron-bsn-agent'
    systemctl restart neutron-bsn-agent

    # patch nova rootwrap
    mkdir -p /usr/share/nova
    rm -rf /usr/share/nova/rootwrap
    rm -rf %(dst_dir)s/rootwrap/rootwrap
    cp -r %(dst_dir)s/rootwrap /usr/share/nova/
    chmod -R 777 /usr/share/nova/rootwrap
    rm -rf /usr/share/nova/rootwrap/rootwrap
}

install_pkg() {
    pkg=$1
    cd $offline_dir
    tar -xzf $pkg
    dir=${pkg::-7}
    cd $dir
    python setup.py build
    python setup.py install
}

set +e

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo -e "Please run as root"
   exit 1
fi

# in case of offline installation, these dependencies are expected to be pre-installed
if [[ ! -d $offline_dir ]]; then
    # prepare dependencies
    yum install -y wget

    wget -r --no-parent --no-directories --timestamping --accept 'epel-release-7-*.rpm' 'http://dl.fedoraproject.org/pub/epel/7/x86_64/e/'
    rpm -iUvh epel-release-7-*.rpm
    rpm -ivh https://yum.puppetlabs.com/el/7/products/x86_64/puppetlabs-release-7-10.noarch.rpm
    yum groupinstall -y 'Development Tools'
    yum install -y python-devel puppet python-pip wget libffi-devel openssl-devel
    easy_install pip
    pip install --upgrade funcsigs
    puppet module install --force puppetlabs-inifile
    puppet module install --force puppetlabs-stdlib
fi

# install bsnstacklib, now known as networking-bigswitch
if [[ $install_bsnstacklib == true ]]; then
    pip uninstall -y networking-bigswitch || true
    sleep 2

    if [[ -d $offline_dir ]]; then
        # install from offline package dir if available
        PKGS=$offline_dir/*
        for pkg in $PKGS
        do
            install_pkg $pkg
        done
    # else online
    elif [[ $pip_proxy == false ]]; then
        pip install --upgrade "networking-bigswitch>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        pip install --upgrade "python-bsn-neutronclient>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        pip install --upgrade "horizon-bsn>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
    else
        pip --proxy $pip_proxy  install --upgrade "networking-bigswitch>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        pip --proxy $pip_proxy  install --upgrade "python-bsn-neutronclient>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
        pip --proxy $pip_proxy  install --upgrade "horizon-bsn>=%(bsnstacklib_version_lower)s,<%(bsnstacklib_version_upper)s"
    fi
fi

if [[ $is_controller == true ]]; then
    controller
else
    compute
fi

set -e

exit 0
