"""
Main interface for bedrock-data-automation-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_data_automation_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_data_automation_runtime import (
        Client,
        RuntimeforBedrockDataAutomationClient,
    )

    session = get_session()
    async with session.create_client("bedrock-data-automation-runtime") as client:
        client: RuntimeforBedrockDataAutomationClient
        ...

    ```
"""

from .client import RuntimeforBedrockDataAutomationClient

Client = RuntimeforBedrockDataAutomationClient

__all__ = ("Client", "RuntimeforBedrockDataAutomationClient")
