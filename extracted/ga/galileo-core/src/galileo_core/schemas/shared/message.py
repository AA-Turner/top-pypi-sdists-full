from typing import List, Union

from pydantic import BaseModel, ConfigDict

from galileo_core.schemas.shared.content_parts import FileContentPart, MessageContent, TextContentPart
from galileo_core.schemas.shared.message_role import MessageRole


class Message(BaseModel):
    content: MessageContent
    role: Union[str, MessageRole]

    model_config = ConfigDict(extra="allow")

    @property
    def message(self) -> str:
        role = self.role.value if isinstance(self.role, MessageRole) else self.role
        if isinstance(self.content, str):
            return f"{role}: {self.content}"
        parts: List[str] = []
        for part in self.content:
            if isinstance(part, TextContentPart):
                parts.append(part.text)
            elif isinstance(part, FileContentPart):
                parts.append(f"[file:{part.file_id}]")
        return f"{role}: {''.join(parts)}"
