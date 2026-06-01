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
phy1_name={phy1_name}
phy1_nics={phy1_nics}
phy2_name={phy2_name}
phy2_nics={phy2_nics}
active_active={active_active}
system_desc={system_desc}

# constants for this job
SERVICE_FILE_1='/usr/lib/systemd/system/send_lldp_1.service'
SERVICE_FILE_2='/usr/lib/systemd/system/send_lldp_2.service'
SERVICE_FILE_MULTI_USER_1='/etc/systemd/system/multi-user.target.wants/send_lldp_1.service'
SERVICE_FILE_MULTI_USER_2='/etc/systemd/system/multi-user.target.wants/send_lldp_2.service'

# new vars with evaluated results
HOSTNAME=`cat /etc/hostname`

# Make sure only root can run this script
if [ "$(id -u)" != "0" ]; then
   echo -e "Please run as root"
   exit 1
fi

# if service file exists, stop and disable the service. else, return true
systemctl stop send_lldp_1 | true
systemctl stop send_lldp_2 | true
systemctl disable send_lldp_1 | true
systemctl disable send_lldp_2 | true

# rewrite service file
echo "
[Unit]
Description=BSN send_lldp for physnet 1
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/bin/python /usr/lib/python2.7/site-packages/networking_bigswitch/bsnlldp/send_lldp.py \
    --system-desc ${{system_desc}} \
    --system-name ${{HOSTNAME}}-${{phy1_name}} \
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

if [[ $active_active == true ]]; then
    rm $SERVICE_FILE_2
    rm $SERVICE_FILE_MULTI_USER_2
else
echo "
[Unit]
Description=BSN send_lldp for physnet 2
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/bin/python /usr/lib/python2.7/site-packages/networking_bigswitch/bsnlldp/send_lldp.py \
    --system-desc ${{system_desc}} \
    --system-name ${{HOSTNAME}}-${{phy2_name}} \
    -i 10 \
    --network_interface ${{phy2_nics}} \
    --sriov
Restart=always
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
" > $SERVICE_FILE_2

# add multi user symlink for send_lldp_2
ln -sf $SERVICE_FILE_2 $SERVICE_FILE_MULTI_USER_2
fi

# reload service files
systemctl daemon-reload

# start services as required
systemctl enable send_lldp_1
systemctl start send_lldp_1

if [[ $active_active != true ]]; then
    # no bonding, start both agents
    systemctl enable send_lldp_2
    systemctl start send_lldp_2
fi

echo "Finished updating with SRIOV LLDP scripts."
