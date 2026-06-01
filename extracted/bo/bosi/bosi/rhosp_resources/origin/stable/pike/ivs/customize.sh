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

export LIBGUESTFS_BACKEND=direct

image_dir="/home/stack/images"

virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload python-networking-bigswitch-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload openstack-neutron-bigswitch-lldp-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload openstack-neutron-bigswitch-agent-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload python-horizon-bsn-${horizon_bsn_version}-1.el7.centos.noarch.rpm:/root/

# enabled for P+V mode
#ivs_version="TODO set_IVS_version_here_if_deploying_PV_mode"
#virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload ivs-${ivs_version}-1.el7.centos.x86_64.rpm:/root/
#virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload ivs-debuginfo-${ivs_version}-1.el7.centos.x86_64.rpm:/root/
#sed -i -e "s/\${ivs_version}/$ivs_version/" ./startup.sh

virt-customize -a ${image_dir}/overcloud-full.qcow2 --firstboot startup.sh

# ensure os-net-config is not overwritten by empty template
# new heat-hiera hooks are used to configure it, starting with Ocata (RHOSP 11)
virt-customize -a ${image_dir}/overcloud-full.qcow2 --delete /usr/libexec/os-apply-config/templates/etc/os-net-config/config.json
