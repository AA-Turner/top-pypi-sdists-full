#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from unittest import mock

import fixtures

from openstackclient.common import cloud
from openstackclient.tests.unit import utils


class TestDeleteCloudCache(utils.TestCommand):
    def setUp(self):
        super().setUp()

        self.cmd = cloud.DeleteCloudCache(self.app, None)
        # The fake client manager has no cloud region of its own.
        self.cloud_region = self.useFixture(
            fixtures.MockPatchObject(
                self.app.client_manager,
                '_cli_options',
                mock.Mock(),
                create=True,
            )
        ).mock

    def test_delete(self):
        parsed_args = self.check_parser(self.cmd, [], [])

        self.cmd.take_action(parsed_args)

        self.cloud_region.clear_auth_cache.assert_called_once_with()

    def test_does_not_authenticate(self):
        # Authenticating in order to discard the credential that would be used
        # to do it is pointless, and impossible when that credential is the
        # broken thing being cleared.
        self.assertFalse(self.cmd.auth_required)
