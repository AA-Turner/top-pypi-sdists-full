"""
Main interface for socialmessaging service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_socialmessaging import (
        Client,
        EndUserMessagingSocialClient,
        ListLinkedWhatsAppBusinessAccountsPaginator,
        ListWhatsAppFlowAssetsPaginator,
        ListWhatsAppFlowsPaginator,
        ListWhatsAppMessageTemplatesPaginator,
        ListWhatsAppTemplateLibraryPaginator,
    )

    session = Session()
    client: EndUserMessagingSocialClient = session.client("socialmessaging")

    list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    list_whatsapp_flow_assets_paginator: ListWhatsAppFlowAssetsPaginator = client.get_paginator("list_whatsapp_flow_assets")
    list_whatsapp_flows_paginator: ListWhatsAppFlowsPaginator = client.get_paginator("list_whatsapp_flows")
    list_whatsapp_message_templates_paginator: ListWhatsAppMessageTemplatesPaginator = client.get_paginator("list_whatsapp_message_templates")
    list_whatsapp_template_library_paginator: ListWhatsAppTemplateLibraryPaginator = client.get_paginator("list_whatsapp_template_library")
    ```
"""

from .client import EndUserMessagingSocialClient
from .paginator import (
    ListLinkedWhatsAppBusinessAccountsPaginator,
    ListWhatsAppFlowAssetsPaginator,
    ListWhatsAppFlowsPaginator,
    ListWhatsAppMessageTemplatesPaginator,
    ListWhatsAppTemplateLibraryPaginator,
)

Client = EndUserMessagingSocialClient


__all__ = (
    "Client",
    "EndUserMessagingSocialClient",
    "ListLinkedWhatsAppBusinessAccountsPaginator",
    "ListWhatsAppFlowAssetsPaginator",
    "ListWhatsAppFlowsPaginator",
    "ListWhatsAppMessageTemplatesPaginator",
    "ListWhatsAppTemplateLibraryPaginator",
)
