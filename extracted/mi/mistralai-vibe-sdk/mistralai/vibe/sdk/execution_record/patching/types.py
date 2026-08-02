"""JSON Patch types (RFC 6902) for streaming updates.

Streaming in vibe_sdk uses JSON Patch to send incremental updates to events.
This allows live UI updates during LLM streaming without persisting every chunk.

Usage:
    StreamEvent = Patch[BaseEvent]  # A patch that updates an event
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, RootModel

# Type aliases for JSON Patch
type JsonPointer = str


# JSON Patch operations (RFC 6902)


class AddOp(BaseModel):
    """Add a value to an object or array."""

    op: Literal["add"] = "add"
    path: JsonPointer
    value: JsonValue


class RemoveOp(BaseModel):
    """Remove a value from an object or array."""

    op: Literal["remove"] = "remove"
    path: JsonPointer


class ReplaceOp(BaseModel):
    """Replace a value."""

    op: Literal["replace"] = "replace"
    path: JsonPointer
    value: JsonValue


class MoveOp(BaseModel):
    """Move a value from one location to another."""

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    op: Literal["move"] = "move"
    path: JsonPointer
    from_: JsonPointer = Field(alias="from")


class CopyOp(BaseModel):
    """Copy a value from one location to another."""

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    op: Literal["copy"] = "copy"
    path: JsonPointer
    from_: JsonPointer = Field(alias="from")


class JsonTestOp(BaseModel):
    """Test that a value exists at a path (RFC 6902 "test" operation)."""

    op: Literal["test"] = "test"
    path: JsonPointer
    value: JsonValue


class AppendOp(BaseModel):
    """Append a string to an existing string value (custom extension).

    This is a vibe_sdk extension to RFC 6902. Standard JSON Patch has no
    "append to string" operation, so each text token would require a replace
    with the full accumulated text (O(n) per token). AppendOp sends only the
    delta, making token streaming O(1) per token.

    Clients that do not understand the "append" operation can safely ignore it
    and refetch the current value. RFC 6902 recommends implementations SHOULD
    ignore unrecognized operations.
    """

    op: Literal["append"] = "append"
    path: JsonPointer
    value: str


# Union of all patch operations (discriminated on the "op" field for Pydantic deserialization)
Op = Annotated[
    AddOp | RemoveOp | ReplaceOp | MoveOp | CopyOp | JsonTestOp | AppendOp,
    Field(discriminator="op"),
]


class Patch[M: BaseModel](RootModel[list[Op]]):
    """A JSON Patch document (RFC 6902).

    The phantom type M indicates what type of object the patch applies to.
    This is for documentation and type hints only - not validated at runtime.

    Example:
        patch: Patch[AssistantMessage] = Patch(root=[
            ReplaceOp(path="/payload/content/0/text", value="Hello world")
        ])
    """

    pass


__all__ = [
    "AddOp",
    "AppendOp",
    "CopyOp",
    "JsonPointer",
    "JsonTestOp",
    "MoveOp",
    "Op",
    "Patch",
    "RemoveOp",
    "ReplaceOp",
]
