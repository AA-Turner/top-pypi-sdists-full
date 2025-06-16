"""
Main interface for voice-id service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_voice_id/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_voice_id import (
        Client,
        ListDomainsPaginator,
        ListFraudsterRegistrationJobsPaginator,
        ListFraudstersPaginator,
        ListSpeakerEnrollmentJobsPaginator,
        ListSpeakersPaginator,
        ListWatchlistsPaginator,
        VoiceIDClient,
    )

    session = get_session()
    async with session.create_client("voice-id") as client:
        client: VoiceIDClient
        ...


    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_fraudster_registration_jobs_paginator: ListFraudsterRegistrationJobsPaginator = client.get_paginator("list_fraudster_registration_jobs")
    list_fraudsters_paginator: ListFraudstersPaginator = client.get_paginator("list_fraudsters")
    list_speaker_enrollment_jobs_paginator: ListSpeakerEnrollmentJobsPaginator = client.get_paginator("list_speaker_enrollment_jobs")
    list_speakers_paginator: ListSpeakersPaginator = client.get_paginator("list_speakers")
    list_watchlists_paginator: ListWatchlistsPaginator = client.get_paginator("list_watchlists")
    ```
"""

from .client import VoiceIDClient
from .paginator import (
    ListDomainsPaginator,
    ListFraudsterRegistrationJobsPaginator,
    ListFraudstersPaginator,
    ListSpeakerEnrollmentJobsPaginator,
    ListSpeakersPaginator,
    ListWatchlistsPaginator,
)

Client = VoiceIDClient


__all__ = (
    "Client",
    "ListDomainsPaginator",
    "ListFraudsterRegistrationJobsPaginator",
    "ListFraudstersPaginator",
    "ListSpeakerEnrollmentJobsPaginator",
    "ListSpeakersPaginator",
    "ListWatchlistsPaginator",
    "VoiceIDClient",
)
