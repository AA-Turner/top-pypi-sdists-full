"""
Type annotations for elb-proxy service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elb_proxy.client import ELBProxyClient
    from mypy_boto3_elb_proxy.waiter import (
        ProxyActiveWaiter,
        ProxyDeletedWaiter,
        ProxyUpdateCompleteWaiter,
    )

    session = Session()
    client: ELBProxyClient = session.client("elb-proxy")

    proxy_active_waiter: ProxyActiveWaiter = client.get_waiter("proxy_active")
    proxy_deleted_waiter: ProxyDeletedWaiter = client.get_waiter("proxy_deleted")
    proxy_update_complete_waiter: ProxyUpdateCompleteWaiter = client.get_waiter("proxy_update_complete")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetProxyRequestWaitExtraTypeDef,
    GetProxyRequestWaitTypeDef,
    GetProxyUpdateRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ProxyActiveWaiter", "ProxyDeletedWaiter", "ProxyUpdateCompleteWaiter")


class ProxyActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyActive.html#ELBProxy.Waiter.ProxyActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxyactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetProxyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyActive.html#ELBProxy.Waiter.ProxyActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxyactivewaiter)
        """


class ProxyDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyDeleted.html#ELBProxy.Waiter.ProxyDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxydeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetProxyRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyDeleted.html#ELBProxy.Waiter.ProxyDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxydeletedwaiter)
        """


class ProxyUpdateCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyUpdateComplete.html#ELBProxy.Waiter.ProxyUpdateComplete)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxyupdatecompletewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetProxyUpdateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/waiter/ProxyUpdateComplete.html#ELBProxy.Waiter.ProxyUpdateComplete.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/waiters/#proxyupdatecompletewaiter)
        """
