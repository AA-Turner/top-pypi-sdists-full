"""
Main interface for socialmessaging service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_socialmessaging import (
        Client,
        EndUserMessagingSocialClient,
        ListLinkedWhatsAppBusinessAccountsPaginator,
        ListWhatsAppFlowAssetsPaginator,
        ListWhatsAppFlowsPaginator,
        ListWhatsAppMessageTemplatesPaginator,
        ListWhatsAppTemplateLibraryPaginator,
    )

    session = get_session()
    async with session.create_client("socialmessaging") as client:
        client: EndUserMessagingSocialClient
        ...


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
