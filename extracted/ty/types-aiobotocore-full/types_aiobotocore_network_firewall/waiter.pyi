"""
Type annotations for network-firewall service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_network_firewall.client import NetworkFirewallClient
    from types_aiobotocore_network_firewall.waiter import (
        FirewallPolicyActiveWaiter,
    )

    session = get_session()
    async with session.create_client("network-firewall") as client:
        client: NetworkFirewallClient

        firewall_policy_active_waiter: FirewallPolicyActiveWaiter = client.get_waiter("firewall_policy_active")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeFirewallPolicyRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("FirewallPolicyActiveWaiter",)

class FirewallPolicyActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/waiter/FirewallPolicyActive.html#NetworkFirewall.Waiter.FirewallPolicyActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/waiters/#firewallpolicyactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFirewallPolicyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-firewall/waiter/FirewallPolicyActive.html#NetworkFirewall.Waiter.FirewallPolicyActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_firewall/waiters/#firewallpolicyactivewaiter)
        """
