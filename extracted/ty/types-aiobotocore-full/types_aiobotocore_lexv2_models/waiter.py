"""
Type annotations for lexv2-models service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lexv2_models.client import LexModelsV2Client
    from types_aiobotocore_lexv2_models.waiter import (
        BotAliasAvailableWaiter,
        BotAvailableWaiter,
        BotExportCompletedWaiter,
        BotImportCompletedWaiter,
        BotLocaleBuiltWaiter,
        BotLocaleCreatedWaiter,
        BotLocaleExpressTestingAvailableWaiter,
        BotVersionAvailableWaiter,
    )

    session = get_session()
    async with session.create_client("lexv2-models") as client:
        client: LexModelsV2Client

        bot_alias_available_waiter: BotAliasAvailableWaiter = client.get_waiter("bot_alias_available")
        bot_available_waiter: BotAvailableWaiter = client.get_waiter("bot_available")
        bot_export_completed_waiter: BotExportCompletedWaiter = client.get_waiter("bot_export_completed")
        bot_import_completed_waiter: BotImportCompletedWaiter = client.get_waiter("bot_import_completed")
        bot_locale_built_waiter: BotLocaleBuiltWaiter = client.get_waiter("bot_locale_built")
        bot_locale_created_waiter: BotLocaleCreatedWaiter = client.get_waiter("bot_locale_created")
        bot_locale_express_testing_available_waiter: BotLocaleExpressTestingAvailableWaiter = client.get_waiter("bot_locale_express_testing_available")
        bot_version_available_waiter: BotVersionAvailableWaiter = client.get_waiter("bot_version_available")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeBotAliasRequestWaitTypeDef,
    DescribeBotLocaleRequestWaitExtraExtraTypeDef,
    DescribeBotLocaleRequestWaitExtraTypeDef,
    DescribeBotLocaleRequestWaitTypeDef,
    DescribeBotRequestWaitTypeDef,
    DescribeBotVersionRequestWaitTypeDef,
    DescribeExportRequestWaitTypeDef,
    DescribeImportRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "BotAliasAvailableWaiter",
    "BotAvailableWaiter",
    "BotExportCompletedWaiter",
    "BotImportCompletedWaiter",
    "BotLocaleBuiltWaiter",
    "BotLocaleCreatedWaiter",
    "BotLocaleExpressTestingAvailableWaiter",
    "BotVersionAvailableWaiter",
)


class BotAliasAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotAliasAvailable.html#LexModelsV2.Waiter.BotAliasAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botaliasavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotAliasRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotAliasAvailable.html#LexModelsV2.Waiter.BotAliasAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botaliasavailablewaiter)
        """


class BotAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotAvailable.html#LexModelsV2.Waiter.BotAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotAvailable.html#LexModelsV2.Waiter.BotAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botavailablewaiter)
        """


class BotExportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotExportCompleted.html#LexModelsV2.Waiter.BotExportCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botexportcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotExportCompleted.html#LexModelsV2.Waiter.BotExportCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botexportcompletedwaiter)
        """


class BotImportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotImportCompleted.html#LexModelsV2.Waiter.BotImportCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botimportcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotImportCompleted.html#LexModelsV2.Waiter.BotImportCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botimportcompletedwaiter)
        """


class BotLocaleBuiltWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleBuilt.html#LexModelsV2.Waiter.BotLocaleBuilt)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalebuiltwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotLocaleRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleBuilt.html#LexModelsV2.Waiter.BotLocaleBuilt.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalebuiltwaiter)
        """


class BotLocaleCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleCreated.html#LexModelsV2.Waiter.BotLocaleCreated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalecreatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotLocaleRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleCreated.html#LexModelsV2.Waiter.BotLocaleCreated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocalecreatedwaiter)
        """


class BotLocaleExpressTestingAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleExpressTestingAvailable.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotLocaleRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotLocaleExpressTestingAvailable.html#LexModelsV2.Waiter.BotLocaleExpressTestingAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botlocaleexpresstestingavailablewaiter)
        """


class BotVersionAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotVersionAvailable.html#LexModelsV2.Waiter.BotVersionAvailable)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botversionavailablewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotVersionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/waiter/BotVersionAvailable.html#LexModelsV2.Waiter.BotVersionAvailable.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/waiters/#botversionavailablewaiter)
        """
