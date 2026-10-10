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

"""Cloud action implementations"""

import argparse

from openstackclient import command
from openstackclient.i18n import _


class DeleteCloudCache(command.Command):
    _description = _("Delete the authentication cached for a cloud")

    # Authenticating in order to throw away the credential that would have
    # been used to do it makes no sense, and would defeat the point when the
    # cached credential is the broken thing being cleared.
    auth_required = False

    def get_parser(self, prog_name: str) -> argparse.ArgumentParser:
        parser = super().get_parser(prog_name)
        parser.epilog = _(
            "Authentication is only cached when the 'cache.auth' setting is "
            "enabled in clouds.yaml. Without it there is nothing stored and "
            "nothing to delete."
        )
        return parser

    def take_action(self, parsed_args: argparse.Namespace) -> None:
        self.app.client_manager._cli_options.clear_auth_cache()
