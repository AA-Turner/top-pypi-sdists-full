"""
Type annotations for amplifyuibuilder service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplifyuibuilder.client import AmplifyUIBuilderClient
    from types_aiobotocore_amplifyuibuilder.paginator import (
        ExportComponentsPaginator,
        ExportFormsPaginator,
        ExportThemesPaginator,
        ListCodegenJobsPaginator,
        ListComponentsPaginator,
        ListFormsPaginator,
        ListThemesPaginator,
    )

    session = get_session()
    with session.create_client("amplifyuibuilder") as client:
        client: AmplifyUIBuilderClient

        export_components_paginator: ExportComponentsPaginator = client.get_paginator("export_components")
        export_forms_paginator: ExportFormsPaginator = client.get_paginator("export_forms")
        export_themes_paginator: ExportThemesPaginator = client.get_paginator("export_themes")
        list_codegen_jobs_paginator: ListCodegenJobsPaginator = client.get_paginator("list_codegen_jobs")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_forms_paginator: ListFormsPaginator = client.get_paginator("list_forms")
        list_themes_paginator: ListThemesPaginator = client.get_paginator("list_themes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ExportComponentsRequestPaginateTypeDef,
    ExportComponentsResponsePaginatorTypeDef,
    ExportComponentsResponseTypeDef,
    ExportFormsRequestPaginateTypeDef,
    ExportFormsResponsePaginatorTypeDef,
    ExportThemesRequestPaginateTypeDef,
    ExportThemesResponsePaginatorTypeDef,
    ListCodegenJobsRequestPaginateTypeDef,
    ListCodegenJobsResponseTypeDef,
    ListComponentsRequestPaginateTypeDef,
    ListComponentsResponseTypeDef,
    ListFormsRequestPaginateTypeDef,
    ListFormsResponseTypeDef,
    ListThemesRequestPaginateTypeDef,
    ListThemesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ExportComponentsPaginator",
    "ExportFormsPaginator",
    "ExportThemesPaginator",
    "ListCodegenJobsPaginator",
    "ListComponentsPaginator",
    "ListFormsPaginator",
    "ListThemesPaginator",
)


if TYPE_CHECKING:
    _ExportComponentsPaginatorBase = AioPaginator[ExportComponentsResponseTypeDef]
else:
    _ExportComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ExportComponentsPaginator(_ExportComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportComponentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExportComponentsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportcomponentspaginator)
        """


if TYPE_CHECKING:
    _ExportFormsPaginatorBase = AioPaginator[ExportFormsResponsePaginatorTypeDef]
else:
    _ExportFormsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ExportFormsPaginator(_ExportFormsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportformspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportFormsRequestPaginateTypeDef]
    ) -> AioPageIterator[ExportFormsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportformspaginator)
        """


if TYPE_CHECKING:
    _ExportThemesPaginatorBase = AioPaginator[ExportThemesResponsePaginatorTypeDef]
else:
    _ExportThemesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ExportThemesPaginator(_ExportThemesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportthemespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportThemesRequestPaginateTypeDef]
    ) -> AioPageIterator[ExportThemesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#exportthemespaginator)
        """


if TYPE_CHECKING:
    _ListCodegenJobsPaginatorBase = AioPaginator[ListCodegenJobsResponseTypeDef]
else:
    _ListCodegenJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCodegenJobsPaginator(_ListCodegenJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcodegenjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodegenJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCodegenJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcodegenjobspaginator)
        """


if TYPE_CHECKING:
    _ListComponentsPaginatorBase = AioPaginator[ListComponentsResponseTypeDef]
else:
    _ListComponentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComponentsPaginator(_ListComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcomponentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listcomponentspaginator)
        """


if TYPE_CHECKING:
    _ListFormsPaginatorBase = AioPaginator[ListFormsResponseTypeDef]
else:
    _ListFormsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFormsPaginator(_ListFormsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listformspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFormsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listformspaginator)
        """


if TYPE_CHECKING:
    _ListThemesPaginatorBase = AioPaginator[ListThemesResponseTypeDef]
else:
    _ListThemesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThemesPaginator(_ListThemesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listthemespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThemesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifyuibuilder/paginators/#listthemespaginator)
        """
