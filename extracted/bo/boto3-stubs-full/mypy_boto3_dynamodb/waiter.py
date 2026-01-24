"""
Type annotations for dynamodb service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dynamodb.client import DynamoDBClient
    from mypy_boto3_dynamodb.waiter import (
        ContributorInsightsEnabledWaiter,
        ExportCompletedWaiter,
        ImportCompletedWaiter,
        KinesisStreamingDestinationActiveWaiter,
        TableExistsWaiter,
        TableNotExistsWaiter,
    )

    session = Session()
    client: DynamoDBClient = session.client("dynamodb")

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

from botocore.waiter import Waiter

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


class ContributorInsightsEnabledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ContributorInsightsEnabled.html#DynamoDB.Waiter.ContributorInsightsEnabled)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#contributorinsightsenabledwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeContributorInsightsInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ContributorInsightsEnabled.html#DynamoDB.Waiter.ContributorInsightsEnabled.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#contributorinsightsenabledwaiter)
        """


class ExportCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ExportCompleted.html#DynamoDB.Waiter.ExportCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#exportcompletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ExportCompleted.html#DynamoDB.Waiter.ExportCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#exportcompletedwaiter)
        """


class ImportCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ImportCompleted.html#DynamoDB.Waiter.ImportCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#importcompletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImportInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/ImportCompleted.html#DynamoDB.Waiter.ImportCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#importcompletedwaiter)
        """


class KinesisStreamingDestinationActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/KinesisStreamingDestinationActive.html#DynamoDB.Waiter.KinesisStreamingDestinationActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#kinesisstreamingdestinationactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeKinesisStreamingDestinationInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/KinesisStreamingDestinationActive.html#DynamoDB.Waiter.KinesisStreamingDestinationActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#kinesisstreamingdestinationactivewaiter)
        """


class TableExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#tableexistswaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#tableexistswaiter)
        """


class TableNotExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#tablenotexistswaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/waiters/#tablenotexistswaiter)
        """
