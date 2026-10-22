"""
Type annotations for network-firewall service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_network_firewall.client import NetworkFirewallClient
    from mypy_boto3_network_firewall.waiter import (
        FirewallPolicyActiveWaiter,
    )

    session = Session()
    client: NetworkFirewallClient = session.client("network-firewall")

    firewall_policy_active_waiter: FirewallPolicyActiveWaiter = client.get_waiter("firewall_policy_active")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeFirewallPolicyRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("FirewallPolicyActiveWaiter",)

class FirewallPolicyActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/waiter/FirewallPolicyActive.html#NetworkFirewall.Waiter.FirewallPolicyActive)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/waiters/#firewallpolicyactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFirewallPolicyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/waiter/FirewallPolicyActive.html#NetworkFirewall.Waiter.FirewallPolicyActive.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_network_firewall/waiters/#firewallpolicyactivewaiter)
        """
