"""
Type annotations for voice-id service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_voice_id.client import VoiceIDClient
    from types_aiobotocore_voice_id.paginator import (
        ListDomainsPaginator,
        ListFraudsterRegistrationJobsPaginator,
        ListFraudstersPaginator,
        ListSpeakerEnrollmentJobsPaginator,
        ListSpeakersPaginator,
        ListWatchlistsPaginator,
    )

    session = get_session()
    with session.create_client("voice-id") as client:
        client: VoiceIDClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_fraudster_registration_jobs_paginator: ListFraudsterRegistrationJobsPaginator = client.get_paginator("list_fraudster_registration_jobs")
        list_fraudsters_paginator: ListFraudstersPaginator = client.get_paginator("list_fraudsters")
        list_speaker_enrollment_jobs_paginator: ListSpeakerEnrollmentJobsPaginator = client.get_paginator("list_speaker_enrollment_jobs")
        list_speakers_paginator: ListSpeakersPaginator = client.get_paginator("list_speakers")
        list_watchlists_paginator: ListWatchlistsPaginator = client.get_paginator("list_watchlists")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResponseTypeDef,
    ListFraudsterRegistrationJobsRequestPaginateTypeDef,
    ListFraudsterRegistrationJobsResponseTypeDef,
    ListFraudstersRequestPaginateTypeDef,
    ListFraudstersResponseTypeDef,
    ListSpeakerEnrollmentJobsRequestPaginateTypeDef,
    ListSpeakerEnrollmentJobsResponseTypeDef,
    ListSpeakersRequestPaginateTypeDef,
    ListSpeakersResponseTypeDef,
    ListWatchlistsRequestPaginateTypeDef,
    ListWatchlistsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDomainsPaginator",
    "ListFraudsterRegistrationJobsPaginator",
    "ListFraudstersPaginator",
    "ListSpeakerEnrollmentJobsPaginator",
    "ListSpeakersPaginator",
    "ListWatchlistsPaginator",
)


if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResponseTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListDomains.html#VoiceID.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListDomains.html#VoiceID.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listdomainspaginator)
        """


if TYPE_CHECKING:
    _ListFraudsterRegistrationJobsPaginatorBase = AioPaginator[
        ListFraudsterRegistrationJobsResponseTypeDef
    ]
else:
    _ListFraudsterRegistrationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFraudsterRegistrationJobsPaginator(_ListFraudsterRegistrationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsterRegistrationJobs.html#VoiceID.Paginator.ListFraudsterRegistrationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterregistrationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFraudsterRegistrationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFraudsterRegistrationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsterRegistrationJobs.html#VoiceID.Paginator.ListFraudsterRegistrationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterregistrationjobspaginator)
        """


if TYPE_CHECKING:
    _ListFraudstersPaginatorBase = AioPaginator[ListFraudstersResponseTypeDef]
else:
    _ListFraudstersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFraudstersPaginator(_ListFraudstersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsters.html#VoiceID.Paginator.ListFraudsters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFraudstersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFraudstersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListFraudsters.html#VoiceID.Paginator.ListFraudsters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listfraudsterspaginator)
        """


if TYPE_CHECKING:
    _ListSpeakerEnrollmentJobsPaginatorBase = AioPaginator[ListSpeakerEnrollmentJobsResponseTypeDef]
else:
    _ListSpeakerEnrollmentJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSpeakerEnrollmentJobsPaginator(_ListSpeakerEnrollmentJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakerEnrollmentJobs.html#VoiceID.Paginator.ListSpeakerEnrollmentJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerenrollmentjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpeakerEnrollmentJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSpeakerEnrollmentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakerEnrollmentJobs.html#VoiceID.Paginator.ListSpeakerEnrollmentJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerenrollmentjobspaginator)
        """


if TYPE_CHECKING:
    _ListSpeakersPaginatorBase = AioPaginator[ListSpeakersResponseTypeDef]
else:
    _ListSpeakersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSpeakersPaginator(_ListSpeakersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakers.html#VoiceID.Paginator.ListSpeakers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpeakersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSpeakersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListSpeakers.html#VoiceID.Paginator.ListSpeakers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listspeakerspaginator)
        """


if TYPE_CHECKING:
    _ListWatchlistsPaginatorBase = AioPaginator[ListWatchlistsResponseTypeDef]
else:
    _ListWatchlistsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWatchlistsPaginator(_ListWatchlistsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListWatchlists.html#VoiceID.Paginator.ListWatchlists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listwatchlistspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWatchlistsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWatchlistsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/voice-id/paginator/ListWatchlists.html#VoiceID.Paginator.ListWatchlists.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/paginators/#listwatchlistspaginator)
        """
