from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, RootModel

from matrx_ai.tools.declared import ToolArgs


class MemoryStoreArgs(BaseModel):
    key: str
    content: str
    memory_type: str = "long"
    scope: str = "user"
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class MemoryRecallArgs(BaseModel):
    key: str = ""
    query: str = ""
    memory_type: str | None = None
    scope: str = "user"
    limit: int = Field(default=5, ge=1, le=20)


class MemorySearchArgs(BaseModel):
    query: str
    scope: str = "user"
    memory_type: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


class MemoryUpdateArgs(BaseModel):
    key: str
    content: str
    scope: str = "user"
    importance: float | None = Field(default=None, ge=0.0, le=1.0)


class MemoryForgetArgs(BaseModel):
    key: str
    scope: str = "user"


# ── Per-action wire contract for the `memory` dispatcher ────────────────────
# The models the executor validates each incoming `memory` call against, assembled
# into the discriminated-union RootModel `MemoryArgs` registered with @tool. Field
# sets == tool_def.parameters "$variants". The plain Memory*Args models above stay
# as inner worker-arg models. Descriptions live only in the DB (Rule 4).


class MemoryRecallWire(ToolArgs):
    action: Literal["recall"]
    key: str = ""
    query: str = ""
    memory_type: str | None = None
    scope: str = "user"
    limit: int = Field(default=5, ge=1, le=20)


class MemorySearchWire(ToolArgs):
    action: Literal["search"]
    query: str
    scope: str = "user"
    memory_type: str | None = None
    limit: int = 10


class MemoryStoreWire(ToolArgs):
    action: Literal["store"]
    key: str
    content: str
    memory_type: str = "long"
    scope: str = "user"
    importance: float = 0.5


class MemoryUpdateWire(ToolArgs):
    action: Literal["update"]
    key: str
    content: str
    scope: str = "user"
    importance: float | None = None


class MemoryForgetWire(ToolArgs):
    action: Literal["forget"]
    key: str
    scope: str = "user"


class MemoryArgs(RootModel[Annotated[
    Union[MemoryRecallWire, MemorySearchWire, MemoryStoreWire,
          MemoryUpdateWire, MemoryForgetWire],
    Field(discriminator="action"),
]]):
    pass
