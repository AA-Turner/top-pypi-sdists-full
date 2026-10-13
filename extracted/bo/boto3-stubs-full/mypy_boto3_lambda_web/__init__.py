"""
Main interface for lambda-web service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lambda_web import (
        Client,
        LambdaWebClient,
        ListWebFunctionEndpointsPaginator,
        ListWebFunctionRevisionsPaginator,
        ListWebFunctionsPaginator,
        WebFunctionActiveWaiter,
        WebFunctionDeletedWaiter,
        WebFunctionEndpointActiveWaiter,
        WebFunctionEndpointDeletedWaiter,
        WebFunctionEndpointUpdatedWaiter,
        WebFunctionRevisionActiveWaiter,
    )

    session = Session()
    client: LambdaWebClient = session.client("lambda-web")

    web_function_active_waiter: WebFunctionActiveWaiter = client.get_waiter("web_function_active")
    web_function_deleted_waiter: WebFunctionDeletedWaiter = client.get_waiter("web_function_deleted")
    web_function_endpoint_active_waiter: WebFunctionEndpointActiveWaiter = client.get_waiter("web_function_endpoint_active")
    web_function_endpoint_deleted_waiter: WebFunctionEndpointDeletedWaiter = client.get_waiter("web_function_endpoint_deleted")
    web_function_endpoint_updated_waiter: WebFunctionEndpointUpdatedWaiter = client.get_waiter("web_function_endpoint_updated")
    web_function_revision_active_waiter: WebFunctionRevisionActiveWaiter = client.get_waiter("web_function_revision_active")

    list_web_function_endpoints_paginator: ListWebFunctionEndpointsPaginator = client.get_paginator("list_web_function_endpoints")
    list_web_function_revisions_paginator: ListWebFunctionRevisionsPaginator = client.get_paginator("list_web_function_revisions")
    list_web_functions_paginator: ListWebFunctionsPaginator = client.get_paginator("list_web_functions")
    ```
"""

from .client import LambdaWebClient
from .paginator import (
    ListWebFunctionEndpointsPaginator,
    ListWebFunctionRevisionsPaginator,
    ListWebFunctionsPaginator,
)
from .waiter import (
    WebFunctionActiveWaiter,
    WebFunctionDeletedWaiter,
    WebFunctionEndpointActiveWaiter,
    WebFunctionEndpointDeletedWaiter,
    WebFunctionEndpointUpdatedWaiter,
    WebFunctionRevisionActiveWaiter,
)

Client = LambdaWebClient


__all__ = (
    "Client",
    "LambdaWebClient",
    "ListWebFunctionEndpointsPaginator",
    "ListWebFunctionRevisionsPaginator",
    "ListWebFunctionsPaginator",
    "WebFunctionActiveWaiter",
    "WebFunctionDeletedWaiter",
    "WebFunctionEndpointActiveWaiter",
    "WebFunctionEndpointDeletedWaiter",
    "WebFunctionEndpointUpdatedWaiter",
    "WebFunctionRevisionActiveWaiter",
)
