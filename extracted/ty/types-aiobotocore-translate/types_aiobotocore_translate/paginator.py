"""
Type annotations for translate service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_translate.client import TranslateClient
    from types_aiobotocore_translate.paginator import (
        ListTerminologiesPaginator,
    )

    session = get_session()
    with session.create_client("translate") as client:
        client: TranslateClient

        list_terminologies_paginator: ListTerminologiesPaginator = client.get_paginator("list_terminologies")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListTerminologiesRequestPaginateTypeDef, ListTerminologiesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListTerminologiesPaginator",)


if TYPE_CHECKING:
    _ListTerminologiesPaginatorBase = AioPaginator[ListTerminologiesResponseTypeDef]
else:
    _ListTerminologiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTerminologiesPaginator(_ListTerminologiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/#listterminologiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTerminologiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTerminologiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate/paginator/ListTerminologies.html#Translate.Paginator.ListTerminologies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/paginators/#listterminologiespaginator)
        """
