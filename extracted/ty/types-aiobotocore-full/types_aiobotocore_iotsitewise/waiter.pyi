"""
Type annotations for iotsitewise service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotsitewise.client import IoTSiteWiseClient
    from types_aiobotocore_iotsitewise.waiter import (
        AssetActiveWaiter,
        AssetModelActiveWaiter,
        AssetModelNotExistsWaiter,
        AssetNotExistsWaiter,
        PortalActiveWaiter,
        PortalNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("iotsitewise") as client:
        client: IoTSiteWiseClient

        asset_active_waiter: AssetActiveWaiter = client.get_waiter("asset_active")
        asset_model_active_waiter: AssetModelActiveWaiter = client.get_waiter("asset_model_active")
        asset_model_not_exists_waiter: AssetModelNotExistsWaiter = client.get_waiter("asset_model_not_exists")
        asset_not_exists_waiter: AssetNotExistsWaiter = client.get_waiter("asset_not_exists")
        portal_active_waiter: PortalActiveWaiter = client.get_waiter("portal_active")
        portal_not_exists_waiter: PortalNotExistsWaiter = client.get_waiter("portal_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeAssetModelRequestWaitExtraTypeDef,
    DescribeAssetModelRequestWaitTypeDef,
    DescribeAssetRequestWaitExtraTypeDef,
    DescribeAssetRequestWaitTypeDef,
    DescribePortalRequestWaitExtraTypeDef,
    DescribePortalRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AssetActiveWaiter",
    "AssetModelActiveWaiter",
    "AssetModelNotExistsWaiter",
    "AssetNotExistsWaiter",
    "PortalActiveWaiter",
    "PortalNotExistsWaiter",
)

class AssetActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetActive.html#IoTSiteWise.Waiter.AssetActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssetRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetActive.html#IoTSiteWise.Waiter.AssetActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetactivewaiter)
        """

class AssetModelActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetModelActive.html#IoTSiteWise.Waiter.AssetModelActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetmodelactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssetModelRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetModelActive.html#IoTSiteWise.Waiter.AssetModelActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetmodelactivewaiter)
        """

class AssetModelNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetModelNotExists.html#IoTSiteWise.Waiter.AssetModelNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetmodelnotexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssetModelRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetModelNotExists.html#IoTSiteWise.Waiter.AssetModelNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetmodelnotexistswaiter)
        """

class AssetNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetNotExists.html#IoTSiteWise.Waiter.AssetNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetnotexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssetRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/AssetNotExists.html#IoTSiteWise.Waiter.AssetNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#assetnotexistswaiter)
        """

class PortalActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/PortalActive.html#IoTSiteWise.Waiter.PortalActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#portalactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePortalRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/PortalActive.html#IoTSiteWise.Waiter.PortalActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#portalactivewaiter)
        """

class PortalNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/PortalNotExists.html#IoTSiteWise.Waiter.PortalNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#portalnotexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePortalRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsitewise/waiter/PortalNotExists.html#IoTSiteWise.Waiter.PortalNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/waiters/#portalnotexistswaiter)
        """
