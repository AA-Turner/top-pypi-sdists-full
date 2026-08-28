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

from typing import ClassVar
import uuid

from openstackclient.tests.functional.network.v2 import common


class IPAvailabilityTests(common.NetworkTests):
    """Functional tests for IP availability"""

    NAME: ClassVar[str]
    NETWORK_NAME: ClassVar[str]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if cls.haz_network:
            cls.NAME = uuid.uuid4().hex
            cls.NETWORK_NAME = uuid.uuid4().hex

            # Create a network for the subnet
            cls.openstack('network create ' + cls.NETWORK_NAME)
            cmd_output = cls.openstack(
                'subnet create '
                + '--network '
                + cls.NETWORK_NAME
                + ' '
                + '--subnet-range 10.10.10.0/24 '
                + cls.NAME,
                parse_output=True,
            )
            cls.assertOutput(cls.NAME, cmd_output['name'])

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.haz_network:
                raw_subnet = cls.openstack('subnet delete ' + cls.NAME)
                raw_network = cls.openstack(
                    'network delete ' + cls.NETWORK_NAME
                )
                cls.assertOutput('', raw_subnet)
                cls.assertOutput('', raw_network)
        finally:
            super().tearDownClass()

    def test_ip_availability_list(self):
        """Test ip availability list"""
        cmd_output = self.openstack(
            'ip availability list',
            parse_output=True,
        )
        names = [x['Network Name'] for x in cmd_output]
        self.assertIn(self.NETWORK_NAME, names)

    def test_ip_availability_show(self):
        """Test ip availability show"""
        cmd_output = self.openstack(
            'ip availability show ' + self.NETWORK_NAME,
            parse_output=True,
        )
        self.assertEqual(
            self.NETWORK_NAME,
            cmd_output['network_name'],
        )

    def test_ip_availability_details(self):
        """Test the network-ip-availability-details extension fields"""
        if not self.is_extension_enabled('network-ip-availability-details'):
            self.skipTest("No network-ip-availability-details extension")

        cmd_output = self.openstack(
            'ip availability show ' + self.NETWORK_NAME,
            parse_output=True,
        )
        details = cmd_output['ip_availability_details']
        # 10.10.10.0/24 minus the network and broadcast addresses
        self.assertEqual(254, details['total_ips_in_subnet'])
        self.assertGreaterEqual(
            details['total_ips_in_subnet'],
            details['total_ips_in_allocation_pool'],
        )
        self.assertGreaterEqual(
            details['used_ips_in_subnet'],
            details['used_ips_in_allocation_pool'],
        )

        cmd_output = self.openstack(
            'ip availability list',
            parse_output=True,
        )
        network = next(
            x for x in cmd_output if x['Network Name'] == self.NETWORK_NAME
        )
        self.assertEqual(
            details['total_ips_in_subnet'], network['Total IPs in Subnet']
        )
        self.assertEqual(
            details['total_ips_in_allocation_pool'],
            network['Total IPs in Allocation Pool'],
        )
