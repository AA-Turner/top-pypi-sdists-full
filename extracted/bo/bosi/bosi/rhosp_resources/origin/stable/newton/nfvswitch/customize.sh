#!/bin/bash

export LIBGUESTFS_BACKEND=direct

image_dir="/home/stack/images"

virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload python-networking-bigswitch-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload openstack-neutron-bigswitch-lldp-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload openstack-neutron-bigswitch-agent-${networking_bigswitch_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload python-horizon-bsn-${horizon_bsn_version}-1.el7.centos.noarch.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload ivs-${ivs_version}.el7.centos.x86_64.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload ivs-debuginfo-${ivs_version}.el7.centos.x86_64.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload nfvswitch-${nfvswitch_version}.el7.centos.x86_64.rpm:/root/
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload nfvswitch-debuginfo-${nfvswitch_version}.el7.centos.x86_64.rpm:/root/

# Temp work-around to include os-net-config patch with RHOSP9: Enable os-net-config to support and configure NFVSwitch
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload osnet-patch/impl_ifcfg.py:/usr/lib/python2.7/site-packages/os_net_config/impl_ifcfg.py
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload osnet-patch/__init__.py:/usr/lib/python2.7/site-packages/os_net_config/__init__.py
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload osnet-patch/objects.py:/usr/lib/python2.7/site-packages/os_net_config/objects.py

# Temp work-around to set selinux to permissive mode to allow QEMU access to vhost-user
virt-customize -a ${image_dir}/overcloud-full.qcow2 --upload selinux-config:/etc/selinux/config

virt-customize -a ${image_dir}/overcloud-full.qcow2 --firstboot startup.sh
