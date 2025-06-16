"""
Type annotations for lex-models service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lex_models.client import LexModelBuildingServiceClient
    from types_aiobotocore_lex_models.paginator import (
        GetBotAliasesPaginator,
        GetBotChannelAssociationsPaginator,
        GetBotVersionsPaginator,
        GetBotsPaginator,
        GetBuiltinIntentsPaginator,
        GetBuiltinSlotTypesPaginator,
        GetIntentVersionsPaginator,
        GetIntentsPaginator,
        GetSlotTypeVersionsPaginator,
        GetSlotTypesPaginator,
    )

    session = get_session()
    with session.create_client("lex-models") as client:
        client: LexModelBuildingServiceClient

        get_bot_aliases_paginator: GetBotAliasesPaginator = client.get_paginator("get_bot_aliases")
        get_bot_channel_associations_paginator: GetBotChannelAssociationsPaginator = client.get_paginator("get_bot_channel_associations")
        get_bot_versions_paginator: GetBotVersionsPaginator = client.get_paginator("get_bot_versions")
        get_bots_paginator: GetBotsPaginator = client.get_paginator("get_bots")
        get_builtin_intents_paginator: GetBuiltinIntentsPaginator = client.get_paginator("get_builtin_intents")
        get_builtin_slot_types_paginator: GetBuiltinSlotTypesPaginator = client.get_paginator("get_builtin_slot_types")
        get_intent_versions_paginator: GetIntentVersionsPaginator = client.get_paginator("get_intent_versions")
        get_intents_paginator: GetIntentsPaginator = client.get_paginator("get_intents")
        get_slot_type_versions_paginator: GetSlotTypeVersionsPaginator = client.get_paginator("get_slot_type_versions")
        get_slot_types_paginator: GetSlotTypesPaginator = client.get_paginator("get_slot_types")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetBotAliasesRequestPaginateTypeDef,
    GetBotAliasesResponseTypeDef,
    GetBotChannelAssociationsRequestPaginateTypeDef,
    GetBotChannelAssociationsResponseTypeDef,
    GetBotsRequestPaginateTypeDef,
    GetBotsResponseTypeDef,
    GetBotVersionsRequestPaginateTypeDef,
    GetBotVersionsResponseTypeDef,
    GetBuiltinIntentsRequestPaginateTypeDef,
    GetBuiltinIntentsResponseTypeDef,
    GetBuiltinSlotTypesRequestPaginateTypeDef,
    GetBuiltinSlotTypesResponseTypeDef,
    GetIntentsRequestPaginateTypeDef,
    GetIntentsResponseTypeDef,
    GetIntentVersionsRequestPaginateTypeDef,
    GetIntentVersionsResponseTypeDef,
    GetSlotTypesRequestPaginateTypeDef,
    GetSlotTypesResponseTypeDef,
    GetSlotTypeVersionsRequestPaginateTypeDef,
    GetSlotTypeVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetBotAliasesPaginator",
    "GetBotChannelAssociationsPaginator",
    "GetBotVersionsPaginator",
    "GetBotsPaginator",
    "GetBuiltinIntentsPaginator",
    "GetBuiltinSlotTypesPaginator",
    "GetIntentVersionsPaginator",
    "GetIntentsPaginator",
    "GetSlotTypeVersionsPaginator",
    "GetSlotTypesPaginator",
)

if TYPE_CHECKING:
    _GetBotAliasesPaginatorBase = AioPaginator[GetBotAliasesResponseTypeDef]
else:
    _GetBotAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBotAliasesPaginator(_GetBotAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotAliases.html#LexModelBuildingService.Paginator.GetBotAliases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBotAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBotAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotAliases.html#LexModelBuildingService.Paginator.GetBotAliases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotaliasespaginator)
        """

if TYPE_CHECKING:
    _GetBotChannelAssociationsPaginatorBase = AioPaginator[GetBotChannelAssociationsResponseTypeDef]
else:
    _GetBotChannelAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBotChannelAssociationsPaginator(_GetBotChannelAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotChannelAssociations.html#LexModelBuildingService.Paginator.GetBotChannelAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotchannelassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBotChannelAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBotChannelAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotChannelAssociations.html#LexModelBuildingService.Paginator.GetBotChannelAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotchannelassociationspaginator)
        """

if TYPE_CHECKING:
    _GetBotVersionsPaginatorBase = AioPaginator[GetBotVersionsResponseTypeDef]
else:
    _GetBotVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBotVersionsPaginator(_GetBotVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotVersions.html#LexModelBuildingService.Paginator.GetBotVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBotVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBotVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBotVersions.html#LexModelBuildingService.Paginator.GetBotVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotversionspaginator)
        """

if TYPE_CHECKING:
    _GetBotsPaginatorBase = AioPaginator[GetBotsResponseTypeDef]
else:
    _GetBotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBotsPaginator(_GetBotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBots.html#LexModelBuildingService.Paginator.GetBots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBotsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBots.html#LexModelBuildingService.Paginator.GetBots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbotspaginator)
        """

if TYPE_CHECKING:
    _GetBuiltinIntentsPaginatorBase = AioPaginator[GetBuiltinIntentsResponseTypeDef]
else:
    _GetBuiltinIntentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBuiltinIntentsPaginator(_GetBuiltinIntentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinIntents.html#LexModelBuildingService.Paginator.GetBuiltinIntents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinintentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBuiltinIntentsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBuiltinIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinIntents.html#LexModelBuildingService.Paginator.GetBuiltinIntents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinintentspaginator)
        """

if TYPE_CHECKING:
    _GetBuiltinSlotTypesPaginatorBase = AioPaginator[GetBuiltinSlotTypesResponseTypeDef]
else:
    _GetBuiltinSlotTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetBuiltinSlotTypesPaginator(_GetBuiltinSlotTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinSlotTypes.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinslottypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBuiltinSlotTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBuiltinSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetBuiltinSlotTypes.html#LexModelBuildingService.Paginator.GetBuiltinSlotTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getbuiltinslottypespaginator)
        """

if TYPE_CHECKING:
    _GetIntentVersionsPaginatorBase = AioPaginator[GetIntentVersionsResponseTypeDef]
else:
    _GetIntentVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetIntentVersionsPaginator(_GetIntentVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntentVersions.html#LexModelBuildingService.Paginator.GetIntentVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetIntentVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetIntentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntentVersions.html#LexModelBuildingService.Paginator.GetIntentVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentversionspaginator)
        """

if TYPE_CHECKING:
    _GetIntentsPaginatorBase = AioPaginator[GetIntentsResponseTypeDef]
else:
    _GetIntentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetIntentsPaginator(_GetIntentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntents.html#LexModelBuildingService.Paginator.GetIntents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetIntentsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetIntentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetIntents.html#LexModelBuildingService.Paginator.GetIntents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getintentspaginator)
        """

if TYPE_CHECKING:
    _GetSlotTypeVersionsPaginatorBase = AioPaginator[GetSlotTypeVersionsResponseTypeDef]
else:
    _GetSlotTypeVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetSlotTypeVersionsPaginator(_GetSlotTypeVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypeVersions.html#LexModelBuildingService.Paginator.GetSlotTypeVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypeversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSlotTypeVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSlotTypeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypeVersions.html#LexModelBuildingService.Paginator.GetSlotTypeVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypeversionspaginator)
        """

if TYPE_CHECKING:
    _GetSlotTypesPaginatorBase = AioPaginator[GetSlotTypesResponseTypeDef]
else:
    _GetSlotTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetSlotTypesPaginator(_GetSlotTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypes.html#LexModelBuildingService.Paginator.GetSlotTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSlotTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSlotTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models/paginator/GetSlotTypes.html#LexModelBuildingService.Paginator.GetSlotTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lex_models/paginators/#getslottypespaginator)
        """
