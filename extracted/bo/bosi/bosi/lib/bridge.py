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

class Bridge(object):
    def __init__(self, br_key, br_name, br_ip, br_vlan):
        self.br_key = br_key
        self.br_name = br_name
        self.br_ip = br_ip
        self.br_vlan = br_vlan

    def __str__(self):
        return (r'''{br_key : %(br_key)s, br_name : %(br_name)s, br_ip :
                %(br_ip)s, br_vlan : %(br_vlan)s}''' %
                {'br_key': self.br_key, 'br_name': self.br_name,
                 'br_ip': self.br_ip, 'br_vlan': self.br_vlan})

    def __repr__(self):
        return self.__str__()
