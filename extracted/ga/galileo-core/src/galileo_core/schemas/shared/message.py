from typing import Union

from pydantic import BaseModel, ConfigDict

from galileo_core.schemas.shared.message_role import MessageRole


class Message(BaseModel):
    content: str
    role: Union[str, MessageRole]

    model_config = ConfigDict(extra="allow")

    @property
    def message(self) -> str:
        role = self.role.value if isinstance(self.role, MessageRole) else self.role
        return f"{role}: {self.content}"
