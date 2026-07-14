# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal, TypeAlias

__all__ = ["AgentConfigListMcpToolsResponse"]

AgentConfigListMcpToolsResponse: TypeAlias = List[
    Literal[
        "Slack", "Linear", "GitHub", "Confluence", "Notion", "Datadog", "PagerDuty", "Salesforce", "Figma", "Granola"
    ]
]
