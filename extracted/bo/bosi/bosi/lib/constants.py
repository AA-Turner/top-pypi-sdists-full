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

from enum import Enum
from enum import EnumMeta

# uname -n cutoff length for port group name
UNAME_CUTOFF = 249

# max number of threads, each thread sets up one node
MAX_WORKERS = 10

# root access to all the nodes is required
DEFAULT_USER = 'root'

# key words to specify node role in yaml config
ROLE_NEUTRON_SERVER = 'controller'
ROLE_COMPUTE = 'compute'
ROLE_CEPH = 'ceph-osd'
ROLE_CINDER = "cinder"
ROLE_MONGO = 'mongo'
ROLE_SRIOV = 'sriov'
ROLE_DPDK = 'ovs-dpdk'
ROLE_DPDK_CONTROL = 'ovs-dpdk-controller'
ROLE_DPDK_COMPUTE = 'ovs-dpdk-compute'
DPDK_ROLES = [ROLE_DPDK, ROLE_DPDK_CONTROL, ROLE_DPDK_COMPUTE]

# deployment t6/t5
T6 = 't6'
T5 = 't5'

MODE_DICT = {'pfabric': T5,
             'pvfabric': T6}

OS_BCF_MAPPING_LOWER = {
    'kilo': {
        '3.6': '20151.36'
    },
    'liberty': {
        '3.6': '20153.36',
        '3.7': '20153.36',
        '4.0': '20153.36',
        '4.1': '20153.36',
        '4.2': '20153.36'
    },
    'mitaka': {
        '3.7': '8.37',
        '4.0': '8.37',
        '4.1': '8.37',
        '4.2': '8.37',
        '4.5': '8.40'
    },
    'newton': {
        '4.2': '9.42',
        '4.5': '9.42',
        '4.6': '9.42',
        '4.7': '9.42'
    },
    'ocata': {
        '4.6': '10.46',
        '4.7': '10.46'
    },
    'pike': {
        '4.7': '11.47'
    },
    'queens': {
        '4.7': '12.0',
        '5.0': '12.0',
        '5.1': '12.0',
        '5.2': '12.0',
        '5.3': '12.0'
    },
    'train': {
        '6.0': '15.0',
        '6.1': '15.0'
    }
}

OS_BCF_MAPPING_UPPER = {
    'kilo': {
        '3.6': '20151.37'
    },
    'liberty': {
        '3.6': '20153.37',
        '3.7': '20153.38',
        '4.0': '20153.41',
        '4.1': '20153.41',
        '4.2': '20153.41'
    },
    'mitaka': {
        # NOTE : we released a 8.40 by mistake and cannot downgrade on pypi,
        # hence upper is 8.41 instead of 8.38. we'll have to keep track
        # of incompatibilities to make sure it doesn't break anything
        '3.7': '8.41',
        '4.0': '8.41',
        '4.1': '8.41',
        '4.2': '8.41',
        '4.5': '8.41'
    },
    'newton': {
        '4.2': '9.43',
        '4.5': '9.43',
        '4.6': '9.43',
        '4.7': '9.43'
    },
    'ocata': {
        '4.6': '10.47',
        '4.7': '10.47'
    },
    'pike' : {
        '4.7': '11.48'
    },
    'queens': {
        '4.7': '12.1',
        '5.0': '12.1',
        '5.1': '12.1',
        '5.2': '12.1',
        '5.3': '12.1'
    },
    'train': {
        '6.0': '15.0',
        '6.1': '15.0'
    }
}

# Since kilo and BCF 3.5, we use tenant name
# instead of tenant uuid to configure tenants,
# The default version is 2. However, in case
# of upgrade, where tenant configuraion was
# using uuid, user needs to use version 1
# to make upgrade happen.
TENANT_UUID_API_VERSION = 1
TENANT_NAME_API_VERSION = 2

IVS_TAR_PKG_DIRS = ["pkg/centos7-x86_64", "pkg/trusty-amd64"]

# constant file, directory names for each node
PRE_REQUEST_BASH = 'pre_request.sh'
DST_DIR = '/tmp'
GENERATED_SCRIPT_DIR = 'generated_script'
BASH_TEMPLATE_DIR = 'bash_template'
PYTHON_TEMPLATE_DIR = 'python_template'
PUPPET_TEMPLATE_DIR = 'puppet_template'
SELINUX_TEMPLATE_DIR = 'selinux_template'
OSPURGE_TEMPLATE_DIR = 'ospurge_template'
LOG_FILE = "/var/log/bcf_setup.log"

# constants for ivs config
INBAND_VLAN = 4092
IVS_DAEMON_ARGS_CERT = (r'''DAEMON_ARGS=\"--hitless --certificate /etc/ivs '''
                        '''--inband-vlan %(inband_vlan)d'''
                        '''%(uplink_interfaces)s%(internal_ports)s\\"''')
IVS_DAEMON_ARGS = (r'''DAEMON_ARGS=\"--hitless '''
                   '''--inband-vlan %(inband_vlan)d'''
                   '''%(uplink_interfaces)s%(internal_ports)s\\"''')

# constants of supported OSes and versions
CENTOS = 'centos'
CENTOS_VERSIONS = ['7']
UBUNTU = 'ubuntu'
UBUNTU_VERSIONS = ['14']
REDHAT = 'redhat'
REDHAT_VERSIONS = ['7']

# OSes that uses rpm or deb packages
RPM_OS_SET = [CENTOS, REDHAT]
DEB_OS_SET = [UBUNTU]

# regular expressions
EXISTING_NETWORK_VLAN_RANGE_EXPRESSION = (
    '^\s*network_vlan_ranges\s*=\s*(\S*)\s*:\s*(\S*)\s*:\s*(\S*)\s*$')
NETWORK_VLAN_RANGE_EXPRESSION = '^\s*(\S*)\s*:\s*(\S*)\s*:\s*(\S*)\s*$'
VLAN_RANGE_CONFIG_PATH = '/etc/neutron/plugins/ml2/ml2_conf.ini'
SELINUX_MODE_EXPRESSION = '^\s*SELINUX\s*=\s*(\S*)\s*$'
SELINUX_CONFIG_PATH = '/etc/selinux/config'


# openrc
FUEL_OPENRC = '/root/openrc'
PACKSTACK_OPENRC = '/root/keystonerc_admin'
MANUAL_OPENRC = '/root/admin-openrc.sh'
RHOSP_UNDERCLOUD_OPENRC = '/home/stack/stackrc'
RHOSP_OVERCLOUD_OPENRC = '/home/stack/overcloudrc'

# fuel constants
NONE_IP = 'none'
BR_KEY_PRIVATE = 'neutron/private'
BR_KEY_FW_ADMIN = 'fw-admin'
BR_NAME_INT = 'br-int'

# ivs internal port prefix mapping
IVS_INTERNAL_PORT_DIC = {
    'management': 'm',
    'ex': 'e',
    'storage': 's'}

HASH_HEADER = 'BCF-SETUP'
BCF_CONTROLLER_PORT = 8443
ANY = 'any'

# T5 for Centos requires extra params when using packstack
T5_CENTOS_BOND_BRIDGE = 'br-bond0'
T5_CENTOS_BOND_NAME = 'bond0'

# big db error message
ELEMENT_EXISTS = "List element already exists"

# directory for csr
CSR_DIR = "/tmp/csr"
KEY_DIR = "/tmp/key"

# constants for csr
CSR_SUB = r'''/C=US/ST=California/L=Santa Clara/O=BSN/CN=%(cn)s'''

# support constants
SUPPORT_DIR = "/tmp/support"

# upgrade pkg key words
UPGRADE_PYPI = ["ivs-debuginfo", "ivs", "horizon-bsn", "bsnstacklib"]
UPGRADE_RPM = ["ivs-debuginfo", "ivs", "python-networking-bigswitch", "openstack-neutron-bigswitch-agent", "openstack-neutron-bigswitch-lldp", "python-horizon-bsn"]


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__


class BondMode(Enum):
    """
    This maps SRIOV/DPDK bond mode to its corresponding MAC address to be
    used by the LLDP script as system-desc.
    """
    __metaclass__ = MetaEnum

    STATIC = '5c:16:c7:00:00:00'
    LACP = '5c:16:c7:00:00:04'
