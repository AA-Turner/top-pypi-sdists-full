# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "Mcp",
    "AllowedTools",
    "AllowedToolsMcpAllowedToolsMcpAllowedToolsFilter",
    "RequireApproval",
    "RequireApprovalMcpRequireApprovalMcpToolApprovalFilter",
    "RequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways",
    "RequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever",
]


class AllowedToolsMcpAllowedToolsMcpAllowedToolsFilter(BaseModel):
    tool_names: Optional[List[str]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


AllowedTools: TypeAlias = Union[List[str], AllowedToolsMcpAllowedToolsMcpAllowedToolsFilter]


class RequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways(BaseModel):
    tool_names: Optional[List[str]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class RequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever(BaseModel):
    tool_names: Optional[List[str]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class RequireApprovalMcpRequireApprovalMcpToolApprovalFilter(BaseModel):
    always: Optional[RequireApprovalMcpRequireApprovalMcpToolApprovalFilterAlways] = None

    never: Optional[RequireApprovalMcpRequireApprovalMcpToolApprovalFilterNever] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


RequireApproval: TypeAlias = Union[RequireApprovalMcpRequireApprovalMcpToolApprovalFilter, Literal["always", "never"]]


class Mcp(BaseModel):
    server_label: str

    server_url: str

    type: Literal["mcp"]

    allowed_tools: Optional[AllowedTools] = None

    headers: Optional[Dict[str, str]] = None

    require_approval: Optional[RequireApproval] = None

    server_description: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
