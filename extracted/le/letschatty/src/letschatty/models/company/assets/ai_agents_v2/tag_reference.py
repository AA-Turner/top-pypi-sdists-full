from typing import Literal, Optional

from letschatty.models.base_models.ai_agent_component import (
    AiAgentComponent,
    AiAgentComponentType,
)
from letschatty.models.utils.types.identifier import StrObjectId


class TagReference(AiAgentComponent):
    type: Literal[AiAgentComponentType.TAG] = AiAgentComponentType.TAG
    tag_id: StrObjectId
    untag_description: Optional[str] = None
    ai_description_override: Optional[str] = None
