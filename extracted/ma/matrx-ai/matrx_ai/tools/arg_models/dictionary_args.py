"""Argument models for the multi-action ``dictionary`` tool.

One tool, several actions (the house pattern — cf. ``memory`` / ``sql`` / ``web``).
Field sets here mirror the ``tool_def.parameters."$variants"`` DB row; descriptions
live only in the DB (Rule 4). The discriminated union ``DictionaryArgs`` is what
``@tool`` validates each incoming call against.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, Union

from pydantic import Field, RootModel

from matrx_ai.tools.declared import ToolArgs

DictLevel = Literal["user", "organization", "scope_type", "scope"]


class DictListOwnersWire(ToolArgs):
    action: Literal["list_owners"]


class DictListEntriesWire(ToolArgs):
    action: Literal["list_entries"]
    level: DictLevel
    # Optional for level=user (defaults to the calling user).
    owner_id: str = ""


class DictResolveWire(ToolArgs):
    action: Literal["resolve"]
    include_personal: bool = True
    all: bool = False
    organization_ids: list[str] = []
    scope_type_ids: list[str] = []
    scope_ids: list[str] = []


class DictUpsertEntriesWire(ToolArgs):
    action: Literal["upsert_entries"]
    level: DictLevel
    owner_id: str = ""
    # Each: {term, sounds_like?, pronunciation?, ipa?, definition?, category?, is_active?}
    entries: list[dict[str, Any]]


class DictDeleteEntriesWire(ToolArgs):
    action: Literal["delete_entries"]
    level: DictLevel
    owner_id: str = ""
    ids: list[str]


class DictGetSettingsWire(ToolArgs):
    action: Literal["get_settings"]
    level: DictLevel
    owner_id: str = ""


class DictSetSettingsWire(ToolArgs):
    action: Literal["set_settings"]
    level: DictLevel
    owner_id: str = ""
    # null → clear (revert to the 200-char default); 0 → never inline; N → ceiling.
    max_inline_chars: int | None = None


class DictFetchUserContentWire(ToolArgs):
    action: Literal["fetch_user_content"]
    source: Literal["conversations", "notes", "both"] = "both"
    limit: int = Field(default=20, ge=1, le=100)


class DictionaryArgs(
    RootModel[
        Annotated[
            Union[
                DictListOwnersWire,
                DictListEntriesWire,
                DictResolveWire,
                DictUpsertEntriesWire,
                DictDeleteEntriesWire,
                DictGetSettingsWire,
                DictSetSettingsWire,
                DictFetchUserContentWire,
            ],
            Field(discriminator="action"),
        ]
    ]
):
    pass


__all__ = ["DictionaryArgs"]
