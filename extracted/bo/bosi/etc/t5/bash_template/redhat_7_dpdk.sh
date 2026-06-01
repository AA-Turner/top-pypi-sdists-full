#!/bin/bash -eux
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

# env variables to be supplied by BOSI
fqdn={fqdn}
is_controller={is_controller}
phy1_name={phy1_name}
phy1_nics={phy1_nics}
system_desc={system_desc}

# constants for this job
SERVICE_FILE_1='/usr/lib/systemd/system/send_lldp.service'
SERVICE_FILE_MULTI_USER_1='/etc/systemd/system/multi-user.target.wants/send_lldp.service'

# new vars with evaluated results
HOSTNAME=`hostname -f`

# system name for LLDP depends on whether its a controller or compute node
SYSTEMNAME=${{HOSTNAME}}-${{phy1_name}}
if [[ $is_controller == true ]]; then
    SYSTEMNAME=${{HOSTNAME}}
fi

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo -e "Please run as root"
   exit 1
fi

# if service file exists, stop and disable the service. else, return true
systemctl stop send_lldp | true
systemctl disable send_lldp | true

# rewrite service file
echo "
[Unit]
Description=BSN send_lldp for DPDK physnet
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/bin/python /usr/lib/python2.7/site-packages/networking_bigswitch/bsnlldp/send_lldp.py \
    --system-desc ${{system_desc}} \
    --system-name ${{SYSTEMNAME}} \
    -i 10 \
    --network_interface ${{phy1_nics}} \
    --sriov
Restart=always
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
" > $SERVICE_FILE_1

# symlink multi user file
ln -sf $SERVICE_FILE_1 $SERVICE_FILE_MULTI_USER_1

# reload service files
systemctl daemon-reload

# start services as required
systemctl enable send_lldp
systemctl start send_lldp

echo "Finished updating with DPDK LLDP scripts."
