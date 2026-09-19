"""Argument models for the ONE action-dispatched ``cloud_browser`` tool.

The nine standalone ``cloud_browser_*`` tools were consolidated into a single
``cloud_browser`` tool on 2026-08-21 (canonical tool-count rule: fewer tools
with actions built in). Each former tool is now one variant of the
``CloudBrowserArgs`` discriminated union, selected by ``action``. Forwarded
constrained-enum arguments match their worker command's accepted values, while
the required ``action`` discriminator selects the applicable public contract.

🚨 S6 (tool surface) invariants still hold on every variant:

  * ``profile_id: str = ""`` on every model — opaque to the model and the tool
    layer; ``""`` means "resolve the acting user's personal default" (S6 §3).
    The tool never parses, validates, prefixes, or infers meaning from it.
  * ``model_config = ConfigDict(extra="forbid")`` on every model — the FIRST of
    two independent layers that make ``user_id`` / ``organization_id`` /
    ``owner_user_id`` / ``org_id`` etc. STRUCTURALLY impossible as arguments
    (S6 §3.3, D-4). A model that invents a principal id gets a Pydantic
    validation error at parse time, before any network call. The second layer is
    the committed test ``test_browser_args_forbid_principal_ids`` — it survives
    someone relaxing ``extra="forbid"``.

The acting user travels on the transport as a signed, audience-bound claim
(D-4), NEVER in a model-authored argument.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

# The single opaque profile argument, appended to every tool. Empty string (not
# None) matches the existing optional-string convention in this module.
_PROFILE_FIELD_DEFAULT = ""


class BrowserNavigateArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["navigate"]
    url: str
    # Keep the public navigate contract identical to the worker command.  A
    # loose string used to reach ``NavigateCommand`` and turn model input such
    # as ``body`` into a production ERROR instead of a normal argument refusal.
    wait_for: Literal["load", "domcontentloaded", "networkidle"] = "load"
    extract_text: bool = True
    session_id: str = ""
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserClickArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["click"]
    selector: str
    session_id: str
    wait_after_ms: int = Field(default=1000, ge=0, le=10000)
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserTypeArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["type_text"]
    selector: str
    text: str
    session_id: str
    clear_first: bool = True
    press_enter: bool = False
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserScreenshotArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["screenshot"]
    session_id: str
    selector: str = ""
    width: int = Field(default=1280, ge=320, le=3840)
    height: int = Field(default=720, ge=240, le=2160)
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserSelectOptionArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["select_option"]
    session_id: str
    selector: str
    value: str = ""
    label: str = ""
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserWaitForArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["wait_for"]
    session_id: str
    selector: str = ""
    text: str = ""
    timeout_ms: int = Field(default=10000, ge=500, le=60000)
    state: Literal["visible", "attached", "detached", "hidden"] = "visible"
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserGetElementArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["get_element"]
    session_id: str
    selector: str
    attributes: list[str] = Field(default_factory=list)
    include_html: bool = False
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserScrollArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["scroll"]
    session_id: str
    direction: Literal["up", "down", "top", "bottom"] = "down"
    amount_px: int = Field(default=500, ge=0, le=10000)
    selector: str = ""
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserCloseArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: Literal["close"]
    session_id: str
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserDismissHandoffArgs(BaseModel):
    """Withdraw a pending human-handoff the AGENT itself opened (e.g. its own
    credential capture card) so the run returns to agent control instead of
    waiting out the TTL. Refused for a person-requested or already-claimed
    handoff — an agent can never cancel a person's takeover."""

    model_config = ConfigDict(extra="forbid")

    action: Literal["dismiss_handoff"]
    session_id: str
    profile_id: str = _PROFILE_FIELD_DEFAULT


class BrowserListProfilesArgs(BaseModel):
    """List the acting user's own cloud browsers so a NAMED one can be opened.

    A person may hold as many browsers as they want (D-28), and until this
    existed the tool had no way to learn their names: "use my work browser"
    could only be guessed at. Call this when the person names a browser, then
    pass the returned ``profile_id`` to ``navigate``.

    ``profile_id`` is kept for S6 uniformity (every variant carries it) and is
    ignored here — the listing is always the acting user's own browsers.
    """

    model_config = ConfigDict(extra="forbid")

    action: Literal["list_profiles"]
    profile_id: str = _PROFILE_FIELD_DEFAULT


CloudBrowserVariant = Annotated[
    BrowserNavigateArgs
    | BrowserClickArgs
    | BrowserTypeArgs
    | BrowserSelectOptionArgs
    | BrowserWaitForArgs
    | BrowserGetElementArgs
    | BrowserScrollArgs
    | BrowserScreenshotArgs
    | BrowserCloseArgs
    | BrowserDismissHandoffArgs
    | BrowserListProfilesArgs,
    Field(discriminator="action"),
]


class CloudBrowserArgs(RootModel[CloudBrowserVariant]):
    """The wire contract of the ONE `cloud_browser` tool (action-dispatched)."""
