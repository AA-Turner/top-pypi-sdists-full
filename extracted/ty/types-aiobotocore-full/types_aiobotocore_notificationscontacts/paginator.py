"""
Type annotations for notificationscontacts service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_notificationscontacts.client import UserNotificationsContactsClient
    from types_aiobotocore_notificationscontacts.paginator import (
        ListEmailContactsPaginator,
    )

    session = get_session()
    with session.create_client("notificationscontacts") as client:
        client: UserNotificationsContactsClient

        list_email_contacts_paginator: ListEmailContactsPaginator = client.get_paginator("list_email_contacts")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListEmailContactsRequestPaginateTypeDef, ListEmailContactsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEmailContactsPaginator",)


if TYPE_CHECKING:
    _ListEmailContactsPaginatorBase = AioPaginator[ListEmailContactsResponseTypeDef]
else:
    _ListEmailContactsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEmailContactsPaginator(_ListEmailContactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/#listemailcontactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEmailContactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEmailContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/#listemailcontactspaginator)
        """
