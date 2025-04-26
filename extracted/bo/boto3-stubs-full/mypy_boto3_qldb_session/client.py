"""
Type annotations for qldb-session service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_qldb_session.client import QLDBSessionClient

    session = Session()
    client: QLDBSessionClient = session.client("qldb-session")
    ```
"""

from __future__ import annotations

import sys
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import SendCommandRequestTypeDef, SendCommandResultTypeDef

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("QLDBSessionClient",)


class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    CapacityExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidSessionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OccConflictException: Type[BotocoreClientError]
    RateExceededException: Type[BotocoreClientError]


class QLDBSessionClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QLDBSessionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session.html#QLDBSession.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/#generate_presigned_url)
        """

    def send_command(self, **kwargs: Unpack[SendCommandRequestTypeDef]) -> SendCommandResultTypeDef:
        """
        Sends a command to an Amazon QLDB ledger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qldb-session/client/send_command.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_qldb_session/client/#send_command)
        """
