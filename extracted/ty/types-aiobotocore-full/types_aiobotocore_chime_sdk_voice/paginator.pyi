"""
Type annotations for chime-sdk-voice service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_chime_sdk_voice.client import ChimeSDKVoiceClient
    from types_aiobotocore_chime_sdk_voice.paginator import (
        ListSipMediaApplicationsPaginator,
        ListSipRulesPaginator,
    )

    session = get_session()
    with session.create_client("chime-sdk-voice") as client:
        client: ChimeSDKVoiceClient

        list_sip_media_applications_paginator: ListSipMediaApplicationsPaginator = client.get_paginator("list_sip_media_applications")
        list_sip_rules_paginator: ListSipRulesPaginator = client.get_paginator("list_sip_rules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListSipMediaApplicationsRequestPaginateTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesRequestPaginateTypeDef,
    ListSipRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSipMediaApplicationsPaginator", "ListSipRulesPaginator")

if TYPE_CHECKING:
    _ListSipMediaApplicationsPaginatorBase = AioPaginator[ListSipMediaApplicationsResponseTypeDef]
else:
    _ListSipMediaApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSipMediaApplicationsPaginator(_ListSipMediaApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSipMediaApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSipMediaApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipMediaApplications.html#ChimeSDKVoice.Paginator.ListSipMediaApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsipmediaapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListSipRulesPaginatorBase = AioPaginator[ListSipRulesResponseTypeDef]
else:
    _ListSipRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSipRulesPaginator(_ListSipRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsiprulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSipRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSipRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-voice/paginator/ListSipRules.html#ChimeSDKVoice.Paginator.ListSipRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_voice/paginators/#listsiprulespaginator)
        """
