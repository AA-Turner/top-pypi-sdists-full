"""
Type annotations for amplifyuibuilder service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_amplifyuibuilder.client import AmplifyUIBuilderClient
    from types_boto3_amplifyuibuilder.paginator import (
        ExportComponentsPaginator,
        ExportFormsPaginator,
        ExportThemesPaginator,
        ListCodegenJobsPaginator,
        ListComponentsPaginator,
        ListFormsPaginator,
        ListThemesPaginator,
    )

    session = Session()
    client: AmplifyUIBuilderClient = session.client("amplifyuibuilder")

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

from botocore.paginate import PageIterator, Paginator

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
    _ExportComponentsPaginatorBase = Paginator[ExportComponentsResponseTypeDef]
else:
    _ExportComponentsPaginatorBase = Paginator  # type: ignore[assignment]

class ExportComponentsPaginator(_ExportComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportComponentsRequestPaginateTypeDef]
    ) -> PageIterator[ExportComponentsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportComponents.html#AmplifyUIBuilder.Paginator.ExportComponents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportcomponentspaginator)
        """

if TYPE_CHECKING:
    _ExportFormsPaginatorBase = Paginator[ExportFormsResponsePaginatorTypeDef]
else:
    _ExportFormsPaginatorBase = Paginator  # type: ignore[assignment]

class ExportFormsPaginator(_ExportFormsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportformspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportFormsRequestPaginateTypeDef]
    ) -> PageIterator[ExportFormsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportForms.html#AmplifyUIBuilder.Paginator.ExportForms.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportformspaginator)
        """

if TYPE_CHECKING:
    _ExportThemesPaginatorBase = Paginator[ExportThemesResponsePaginatorTypeDef]
else:
    _ExportThemesPaginatorBase = Paginator  # type: ignore[assignment]

class ExportThemesPaginator(_ExportThemesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ExportThemesRequestPaginateTypeDef]
    ) -> PageIterator[ExportThemesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ExportThemes.html#AmplifyUIBuilder.Paginator.ExportThemes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#exportthemespaginator)
        """

if TYPE_CHECKING:
    _ListCodegenJobsPaginatorBase = Paginator[ListCodegenJobsResponseTypeDef]
else:
    _ListCodegenJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodegenJobsPaginator(_ListCodegenJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listcodegenjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodegenJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListCodegenJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListCodegenJobs.html#AmplifyUIBuilder.Paginator.ListCodegenJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listcodegenjobspaginator)
        """

if TYPE_CHECKING:
    _ListComponentsPaginatorBase = Paginator[ListComponentsResponseTypeDef]
else:
    _ListComponentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListComponentsPaginator(_ListComponentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComponentsRequestPaginateTypeDef]
    ) -> PageIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListComponents.html#AmplifyUIBuilder.Paginator.ListComponents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listcomponentspaginator)
        """

if TYPE_CHECKING:
    _ListFormsPaginatorBase = Paginator[ListFormsResponseTypeDef]
else:
    _ListFormsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFormsPaginator(_ListFormsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listformspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFormsRequestPaginateTypeDef]
    ) -> PageIterator[ListFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListForms.html#AmplifyUIBuilder.Paginator.ListForms.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listformspaginator)
        """

if TYPE_CHECKING:
    _ListThemesPaginatorBase = Paginator[ListThemesResponseTypeDef]
else:
    _ListThemesPaginatorBase = Paginator  # type: ignore[assignment]

class ListThemesPaginator(_ListThemesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listthemespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThemesRequestPaginateTypeDef]
    ) -> PageIterator[ListThemesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifyuibuilder/paginator/ListThemes.html#AmplifyUIBuilder.Paginator.ListThemes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/paginators/#listthemespaginator)
        """
