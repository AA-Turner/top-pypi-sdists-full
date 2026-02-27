"""
Pro plugin hooks for the LocalStack CLI.

These hooks are executed on the host machine when running CLI commands like `localstack start`.
They handle license activation, container configuration, and extension developer mode.

Note: This file was extracted from localstack-pro-core/localstack/pro/core/plugins.py
and rewritten to contain only CLI-relevant functionality.
"""

from __future__ import annotations

import logging
import os

from localstack_cli import config as localstack_config
from localstack_cli.config import HostAndPort
from localstack_cli.pro.core import config as pro_config
from localstack_cli.pro.core.bootstrap import licensingv2
from localstack_cli.runtime import hooks
from localstack_cli.runtime.exceptions import LocalstackExit
from localstack_cli.utils.bootstrap import Container

LOG = logging.getLogger(__name__)


def modify_gateway_listen_config(cfg):
    """
    Modifies the localstack config to additionally listen to port 443.
    Needs to be called before any edge URLs are resolved using the config.
    """
    if os.getenv("GATEWAY_LISTEN") is None:
        host = "0.0.0.0" if localstack_config.in_docker() else "127.0.0.1"
        cfg.GATEWAY_LISTEN.append(HostAndPort(host=host, port=443))


@hooks.prepare_host(priority=200)
def patch_community_pro_detection():
    """This is currently needed to make localstack core aware of the `localstack auth set-token`
    functionality, where we set the key into the ``~/.localstack/auth.json`` file that community does not
    yet know about. ``is_api_key_configured`` is used in the LocalStack CLI to determine whether to start
    the localstack or localstack-pro container image."""
    from localstack_cli.utils import bootstrap

    bootstrap.is_auth_token_configured = pro_config.is_auth_token_configured


@hooks.prepare_host(priority=100, should_load=pro_config.ACTIVATE_PRO)
def activate_pro_key_on_host():
    """Activate license on host (needed for DNS forward and EC2 daemon)."""
    try:
        licensingv2.get_licensed_environment().activate()
    except licensingv2.LicensingError as e:
        raise LocalstackExit(reason=e.get_user_friendly(), code=55)


@hooks.configure_localstack_container(priority=10, should_load=pro_config.ACTIVATE_PRO)
def configure_pro_container(container: Container):
    """Configure the LocalStack container for pro features."""
    modify_gateway_listen_config(localstack_config)
    container.configure(licensingv2.configure_container_licensing)


@hooks.prepare_host(should_load=pro_config.ACTIVATE_PRO and pro_config.EXTENSION_DEV_MODE)
def configure_extensions_dev_host():
    """Load extension directories from ~/.localstack/extensions-dev.json."""
    from localstack_cli.pro.core.bootstrap.extensions.bootstrap import run_on_configure_host_hook

    run_on_configure_host_hook()


@hooks.configure_localstack_container(
    should_load=pro_config.ACTIVATE_PRO and pro_config.EXTENSION_DEV_MODE
)
def configure_extensions_dev_container(container: Container):
    """Configure container for extension developer mode."""
    from localstack_cli.pro.core.bootstrap.extensions.bootstrap import (
        run_on_configure_localstack_container_hook,
    )

    run_on_configure_localstack_container_hook(container)
