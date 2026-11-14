"""
Type annotations for lambda-core service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lambda_core.client import LambdaCoreClient

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListNetworkConnectorsPaginator,
    ListNetworkConnectorVersionsPaginator,
    ListRuntimeAliasesPaginator,
    ListRuntimesPaginator,
    ListRuntimeVersionsPaginator,
)
from .type_defs import (
    CreateNetworkConnectorRequestTypeDef,
    CreateNetworkConnectorResponseTypeDef,
    CreateRuntimeAliasRequestTypeDef,
    CreateRuntimeAliasResponseTypeDef,
    CreateRuntimeRequestTypeDef,
    CreateRuntimeResponseTypeDef,
    CreateRuntimeVersionRequestTypeDef,
    CreateRuntimeVersionResponseTypeDef,
    DeleteNetworkConnectorRequestTypeDef,
    DeleteNetworkConnectorResponseTypeDef,
    DeleteRuntimeAliasRequestTypeDef,
    DeleteRuntimeRequestTypeDef,
    DeleteRuntimeVersionRequestTypeDef,
    GetNetworkConnectorRequestTypeDef,
    GetNetworkConnectorResponseTypeDef,
    GetRuntimeAliasRequestTypeDef,
    GetRuntimeAliasResponseTypeDef,
    GetRuntimeRequestTypeDef,
    GetRuntimeResponseTypeDef,
    GetRuntimeVersionRequestTypeDef,
    GetRuntimeVersionResponseTypeDef,
    ListNetworkConnectorsRequestTypeDef,
    ListNetworkConnectorsResponseTypeDef,
    ListNetworkConnectorVersionsRequestTypeDef,
    ListNetworkConnectorVersionsResponseTypeDef,
    ListRuntimeAliasesRequestTypeDef,
    ListRuntimeAliasesResponseTypeDef,
    ListRuntimesRequestTypeDef,
    ListRuntimesResponseTypeDef,
    ListRuntimeVersionsRequestTypeDef,
    ListRuntimeVersionsResponseTypeDef,
    RestoreRuntimeRequestTypeDef,
    RestoreRuntimeResponseTypeDef,
    UpdateNetworkConnectorRequestTypeDef,
    UpdateNetworkConnectorResponseTypeDef,
    UpdateRuntimeAliasRequestTypeDef,
    UpdateRuntimeAliasResponseTypeDef,
    UpdateRuntimeRequestTypeDef,
    UpdateRuntimeResponseTypeDef,
    UpdateRuntimeVersionRequestTypeDef,
    UpdateRuntimeVersionResponseTypeDef,
)
from .waiter import RuntimeAliasActiveWaiter, RuntimeVersionActiveWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("LambdaCoreClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    NetworkConnectorLimitExceededException: type[BotocoreClientError]
    ResourceConflictException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]


class LambdaCoreClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core.html#LambdaCore.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LambdaCoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core.html#LambdaCore.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#generate_presigned_url)
        """

    def create_network_connector(
        self, **kwargs: Unpack[CreateNetworkConnectorRequestTypeDef]
    ) -> CreateNetworkConnectorResponseTypeDef:
        """
        Creates a network connector that enables Lambda compute resources to route
        outbound traffic through your Amazon VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/create_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#create_network_connector)
        """

    def create_runtime(
        self, **kwargs: Unpack[CreateRuntimeRequestTypeDef]
    ) -> CreateRuntimeResponseTypeDef:
        """
        Creates a customer-managed runtime, a resource providing a centrally managed
        execution environment for your Lambda functions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/create_runtime.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#create_runtime)
        """

    def create_runtime_alias(
        self, **kwargs: Unpack[CreateRuntimeAliasRequestTypeDef]
    ) -> CreateRuntimeAliasResponseTypeDef:
        """
        Creates a new customer-managed runtime alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/create_runtime_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#create_runtime_alias)
        """

    def create_runtime_version(
        self, **kwargs: Unpack[CreateRuntimeVersionRequestTypeDef]
    ) -> CreateRuntimeVersionResponseTypeDef:
        """
        Creates a new runtime version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/create_runtime_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#create_runtime_version)
        """

    def delete_network_connector(
        self, **kwargs: Unpack[DeleteNetworkConnectorRequestTypeDef]
    ) -> DeleteNetworkConnectorResponseTypeDef:
        """
        Initiates deletion of a network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/delete_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#delete_network_connector)
        """

    def delete_runtime(self, **kwargs: Unpack[DeleteRuntimeRequestTypeDef]) -> dict[str, Any]:
        """
        Schedules a customer-managed runtime to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/delete_runtime.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#delete_runtime)
        """

    def delete_runtime_alias(
        self, **kwargs: Unpack[DeleteRuntimeAliasRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Schedules a runtime alias to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/delete_runtime_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#delete_runtime_alias)
        """

    def delete_runtime_version(
        self, **kwargs: Unpack[DeleteRuntimeVersionRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Schedules a runtime version to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/delete_runtime_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#delete_runtime_version)
        """

    def get_network_connector(
        self, **kwargs: Unpack[GetNetworkConnectorRequestTypeDef]
    ) -> GetNetworkConnectorResponseTypeDef:
        """
        Retrieves the current configuration, state, and metadata of a network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_network_connector)
        """

    def get_runtime(self, **kwargs: Unpack[GetRuntimeRequestTypeDef]) -> GetRuntimeResponseTypeDef:
        """
        Retrieves the configuration and metadata of a runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_runtime.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_runtime)
        """

    def get_runtime_alias(
        self, **kwargs: Unpack[GetRuntimeAliasRequestTypeDef]
    ) -> GetRuntimeAliasResponseTypeDef:
        """
        Retrieves the configuration, state, and metadata of a runtime alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_runtime_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_runtime_alias)
        """

    def get_runtime_version(
        self, **kwargs: Unpack[GetRuntimeVersionRequestTypeDef]
    ) -> GetRuntimeVersionResponseTypeDef:
        """
        Retrieves the configuration, state, and metadata of a runtime version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_runtime_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_runtime_version)
        """

    def list_network_connector_versions(
        self, **kwargs: Unpack[ListNetworkConnectorVersionsRequestTypeDef]
    ) -> ListNetworkConnectorVersionsResponseTypeDef:
        """
        Returns a paginated list of the versions of a network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/list_network_connector_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#list_network_connector_versions)
        """

    def list_network_connectors(
        self, **kwargs: Unpack[ListNetworkConnectorsRequestTypeDef]
    ) -> ListNetworkConnectorsResponseTypeDef:
        """
        Returns a paginated list of network connectors in your account for the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/list_network_connectors.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#list_network_connectors)
        """

    def list_runtime_aliases(
        self, **kwargs: Unpack[ListRuntimeAliasesRequestTypeDef]
    ) -> ListRuntimeAliasesResponseTypeDef:
        """
        Returns a paginated list of aliases for the specified runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/list_runtime_aliases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#list_runtime_aliases)
        """

    def list_runtime_versions(
        self, **kwargs: Unpack[ListRuntimeVersionsRequestTypeDef]
    ) -> ListRuntimeVersionsResponseTypeDef:
        """
        Returns a paginated list of versions for the specified runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/list_runtime_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#list_runtime_versions)
        """

    def list_runtimes(
        self, **kwargs: Unpack[ListRuntimesRequestTypeDef]
    ) -> ListRuntimesResponseTypeDef:
        """
        Returns a paginated list of runtimes in your account for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/list_runtimes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#list_runtimes)
        """

    def restore_runtime(
        self, **kwargs: Unpack[RestoreRuntimeRequestTypeDef]
    ) -> RestoreRuntimeResponseTypeDef:
        """
        Cancels a pending scheduled deletion, returning the resource to the ACTIVE
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/restore_runtime.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#restore_runtime)
        """

    def update_network_connector(
        self, **kwargs: Unpack[UpdateNetworkConnectorRequestTypeDef]
    ) -> UpdateNetworkConnectorResponseTypeDef:
        """
        Updates the VPC configuration or operator role of an existing network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/update_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#update_network_connector)
        """

    def update_runtime(
        self, **kwargs: Unpack[UpdateRuntimeRequestTypeDef]
    ) -> UpdateRuntimeResponseTypeDef:
        """
        Updates the properties of an existing customer-managed runtime, such as its
        description, license information, or lifecycle information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/update_runtime.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#update_runtime)
        """

    def update_runtime_alias(
        self, **kwargs: Unpack[UpdateRuntimeAliasRequestTypeDef]
    ) -> UpdateRuntimeAliasResponseTypeDef:
        """
        Updates an existing runtime alias to point to a different runtime version or to
        change its description or lifecycle information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/update_runtime_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#update_runtime_alias)
        """

    def update_runtime_version(
        self, **kwargs: Unpack[UpdateRuntimeVersionRequestTypeDef]
    ) -> UpdateRuntimeVersionResponseTypeDef:
        """
        Updates the runtime version release notes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/update_runtime_version.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#update_runtime_version)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_network_connector_versions"]
    ) -> ListNetworkConnectorVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_network_connectors"]
    ) -> ListNetworkConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_runtime_aliases"]
    ) -> ListRuntimeAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_runtime_versions"]
    ) -> ListRuntimeVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_runtimes"]
    ) -> ListRuntimesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["runtime_alias_active"]
    ) -> RuntimeAliasActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["runtime_version_active"]
    ) -> RuntimeVersionActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_waiter.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_waiter)
        """
