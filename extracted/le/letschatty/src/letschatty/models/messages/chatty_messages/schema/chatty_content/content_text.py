from pydantic import BaseModel, field_validator

class ChattyContentText(BaseModel):
    body: str
    preview_url: bool = False

    def get_body_or_caption(self) -> str:
        return self.body

    @field_validator('body', mode='before')
    def fix_line_breaks(cls, v: str) -> str:
        """if there are \\n, replace them with an actual line break"""
        return v.replace("\\n", "\n").replace("↵", "\n")