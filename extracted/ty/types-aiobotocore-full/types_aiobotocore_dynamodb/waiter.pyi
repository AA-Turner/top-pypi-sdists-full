"""
Type annotations for dynamodb service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dynamodb.client import DynamoDBClient
    from types_aiobotocore_dynamodb.waiter import (
        ContributorInsightsEnabledWaiter,
        ExportCompletedWaiter,
        ImportCompletedWaiter,
        KinesisStreamingDestinationActiveWaiter,
        TableExistsWaiter,
        TableNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("dynamodb") as client:
        client: DynamoDBClient

        contributor_insights_enabled_waiter: ContributorInsightsEnabledWaiter = client.get_waiter("contributor_insights_enabled")
        export_completed_waiter: ExportCompletedWaiter = client.get_waiter("export_completed")
        import_completed_waiter: ImportCompletedWaiter = client.get_waiter("import_completed")
        kinesis_streaming_destination_active_waiter: KinesisStreamingDestinationActiveWaiter = client.get_waiter("kinesis_streaming_destination_active")
        table_exists_waiter: TableExistsWaiter = client.get_waiter("table_exists")
        table_not_exists_waiter: TableNotExistsWaiter = client.get_waiter("table_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeContributorInsightsInputWaitTypeDef,
    DescribeExportInputWaitTypeDef,
    DescribeImportInputWaitTypeDef,
    DescribeKinesisStreamingDestinationInputWaitTypeDef,
    DescribeTableInputWaitExtraTypeDef,
    DescribeTableInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ContributorInsightsEnabledWaiter",
    "ExportCompletedWaiter",
    "ImportCompletedWaiter",
    "KinesisStreamingDestinationActiveWaiter",
    "TableExistsWaiter",
    "TableNotExistsWaiter",
)

class ContributorInsightsEnabledWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ContributorInsightsEnabled.html#DynamoDB.Waiter.ContributorInsightsEnabled)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#contributorinsightsenabledwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeContributorInsightsInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ContributorInsightsEnabled.html#DynamoDB.Waiter.ContributorInsightsEnabled.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#contributorinsightsenabledwaiter)
        """

class ExportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ExportCompleted.html#DynamoDB.Waiter.ExportCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#exportcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ExportCompleted.html#DynamoDB.Waiter.ExportCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#exportcompletedwaiter)
        """

class ImportCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ImportCompleted.html#DynamoDB.Waiter.ImportCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#importcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImportInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ImportCompleted.html#DynamoDB.Waiter.ImportCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#importcompletedwaiter)
        """

class KinesisStreamingDestinationActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/KinesisStreamingDestinationActive.html#DynamoDB.Waiter.KinesisStreamingDestinationActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#kinesisstreamingdestinationactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeKinesisStreamingDestinationInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/KinesisStreamingDestinationActive.html#DynamoDB.Waiter.KinesisStreamingDestinationActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#kinesisstreamingdestinationactivewaiter)
        """

class TableExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tableexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tableexistswaiter)
        """

class TableNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tablenotexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tablenotexistswaiter)
        """
