# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import os

from qctrlclient.auth import CliAuth

from .globals import global_value

_DEFAULT_API_URL = "https://federation-service.q-ctrl.com"
_DEFAULT_OIDC_URL = "https://id.q-ctrl.com"


def get_default_api_url() -> str:
    """
    Return the default API URL. Can be overridden by
    setting the `QCTRL_API_URL` environment variable.
    """
    return os.getenv("QCTRL_API_URL", _DEFAULT_API_URL)


def get_default_oidc_url() -> str:
    """
    Return the default OIDC URL. Can be overridden by
    setting the `QCTRL_OIDC_URL` environment variable.
    """
    return os.getenv("QCTRL_OIDC_URL", _DEFAULT_OIDC_URL)


@global_value("DEFAULT_CLI_AUTH")
def get_default_cli_auth() -> CliAuth:
    """Return default `CliAuth` object."""
    url = get_default_oidc_url()
    return CliAuth(url)
