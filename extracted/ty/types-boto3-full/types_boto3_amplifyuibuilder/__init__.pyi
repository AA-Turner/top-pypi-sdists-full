"""
Main interface for amplifyuibuilder service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_amplifyuibuilder/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_amplifyuibuilder import (
        AmplifyUIBuilderClient,
        Client,
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

from .client import AmplifyUIBuilderClient
from .paginator import (
    ExportComponentsPaginator,
    ExportFormsPaginator,
    ExportThemesPaginator,
    ListCodegenJobsPaginator,
    ListComponentsPaginator,
    ListFormsPaginator,
    ListThemesPaginator,
)

Client = AmplifyUIBuilderClient

__all__ = (
    "AmplifyUIBuilderClient",
    "Client",
    "ExportComponentsPaginator",
    "ExportFormsPaginator",
    "ExportThemesPaginator",
    "ListCodegenJobsPaginator",
    "ListComponentsPaginator",
    "ListFormsPaginator",
    "ListThemesPaginator",
)
