"""
Type annotations for rds-data service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_rds_data.client import RDSDataServiceClient

    session = Session()
    client: RDSDataServiceClient = session.client("rds-data")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    BatchExecuteStatementRequestTypeDef,
    BatchExecuteStatementResponseTypeDef,
    BeginTransactionRequestTypeDef,
    BeginTransactionResponseTypeDef,
    CommitTransactionRequestTypeDef,
    CommitTransactionResponseTypeDef,
    ExecuteSqlRequestTypeDef,
    ExecuteSqlResponseTypeDef,
    ExecuteStatementRequestTypeDef,
    ExecuteStatementResponseTypeDef,
    RollbackTransactionRequestTypeDef,
    RollbackTransactionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("RDSDataServiceClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    DatabaseErrorException: type[BotocoreClientError]
    DatabaseNotFoundException: type[BotocoreClientError]
    DatabaseResumingException: type[BotocoreClientError]
    DatabaseUnavailableException: type[BotocoreClientError]
    ForbiddenException: type[BotocoreClientError]
    HttpEndpointNotEnabledException: type[BotocoreClientError]
    InternalServerErrorException: type[BotocoreClientError]
    InvalidResourceStateException: type[BotocoreClientError]
    InvalidSecretException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    SecretsErrorException: type[BotocoreClientError]
    ServiceUnavailableError: type[BotocoreClientError]
    StatementTimeoutException: type[BotocoreClientError]
    TransactionNotFoundException: type[BotocoreClientError]
    UnsupportedResultException: type[BotocoreClientError]

class RDSDataServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RDSDataServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data.html#RDSDataService.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#generate_presigned_url)
        """

    def batch_execute_statement(
        self, **kwargs: Unpack[BatchExecuteStatementRequestTypeDef]
    ) -> BatchExecuteStatementResponseTypeDef:
        """
        Runs a batch SQL statement over an array of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/batch_execute_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#batch_execute_statement)
        """

    def begin_transaction(
        self, **kwargs: Unpack[BeginTransactionRequestTypeDef]
    ) -> BeginTransactionResponseTypeDef:
        """
        Starts a SQL transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/begin_transaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#begin_transaction)
        """

    def commit_transaction(
        self, **kwargs: Unpack[CommitTransactionRequestTypeDef]
    ) -> CommitTransactionResponseTypeDef:
        """
        Ends a SQL transaction started with the <code>BeginTransaction</code> operation
        and commits the changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/commit_transaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#commit_transaction)
        """

    def execute_sql(self, **kwargs: Unpack[ExecuteSqlRequestTypeDef]) -> ExecuteSqlResponseTypeDef:
        """
        Runs one or more SQL statements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_sql.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#execute_sql)
        """

    def execute_statement(
        self, **kwargs: Unpack[ExecuteStatementRequestTypeDef]
    ) -> ExecuteStatementResponseTypeDef:
        """
        Runs a SQL statement against a database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/execute_statement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#execute_statement)
        """

    def rollback_transaction(
        self, **kwargs: Unpack[RollbackTransactionRequestTypeDef]
    ) -> RollbackTransactionResponseTypeDef:
        """
        Performs a rollback of a transaction.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds-data/client/rollback_transaction.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds_data/client/#rollback_transaction)
        """
