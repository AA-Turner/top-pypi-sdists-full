"""
Main interface for codeguruprofiler service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguruprofiler import (
        Client,
        CodeGuruProfilerClient,
        ListProfileTimesPaginator,
    )

    session = get_session()
    async with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient
        ...


    list_profile_times_paginator: ListProfileTimesPaginator = client.get_paginator("list_profile_times")
    ```
"""

from .client import CodeGuruProfilerClient
from .paginator import ListProfileTimesPaginator

Client = CodeGuruProfilerClient

__all__ = ("Client", "CodeGuruProfilerClient", "ListProfileTimesPaginator")
