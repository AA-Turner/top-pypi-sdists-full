from pydantic import BaseModel


class SandboxMeta(BaseModel):
    sandbox_id: str
    sandbox_ref: object
