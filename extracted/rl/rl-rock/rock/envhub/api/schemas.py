"""EnvHub data model definitions"""

from typing import Any

from pydantic import BaseModel


class EnvInfo(BaseModel):
    """Environment information model"""

    env_name: str
    image: str
    owner: str = ""
    description: str = ""
    tags: list[str] = []
    extra_spec: dict[str, Any] | None = None
    create_at: str | None = None
    update_at: str | None = None


class RegisterRequest(BaseModel):
    """Register environment request"""

    env_name: str
    image: str
    owner: str = ""
    description: str = ""
    tags: list[str] = []
    extra_spec: dict[str, Any] | None = None


class GetEnvRequest(BaseModel):
    """Get environment request"""

    env_name: str


class ListEnvsRequest(BaseModel):
    """List environments request"""

    owner: str | None = None
    tags: list[str] | None = None


class DeleteEnvRequest(BaseModel):
    """Delete environment request"""

    env_name: str
