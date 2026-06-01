#!/bin/bash

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
