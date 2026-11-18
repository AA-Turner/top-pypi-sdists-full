"""
Main interface for elementalinference service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_elementalinference import (
        Client,
        ElementalInferenceClient,
        FeedDeletedWaiter,
        ListDictionariesPaginator,
        ListFeedsPaginator,
        ListFunctionsPaginator,
        ListQuestionSetVersionsPaginator,
        ListQuestionSetsPaginator,
        ListScheduleActionsPaginator,
        SearchFixturesPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    feed_deleted_waiter: FeedDeletedWaiter = client.get_waiter("feed_deleted")

    list_dictionaries_paginator: ListDictionariesPaginator = client.get_paginator("list_dictionaries")
    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
    list_question_set_versions_paginator: ListQuestionSetVersionsPaginator = client.get_paginator("list_question_set_versions")
    list_question_sets_paginator: ListQuestionSetsPaginator = client.get_paginator("list_question_sets")
    list_schedule_actions_paginator: ListScheduleActionsPaginator = client.get_paginator("list_schedule_actions")
    search_fixtures_paginator: SearchFixturesPaginator = client.get_paginator("search_fixtures")
    ```
"""

from .client import ElementalInferenceClient
from .paginator import (
    ListDictionariesPaginator,
    ListFeedsPaginator,
    ListFunctionsPaginator,
    ListQuestionSetsPaginator,
    ListQuestionSetVersionsPaginator,
    ListScheduleActionsPaginator,
    SearchFixturesPaginator,
)
from .waiter import FeedDeletedWaiter

Client = ElementalInferenceClient


__all__ = (
    "Client",
    "ElementalInferenceClient",
    "FeedDeletedWaiter",
    "ListDictionariesPaginator",
    "ListFeedsPaginator",
    "ListFunctionsPaginator",
    "ListQuestionSetVersionsPaginator",
    "ListQuestionSetsPaginator",
    "ListScheduleActionsPaginator",
    "SearchFixturesPaginator",
)
