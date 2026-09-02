from pydantic import BaseModel, Field


class ShellExecuteArgs(BaseModel):
    command: str
    working_dir: str = "."
    timeout_seconds: int = Field(default=30, ge=1, le=300)
    allow_network: bool = True


class ShellPythonArgs(BaseModel):
    code: str
    timeout_seconds: int = Field(default=30, ge=1, le=300)
