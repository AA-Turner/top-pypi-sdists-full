#!/bin/bash
# Copyright 2021 Arista Networks, Inc.
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


virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload neutron-arista-ccf-lldp-${lldp_version}-1.el8.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload selinux-rules-lldp/neutron-arista-ccf-selinux.pp:/root/

virt-customize -a ${image_dir}/overcloud-full.qcow2 --install /root/neutron-arista-ccf-lldp-${lldp_version}-1.el8.noarch.rpm
virt-customize -a ${image_dir}/overcloud-full.qcow2 --run-command "systemctl enable neutron-arista-ccf-lldp.service"
virt-customize -a ${image_dir}/overcloud-full.qcow2 --run-command "semodule -i /root/neutron-arista-ccf-selinux.pp"

