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


from openstackclient.tests.functional.volume.v3 import common


class VolumeServiceTests(common.BaseVolumeTests):
    """Functional tests for 'openstack volume service'."""

    def test_volume_service(self):
        """Verify listing works and host/service filters narrow results."""

        # List all services and ensure we have at least one cinder-volume
        rows = self.openstack('volume service list', parse_output=True)
        self.assertTrue(rows, 'no volume services returned')

        # Pick one row for filter checks
        row = rows[0]
        host = row['Host']
        binary = row['Binary']
        self.assertIsNotNone(host)
        self.assertIsNotNone(binary)

        # Filter by host+service should return matching entries only
        filtered = self.openstack(
            'volume service list --host ' + host + ' --service ' + binary,
            parse_output=True,
        )
        self.assertTrue(filtered, 'filtered list is empty')
        for r in filtered:
            self.assertEqual(host, r['Host'])
            self.assertEqual(binary, r['Binary'])

        # --long should include additional details but at least must succeed
        long_rows = self.openstack(
            'volume service list --long --host '
            + host
            + ' --service '
            + binary,
            parse_output=True,
        )
        self.assertEqual(1, len(long_rows))
        # Ensure disabled reason column exists (value may be None)
        lr0 = long_rows[0]
        self.assertIn('Disabled Reason', lr0)
