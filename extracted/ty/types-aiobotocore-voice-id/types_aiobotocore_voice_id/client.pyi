"""
Type annotations for voice-id service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_voice_id.client import VoiceIDClient

    session = get_session()
    async with session.create_client("voice-id") as client:
        client: VoiceIDClient
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
    ListDomainsPaginator,
    ListFraudsterRegistrationJobsPaginator,
    ListFraudstersPaginator,
    ListSpeakerEnrollmentJobsPaginator,
    ListSpeakersPaginator,
    ListWatchlistsPaginator,
)
from .type_defs import (
    AssociateFraudsterRequestTypeDef,
    AssociateFraudsterResponseTypeDef,
    CreateDomainRequestTypeDef,
    CreateDomainResponseTypeDef,
    CreateWatchlistRequestTypeDef,
    CreateWatchlistResponseTypeDef,
    DeleteDomainRequestTypeDef,
    DeleteFraudsterRequestTypeDef,
    DeleteSpeakerRequestTypeDef,
    DeleteWatchlistRequestTypeDef,
    DescribeDomainRequestTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeFraudsterRegistrationJobRequestTypeDef,
    DescribeFraudsterRegistrationJobResponseTypeDef,
    DescribeFraudsterRequestTypeDef,
    DescribeFraudsterResponseTypeDef,
    DescribeSpeakerEnrollmentJobRequestTypeDef,
    DescribeSpeakerEnrollmentJobResponseTypeDef,
    DescribeSpeakerRequestTypeDef,
    DescribeSpeakerResponseTypeDef,
    DescribeWatchlistRequestTypeDef,
    DescribeWatchlistResponseTypeDef,
    DisassociateFraudsterRequestTypeDef,
    DisassociateFraudsterResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluateSessionRequestTypeDef,
    EvaluateSessionResponseTypeDef,
    ListDomainsRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListFraudsterRegistrationJobsRequestTypeDef,
    ListFraudsterRegistrationJobsResponseTypeDef,
    ListFraudstersRequestTypeDef,
    ListFraudstersResponseTypeDef,
    ListSpeakerEnrollmentJobsRequestTypeDef,
    ListSpeakerEnrollmentJobsResponseTypeDef,
    ListSpeakersRequestTypeDef,
    ListSpeakersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWatchlistsRequestTypeDef,
    ListWatchlistsResponseTypeDef,
    OptOutSpeakerRequestTypeDef,
    OptOutSpeakerResponseTypeDef,
    StartFraudsterRegistrationJobRequestTypeDef,
    StartFraudsterRegistrationJobResponseTypeDef,
    StartSpeakerEnrollmentJobRequestTypeDef,
    StartSpeakerEnrollmentJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDomainRequestTypeDef,
    UpdateDomainResponseTypeDef,
    UpdateWatchlistRequestTypeDef,
    UpdateWatchlistResponseTypeDef,
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

__all__ = ("VoiceIDClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class VoiceIDClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        VoiceIDClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#generate_presigned_url)
        """

    async def associate_fraudster(
        self, **kwargs: Unpack[AssociateFraudsterRequestTypeDef]
    ) -> AssociateFraudsterResponseTypeDef:
        """
        Associates the fraudsters with the watchlist specified in the same domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/associate_fraudster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#associate_fraudster)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainRequestTypeDef]
    ) -> CreateDomainResponseTypeDef:
        """
        Creates a domain that contains all Amazon Connect Voice ID data, such as
        speakers, fraudsters, customer audio, and voiceprints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/create_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#create_domain)
        """

    async def create_watchlist(
        self, **kwargs: Unpack[CreateWatchlistRequestTypeDef]
    ) -> CreateWatchlistResponseTypeDef:
        """
        Creates a watchlist that fraudsters can be a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/create_watchlist.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#create_watchlist)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified domain from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#delete_domain)
        """

    async def delete_fraudster(
        self, **kwargs: Unpack[DeleteFraudsterRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified fraudster from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_fraudster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#delete_fraudster)
        """

    async def delete_speaker(
        self, **kwargs: Unpack[DeleteSpeakerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified speaker from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_speaker.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#delete_speaker)
        """

    async def delete_watchlist(
        self, **kwargs: Unpack[DeleteWatchlistRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified watchlist from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/delete_watchlist.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#delete_watchlist)
        """

    async def describe_domain(
        self, **kwargs: Unpack[DescribeDomainRequestTypeDef]
    ) -> DescribeDomainResponseTypeDef:
        """
        Describes the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_domain)
        """

    async def describe_fraudster(
        self, **kwargs: Unpack[DescribeFraudsterRequestTypeDef]
    ) -> DescribeFraudsterResponseTypeDef:
        """
        Describes the specified fraudster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_fraudster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_fraudster)
        """

    async def describe_fraudster_registration_job(
        self, **kwargs: Unpack[DescribeFraudsterRegistrationJobRequestTypeDef]
    ) -> DescribeFraudsterRegistrationJobResponseTypeDef:
        """
        Describes the specified fraudster registration job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_fraudster_registration_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_fraudster_registration_job)
        """

    async def describe_speaker(
        self, **kwargs: Unpack[DescribeSpeakerRequestTypeDef]
    ) -> DescribeSpeakerResponseTypeDef:
        """
        Describes the specified speaker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_speaker.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_speaker)
        """

    async def describe_speaker_enrollment_job(
        self, **kwargs: Unpack[DescribeSpeakerEnrollmentJobRequestTypeDef]
    ) -> DescribeSpeakerEnrollmentJobResponseTypeDef:
        """
        Describes the specified speaker enrollment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_speaker_enrollment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_speaker_enrollment_job)
        """

    async def describe_watchlist(
        self, **kwargs: Unpack[DescribeWatchlistRequestTypeDef]
    ) -> DescribeWatchlistResponseTypeDef:
        """
        Describes the specified watchlist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/describe_watchlist.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#describe_watchlist)
        """

    async def disassociate_fraudster(
        self, **kwargs: Unpack[DisassociateFraudsterRequestTypeDef]
    ) -> DisassociateFraudsterResponseTypeDef:
        """
        Disassociates the fraudsters from the watchlist specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/disassociate_fraudster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#disassociate_fraudster)
        """

    async def evaluate_session(
        self, **kwargs: Unpack[EvaluateSessionRequestTypeDef]
    ) -> EvaluateSessionResponseTypeDef:
        """
        Evaluates a specified session based on audio data accumulated during a
        streaming Amazon Connect Voice ID call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/evaluate_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#evaluate_session)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        Lists all the domains in the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_domains.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_domains)
        """

    async def list_fraudster_registration_jobs(
        self, **kwargs: Unpack[ListFraudsterRegistrationJobsRequestTypeDef]
    ) -> ListFraudsterRegistrationJobsResponseTypeDef:
        """
        Lists all the fraudster registration jobs in the domain with the given
        <code>JobStatus</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_fraudster_registration_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_fraudster_registration_jobs)
        """

    async def list_fraudsters(
        self, **kwargs: Unpack[ListFraudstersRequestTypeDef]
    ) -> ListFraudstersResponseTypeDef:
        """
        Lists all fraudsters in a specified watchlist or domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_fraudsters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_fraudsters)
        """

    async def list_speaker_enrollment_jobs(
        self, **kwargs: Unpack[ListSpeakerEnrollmentJobsRequestTypeDef]
    ) -> ListSpeakerEnrollmentJobsResponseTypeDef:
        """
        Lists all the speaker enrollment jobs in the domain with the specified
        <code>JobStatus</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_speaker_enrollment_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_speaker_enrollment_jobs)
        """

    async def list_speakers(
        self, **kwargs: Unpack[ListSpeakersRequestTypeDef]
    ) -> ListSpeakersResponseTypeDef:
        """
        Lists all speakers in a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_speakers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_speakers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with a specified Voice ID resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_tags_for_resource)
        """

    async def list_watchlists(
        self, **kwargs: Unpack[ListWatchlistsRequestTypeDef]
    ) -> ListWatchlistsResponseTypeDef:
        """
        Lists all watchlists in a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/list_watchlists.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#list_watchlists)
        """

    async def opt_out_speaker(
        self, **kwargs: Unpack[OptOutSpeakerRequestTypeDef]
    ) -> OptOutSpeakerResponseTypeDef:
        """
        Opts out a speaker from Voice ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/opt_out_speaker.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#opt_out_speaker)
        """

    async def start_fraudster_registration_job(
        self, **kwargs: Unpack[StartFraudsterRegistrationJobRequestTypeDef]
    ) -> StartFraudsterRegistrationJobResponseTypeDef:
        """
        Starts a new batch fraudster registration job using provided details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/start_fraudster_registration_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#start_fraudster_registration_job)
        """

    async def start_speaker_enrollment_job(
        self, **kwargs: Unpack[StartSpeakerEnrollmentJobRequestTypeDef]
    ) -> StartSpeakerEnrollmentJobResponseTypeDef:
        """
        Starts a new batch speaker enrollment job using specified details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/start_speaker_enrollment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#start_speaker_enrollment_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags a Voice ID resource with the provided list of tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes specified tags from a specified Amazon Connect Voice ID resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#untag_resource)
        """

    async def update_domain(
        self, **kwargs: Unpack[UpdateDomainRequestTypeDef]
    ) -> UpdateDomainResponseTypeDef:
        """
        Updates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/update_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#update_domain)
        """

    async def update_watchlist(
        self, **kwargs: Unpack[UpdateWatchlistRequestTypeDef]
    ) -> UpdateWatchlistResponseTypeDef:
        """
        Updates the specified watchlist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/update_watchlist.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#update_watchlist)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domains"]
    ) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fraudster_registration_jobs"]
    ) -> ListFraudsterRegistrationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fraudsters"]
    ) -> ListFraudstersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_speaker_enrollment_jobs"]
    ) -> ListSpeakerEnrollmentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_speakers"]
    ) -> ListSpeakersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_watchlists"]
    ) -> ListWatchlistsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id.html#VoiceID.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/client/)
        """
