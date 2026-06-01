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

# This template deletes all network related resources for fresh installation.

source %(openrc)s

# delete all routers
routers=$(neutron router-list | awk '$2 != "id" {print $2}' | awk 'NF && $1!~/^#/')
for router in $routers; do
    # delete all subnets that have interface on router
    subnets=$(neutron router-port-list $router | awk '$0 ~ /.*subnet_id.*/ {print $0}' | awk '{print $(NF - 3)}' | tr -d ,| tr -d \")
    for subnet in $subnets; do
        neutron router-interface-delete $router $subnet
    done
    neutron router-gateway-clear $router
    neutron router-delete $router
done

# delete floating ips
floatingips=$(neutron floatingip-list | awk '$2 != "id" {print $2}' | awk 'NF && $1!~/^#/')
for floatingip in $floatingips; do
    neutron floatingip-delete $floatingip
done

# delete nova instances
instances=$(nova list --all-tenants | awk '$2 != "ID" {print $2}' | awk 'NF && $1!~/^#/')
for instance in $instances; do
    nova delete $instance
done

# delete all subnets
subnets=$(neutron subnet-list | awk '$2 != "id" {print $2}' | awk 'NF && $1!~/^#/')
for subnet in $subnets; do
    neutron subnet-delete $subnet
done

# delete all networks
nets=$(neutron net-list | awk '$2 != "id" {print $2}' | awk 'NF && $1!~/^#/')
for net in $nets; do
    neutron net-delete $net
done
