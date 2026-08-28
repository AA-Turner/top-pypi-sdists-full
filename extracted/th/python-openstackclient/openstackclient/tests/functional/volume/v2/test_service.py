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

from openstackclient.tests.functional.volume.v2 import common


class VolumeServiceTests(common.BaseVolumeTests):
    """Functional tests for volume service."""

    def test_volume_service_list(self):
        cmd_output = self.openstack('volume service list', parse_output=True)

        # Get the nonredundant services and hosts
        services = list({x['Binary'] for x in cmd_output})
        hosts = list({x['Host'] for x in cmd_output})

        # Test volume service list --service
        cmd_output = self.openstack(
            'volume service list ' + '--service ' + services[0],
            parse_output=True,
        )
        for x in cmd_output:
            self.assertEqual(services[0], x['Binary'])

        # Test volume service list --host
        cmd_output = self.openstack(
            'volume service list ' + '--host ' + hosts[0],
            parse_output=True,
        )
        for x in cmd_output:
            self.assertIn(hosts[0], x['Host'])
