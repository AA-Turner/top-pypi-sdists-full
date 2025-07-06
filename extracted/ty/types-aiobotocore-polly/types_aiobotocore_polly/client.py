"""
Type annotations for polly service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_polly.client import PollyClient

    session = get_session()
    async with session.create_client("polly") as client:
        client: PollyClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeVoicesPaginator,
    ListLexiconsPaginator,
    ListSpeechSynthesisTasksPaginator,
)
from .type_defs import (
    DeleteLexiconInputTypeDef,
    DescribeVoicesInputTypeDef,
    DescribeVoicesOutputTypeDef,
    GetLexiconInputTypeDef,
    GetLexiconOutputTypeDef,
    GetSpeechSynthesisTaskInputTypeDef,
    GetSpeechSynthesisTaskOutputTypeDef,
    ListLexiconsInputTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksInputTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
    PutLexiconInputTypeDef,
    StartSpeechSynthesisTaskInputTypeDef,
    StartSpeechSynthesisTaskOutputTypeDef,
    SynthesizeSpeechInputTypeDef,
    SynthesizeSpeechOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("PollyClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    EngineNotSupportedException: Type[BotocoreClientError]
    InvalidLexiconException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidS3BucketException: Type[BotocoreClientError]
    InvalidS3KeyException: Type[BotocoreClientError]
    InvalidSampleRateException: Type[BotocoreClientError]
    InvalidSnsTopicArnException: Type[BotocoreClientError]
    InvalidSsmlException: Type[BotocoreClientError]
    InvalidTaskIdException: Type[BotocoreClientError]
    LanguageNotSupportedException: Type[BotocoreClientError]
    LexiconNotFoundException: Type[BotocoreClientError]
    LexiconSizeExceededException: Type[BotocoreClientError]
    MarksNotSupportedForFormatException: Type[BotocoreClientError]
    MaxLexemeLengthExceededException: Type[BotocoreClientError]
    MaxLexiconsNumberExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    SsmlMarksNotSupportedForTextTypeException: Type[BotocoreClientError]
    SynthesisTaskNotFoundException: Type[BotocoreClientError]
    TextLengthExceededException: Type[BotocoreClientError]
    UnsupportedPlsAlphabetException: Type[BotocoreClientError]
    UnsupportedPlsLanguageException: Type[BotocoreClientError]


class PollyClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PollyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#generate_presigned_url)
        """

    async def delete_lexicon(self, **kwargs: Unpack[DeleteLexiconInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified pronunciation lexicon stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/delete_lexicon.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#delete_lexicon)
        """

    async def describe_voices(
        self, **kwargs: Unpack[DescribeVoicesInputTypeDef]
    ) -> DescribeVoicesOutputTypeDef:
        """
        Returns the list of voices that are available for use when requesting speech
        synthesis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/describe_voices.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#describe_voices)
        """

    async def get_lexicon(
        self, **kwargs: Unpack[GetLexiconInputTypeDef]
    ) -> GetLexiconOutputTypeDef:
        """
        Returns the content of the specified pronunciation lexicon stored in an Amazon
        Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_lexicon.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#get_lexicon)
        """

    async def get_speech_synthesis_task(
        self, **kwargs: Unpack[GetSpeechSynthesisTaskInputTypeDef]
    ) -> GetSpeechSynthesisTaskOutputTypeDef:
        """
        Retrieves a specific SpeechSynthesisTask object based on its TaskID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_speech_synthesis_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#get_speech_synthesis_task)
        """

    async def list_lexicons(
        self, **kwargs: Unpack[ListLexiconsInputTypeDef]
    ) -> ListLexiconsOutputTypeDef:
        """
        Returns a list of pronunciation lexicons stored in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/list_lexicons.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#list_lexicons)
        """

    async def list_speech_synthesis_tasks(
        self, **kwargs: Unpack[ListSpeechSynthesisTasksInputTypeDef]
    ) -> ListSpeechSynthesisTasksOutputTypeDef:
        """
        Returns a list of SpeechSynthesisTask objects ordered by their creation date.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/list_speech_synthesis_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#list_speech_synthesis_tasks)
        """

    async def put_lexicon(self, **kwargs: Unpack[PutLexiconInputTypeDef]) -> Dict[str, Any]:
        """
        Stores a pronunciation lexicon in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/put_lexicon.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#put_lexicon)
        """

    async def start_speech_synthesis_task(
        self, **kwargs: Unpack[StartSpeechSynthesisTaskInputTypeDef]
    ) -> StartSpeechSynthesisTaskOutputTypeDef:
        """
        Allows the creation of an asynchronous synthesis task, by starting a new
        <code>SpeechSynthesisTask</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/start_speech_synthesis_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#start_speech_synthesis_task)
        """

    async def synthesize_speech(
        self, **kwargs: Unpack[SynthesizeSpeechInputTypeDef]
    ) -> SynthesizeSpeechOutputTypeDef:
        """
        Synthesizes UTF-8 input, plain text or SSML, to a stream of bytes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/synthesize_speech.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#synthesize_speech)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_voices"]
    ) -> DescribeVoicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_lexicons"]
    ) -> ListLexiconsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_speech_synthesis_tasks"]
    ) -> ListSpeechSynthesisTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/client/)
        """
