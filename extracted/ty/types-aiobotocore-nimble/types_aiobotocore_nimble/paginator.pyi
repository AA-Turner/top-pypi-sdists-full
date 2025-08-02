"""
Type annotations for nimble service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_nimble.client import NimbleStudioClient
    from types_aiobotocore_nimble.paginator import (
        ListEulaAcceptancesPaginator,
        ListEulasPaginator,
        ListLaunchProfileMembersPaginator,
        ListLaunchProfilesPaginator,
        ListStreamingImagesPaginator,
        ListStreamingSessionBackupsPaginator,
        ListStreamingSessionsPaginator,
        ListStudioComponentsPaginator,
        ListStudioMembersPaginator,
        ListStudiosPaginator,
    )

    session = get_session()
    with session.create_client("nimble") as client:
        client: NimbleStudioClient

        list_eula_acceptances_paginator: ListEulaAcceptancesPaginator = client.get_paginator("list_eula_acceptances")
        list_eulas_paginator: ListEulasPaginator = client.get_paginator("list_eulas")
        list_launch_profile_members_paginator: ListLaunchProfileMembersPaginator = client.get_paginator("list_launch_profile_members")
        list_launch_profiles_paginator: ListLaunchProfilesPaginator = client.get_paginator("list_launch_profiles")
        list_streaming_images_paginator: ListStreamingImagesPaginator = client.get_paginator("list_streaming_images")
        list_streaming_session_backups_paginator: ListStreamingSessionBackupsPaginator = client.get_paginator("list_streaming_session_backups")
        list_streaming_sessions_paginator: ListStreamingSessionsPaginator = client.get_paginator("list_streaming_sessions")
        list_studio_components_paginator: ListStudioComponentsPaginator = client.get_paginator("list_studio_components")
        list_studio_members_paginator: ListStudioMembersPaginator = client.get_paginator("list_studio_members")
        list_studios_paginator: ListStudiosPaginator = client.get_paginator("list_studios")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef,
    ListEulaAcceptancesResponseTypeDef,
    ListEulasRequestListEulasPaginateTypeDef,
    ListEulasResponseTypeDef,
    ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef,
    ListLaunchProfileMembersResponseTypeDef,
    ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef,
    ListLaunchProfilesResponseTypeDef,
    ListStreamingImagesRequestListStreamingImagesPaginateTypeDef,
    ListStreamingImagesResponseTypeDef,
    ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef,
    ListStreamingSessionBackupsResponseTypeDef,
    ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef,
    ListStreamingSessionsResponseTypeDef,
    ListStudioComponentsRequestListStudioComponentsPaginateTypeDef,
    ListStudioComponentsResponseTypeDef,
    ListStudioMembersRequestListStudioMembersPaginateTypeDef,
    ListStudioMembersResponseTypeDef,
    ListStudiosRequestListStudiosPaginateTypeDef,
    ListStudiosResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEulaAcceptancesPaginator",
    "ListEulasPaginator",
    "ListLaunchProfileMembersPaginator",
    "ListLaunchProfilesPaginator",
    "ListStreamingImagesPaginator",
    "ListStreamingSessionBackupsPaginator",
    "ListStreamingSessionsPaginator",
    "ListStudioComponentsPaginator",
    "ListStudioMembersPaginator",
    "ListStudiosPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEulaAcceptancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListEulaAcceptances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listeulaacceptancespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef]
    ) -> AsyncIterator[ListEulaAcceptancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListEulaAcceptances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listeulaacceptancespaginator)
        """

class ListEulasPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListEulas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listeulaspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEulasRequestListEulasPaginateTypeDef]
    ) -> AsyncIterator[ListEulasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListEulas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listeulaspaginator)
        """

class ListLaunchProfileMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfileMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listlaunchprofilememberspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef],
    ) -> AsyncIterator[ListLaunchProfileMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfileMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listlaunchprofilememberspaginator)
        """

class ListLaunchProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listlaunchprofilespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef]
    ) -> AsyncIterator[ListLaunchProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListLaunchProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#listlaunchprofilespaginator)
        """

class ListStreamingImagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingimagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamingImagesRequestListStreamingImagesPaginateTypeDef]
    ) -> AsyncIterator[ListStreamingImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingimagespaginator)
        """

class ListStreamingSessionBackupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessionBackups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingsessionbackupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListStreamingSessionBackupsRequestListStreamingSessionBackupsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListStreamingSessionBackupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessionBackups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingsessionbackupspaginator)
        """

class ListStreamingSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingsessionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef]
    ) -> AsyncIterator[ListStreamingSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStreamingSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststreamingsessionspaginator)
        """

class ListStudioComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiocomponentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStudioComponentsRequestListStudioComponentsPaginateTypeDef]
    ) -> AsyncIterator[ListStudioComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiocomponentspaginator)
        """

class ListStudioMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiomemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStudioMembersRequestListStudioMembersPaginateTypeDef]
    ) -> AsyncIterator[ListStudioMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudioMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiomemberspaginator)
        """

class ListStudiosPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudios)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiospaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListStudiosRequestListStudiosPaginateTypeDef]
    ) -> AsyncIterator[ListStudiosResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Paginator.ListStudios.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/paginators/#liststudiospaginator)
        """
