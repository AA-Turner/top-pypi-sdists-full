"""Client Actions — work the person's browser runs, declared once in the ONE catalog.

The ``client`` engine (``engines.py``) answers every call on the server with
:class:`~matrx_graph.actions.engines.ActionOnClient` ("run this on the client"); the client's
one runner (alchemy ``runSurfaceAction`` with ``runs: "client"``) runs the Action of the SAME
name in the browser. Declaring them here is what puts them in ``GET /actions`` with typed
inputs, so agents and workflows see what a page can do; it never makes the server do them.

Names are the client registry's ids (``kind.<key>`` — the kind action keys a shape's
``runAction(key, input)`` names), so one name reaches the same work from every door.

Host wiring: call :func:`declare_client_actions` once at startup (idempotent).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.actions.decorator import declare_engine_action
from matrx_graph.actions.registry import ActionRegistry, default_action_registry
from matrx_graph.actions.spec import ActionSpec


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ClientActionOutput(BaseModel):
    """What the client answers after it ran a client Action (the kind action envelope)."""

    model_config = ConfigDict(extra="forbid")

    ok: bool
    result: JsonValue = None
    error: str | None = None


class OpenUrlInput(_In):
    url: str = Field(min_length=1, description="The web address to open in a new tab.")


class CopyInput(_In):
    text: str = Field(description="The text to put on the person's clipboard.")


class DownloadInput(_In):
    file_id: str | None = Field(default=None, description="A saved file to download (wins over content).")
    filename: str | None = Field(default=None, description="The name to save under.")
    content: str | None = Field(default=None, description="Text content to save as a file.")
    base64: str | None = Field(default=None, description="Binary content, base64-encoded.")
    mime: str | None = Field(default=None, description="The content's MIME type.")


class PrintInput(_In):
    title: str | None = None
    markdown: str | None = Field(default=None, description="Markdown to print (or pass html).")
    html: str | None = Field(default=None, description="HTML to print (or pass markdown).")


class PlayEmbedInput(_In):
    url: str = Field(min_length=1, description="A provider embed or media address.")
    title: str | None = None


class FileInput(_In):
    file_id: str = Field(min_length=1, description="The saved file.")
    name: str | None = Field(default=None, description="The file's name, shown in the window.")


class LoadMediaInput(_In):
    file_id: str = Field(min_length=1, description="The saved file whose bytes to load.")
    organization_id: str | None = Field(default=None, description="The organization the file lives in.")


class FetchImageInput(_In):
    file_id: str | None = Field(default=None, description="A saved image file (wins over url).")
    url: str | None = Field(default=None, description="A web image address.")


class OpenPlaceInput(_In):
    to: str = Field(
        min_length=1,
        description="A place in the app: a surface name (e.g. 'crm/contact') or an in-app path a surface declares ('/hr').",
    )
    params: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Values for the place's [param] segments, by name (e.g. {'contactId': '…'}). A table's records place "
            "(data/[tableId]) also takes an object `filter` ({column: value}, the rows a count tile counted), a text "
            "`label` (what was clicked) and a `viewId` - exactly what matrx.open(alias, {filter, label}) takes."
        ),
    )


class OpenRecordInput(_In):
    mode: Literal["page", "panel"] | None = Field(
        default=None,
        description=(
            "How to open the card's full record: 'page' (the default) or 'panel'. The record is never given here - the "
            "host answers from the card's OWN saved record, and refuses a card tied to none."
        ),
    )


ClientActionKey = Literal[
    "open_url",
    "open_place",
    "open_record",
    "copy",
    "download",
    "print",
    "play_embed",
    "share_file",
    "open_file",
    "load_media",
    "fetch_image",
]

#: key → (input schema, one-line description). The client registry holds the same keys as ``kind.<key>``.
CLIENT_ACTION_INPUTS: dict[str, tuple[type[BaseModel], str]] = {
    "open_url": (OpenUrlInput, "Open a web address in a new tab on the person's screen."),
    "open_place": (
        OpenPlaceInput,
        "Go to a place in the app (a surface or in-app path from the route registry); an unknown place is refused by name.",
    ),
    "open_record": (
        OpenRecordInput,
        "Open the card's own full saved record; a card tied to no saved record is refused in a sentence.",
    ),
    "copy": (CopyInput, "Copy text to the person's clipboard."),
    "download": (DownloadInput, "Save content or a saved file to the person's device."),
    "print": (PrintInput, "Print a document from markdown or HTML."),
    "play_embed": (PlayEmbedInput, "Open a provider embed or media address in the player window."),
    "share_file": (FileInput, "Open the share window for a saved file."),
    "open_file": (FileInput, "Open a saved file in the file preview window."),
    "load_media": (LoadMediaInput, "Load a saved file's bytes with the reader's own authorization."),
    "fetch_image": (FetchImageInput, "Fetch an image's bytes from a web address or a saved file."),
}


def client_action_name(key: str) -> str:
    """The registered name of a client Action: the client registry's id for the kind action key."""
    return f"kind.{key}"


def declare_client_actions(*, action_registry: ActionRegistry | None = None) -> list[ActionSpec]:
    """Declare every client Action on the registry (idempotent). Returns their specs."""
    registry = action_registry or default_action_registry()
    out: list[ActionSpec] = []
    for key, (schema, description) in CLIENT_ACTION_INPUTS.items():
        name = client_action_name(key)
        if registry.has(name):
            out.append(registry.get(name))
            continue
        out.append(
            declare_engine_action(
                name=name,
                description=description,
                input_schema=schema,
                output_schema=ClientActionOutput,
                engine="client",
                doors=("api",),
                tags=("client",),
                action_registry=registry,
            )
        )
    return out


__all__ = [
    "CLIENT_ACTION_INPUTS",
    "ClientActionKey",
    "ClientActionOutput",
    "client_action_name",
    "declare_client_actions",
]
