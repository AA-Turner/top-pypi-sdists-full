#!/bin/bash

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

