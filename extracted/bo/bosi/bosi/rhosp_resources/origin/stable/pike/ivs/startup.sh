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

yum remove -y openstack-neutron-bigswitch-agent
yum remove -y openstack-neutron-bigswitch-lldp
yum remove -y python-networking-bigswitch
rpm -ivhU --force /root/python-networking-bigswitch-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/openstack-neutron-bigswitch-agent-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/openstack-neutron-bigswitch-lldp-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/python-horizon-bsn-${horizon_bsn_version}-1.el7.centos.noarch.rpm
# enabled for P+V mode
#rpm -ivhU --force /root/ivs-${ivs_version}-1.el7.centos.x86_64.rpm
#rpm -ivhU --force /root/ivs-debuginfo-${ivs_version}-1.el7.centos.x86_64.rpm
systemctl enable neutron-bsn-lldp.service
systemctl restart neutron-bsn-lldp.service
