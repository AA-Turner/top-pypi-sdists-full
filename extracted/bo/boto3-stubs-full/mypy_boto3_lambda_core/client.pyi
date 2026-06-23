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
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListNetworkConnectorsPaginator
from .type_defs import (
    CreateNetworkConnectorRequestTypeDef,
    CreateNetworkConnectorResponseTypeDef,
    DeleteNetworkConnectorRequestTypeDef,
    DeleteNetworkConnectorResponseTypeDef,
    GetNetworkConnectorRequestTypeDef,
    GetNetworkConnectorResponseTypeDef,
    ListNetworkConnectorsRequestTypeDef,
    ListNetworkConnectorsResponseTypeDef,
    UpdateNetworkConnectorRequestTypeDef,
    UpdateNetworkConnectorResponseTypeDef,
)

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

    def delete_network_connector(
        self, **kwargs: Unpack[DeleteNetworkConnectorRequestTypeDef]
    ) -> DeleteNetworkConnectorResponseTypeDef:
        """
        Initiates deletion of a network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/delete_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#delete_network_connector)
        """

    def get_network_connector(
        self, **kwargs: Unpack[GetNetworkConnectorRequestTypeDef]
    ) -> GetNetworkConnectorResponseTypeDef:
        """
        Retrieves the current configuration, state, and metadata of a network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_network_connector)
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

    def update_network_connector(
        self, **kwargs: Unpack[UpdateNetworkConnectorRequestTypeDef]
    ) -> UpdateNetworkConnectorResponseTypeDef:
        """
        Updates the VPC configuration or operator role of an existing network connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/update_network_connector.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#update_network_connector)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_network_connectors"]
    ) -> ListNetworkConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/client/#get_paginator)
        """
