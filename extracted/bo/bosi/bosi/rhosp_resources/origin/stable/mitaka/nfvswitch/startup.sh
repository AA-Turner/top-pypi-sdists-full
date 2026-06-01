#!/bin/bash

ISOL_CPU="2-55"
HUGEPAGES="12288"

yum remove -y openstack-neutron-bigswitch-agent
yum remove -y openstack-neutron-bigswitch-lldp
yum remove -y python-networking-bigswitch

rpm -ivhU --force /root/python-networking-bigswitch-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/openstack-neutron-bigswitch-agent-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/openstack-neutron-bigswitch-lldp-${networking_bigswitch_version}-1.el7.centos.noarch.rpm
rpm -ivhU --force /root/python-horizon-bsn-${horizon_bsn_version}-1.el7.centos.noarch.rpm

systemctl enable neutron-bsn-lldp.service
systemctl restart neutron-bsn-lldp.service

if [[ $(hostname) == *compute* ]]; then
    rpm -ivhU --force /root/ivs-${ivs_version}.el7.centos.x86_64.rpm
    rpm -ivhU --force /root/ivs-debuginfo-${ivs_version}.el7.centos.x86_64.rpm
    rpm -ivhU --force /root/nfvswitch-${nfvswitch_version}.el7.centos.x86_64.rpm
    rpm -ivhU --force /root/nfvswitch-debuginfo-${nfvswitch_version}.el7.centos.x86_64.rpm

    grubby --update-kernel=ALL --args="isolcpus=$ISOL_CPU nohz_full=$ISOL_CPU hugepages=$HUGEPAGES iommu=pt intel_iommu=on"
    reboot
fi
