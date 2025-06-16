from dataclasses import dataclass
from typing import List

from mcp.types import Tool, Resource, ResourceTemplate, Prompt


@dataclass
class ServerCapabilities:
    tools: List[Tool]
    resources: List[Resource | ResourceTemplate]
    prompts: List[Prompt]