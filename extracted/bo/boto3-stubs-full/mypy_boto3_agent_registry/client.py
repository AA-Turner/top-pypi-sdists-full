"""
Type annotations for agent-registry service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_agent_registry.client import AgentRegistryClient

    session = Session()
    client: AgentRegistryClient = session.client("agent-registry")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListDiscoverableRegistryRecordsPaginator
from .type_defs import (
    BatchGetDiscoverableRegistryRecordRequestTypeDef,
    BatchGetDiscoverableRegistryRecordResponseTypeDef,
    ListDiscoverableRegistryRecordsRequestTypeDef,
    ListDiscoverableRegistryRecordsResponseTypeDef,
    SearchDiscoverableRegistryRecordsRequestTypeDef,
    SearchDiscoverableRegistryRecordsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AgentRegistryClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class AgentRegistryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry.html#AgentRegistry.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentRegistryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry.html#AgentRegistry.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#generate_presigned_url)
        """

    def batch_get_discoverable_registry_record(
        self, **kwargs: Unpack[BatchGetDiscoverableRegistryRecordRequestTypeDef]
    ) -> BatchGetDiscoverableRegistryRecordResponseTypeDef:
        """
        Retrieves multiple discoverable registry records by ID from a single registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/batch_get_discoverable_registry_record.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#batch_get_discoverable_registry_record)
        """

    def list_discoverable_registry_records(
        self, **kwargs: Unpack[ListDiscoverableRegistryRecordsRequestTypeDef]
    ) -> ListDiscoverableRegistryRecordsResponseTypeDef:
        """
        Lists the discoverable registry records in a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/list_discoverable_registry_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#list_discoverable_registry_records)
        """

    def search_discoverable_registry_records(
        self, **kwargs: Unpack[SearchDiscoverableRegistryRecordsRequestTypeDef]
    ) -> SearchDiscoverableRegistryRecordsResponseTypeDef:
        """
        Searches the discoverable registry records in a registry using a natural
        language query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/search_discoverable_registry_records.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#search_discoverable_registry_records)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_discoverable_registry_records"]
    ) -> ListDiscoverableRegistryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_agent_registry/client/#get_paginator)
        """
