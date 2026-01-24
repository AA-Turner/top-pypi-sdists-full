"""
Type annotations for lex-runtime service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lex_runtime.client import LexRuntimeServiceClient

    session = Session()
    client: LexRuntimeServiceClient = session.client("lex-runtime")
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
    DeleteSessionRequestTypeDef,
    DeleteSessionResponseTypeDef,
    GetSessionRequestTypeDef,
    GetSessionResponseTypeDef,
    PostContentRequestTypeDef,
    PostContentResponseTypeDef,
    PostTextRequestTypeDef,
    PostTextResponseTypeDef,
    PutSessionRequestTypeDef,
    PutSessionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("LexRuntimeServiceClient",)

class Exceptions(BaseClientExceptions):
    BadGatewayException: type[BotocoreClientError]
    BadRequestException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DependencyFailedException: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    LoopDetectedException: type[BotocoreClientError]
    NotAcceptableException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    RequestTimeoutException: type[BotocoreClientError]
    UnsupportedMediaTypeException: type[BotocoreClientError]

class LexRuntimeServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LexRuntimeServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html#LexRuntimeService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#generate_presigned_url)
        """

    def delete_session(
        self, **kwargs: Unpack[DeleteSessionRequestTypeDef]
    ) -> DeleteSessionResponseTypeDef:
        """
        Removes session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/delete_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#delete_session)
        """

    def get_session(self, **kwargs: Unpack[GetSessionRequestTypeDef]) -> GetSessionResponseTypeDef:
        """
        Returns session information for a specified bot, alias, and user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/get_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#get_session)
        """

    def post_content(
        self, **kwargs: Unpack[PostContentRequestTypeDef]
    ) -> PostContentResponseTypeDef:
        """
        Sends user input (text or speech) to Amazon Lex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/post_content.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#post_content)
        """

    def post_text(self, **kwargs: Unpack[PostTextRequestTypeDef]) -> PostTextResponseTypeDef:
        """
        Sends user input to Amazon Lex.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/post_text.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#post_text)
        """

    def put_session(self, **kwargs: Unpack[PutSessionRequestTypeDef]) -> PutSessionResponseTypeDef:
        """
        Creates a new session or modifies an existing session with an Amazon Lex bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime/client/put_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lex_runtime/client/#put_session)
        """
