"""On-the-fly credential capture — the agent hits a login it has NO stored
credential for, and instead of asking the human to log in (and seeing the
password), the flow shows the USER a username/password box, the user types, and
the typed values are written to the user's vault as a NEW credential with
AGENT-SUPPLIED METADATA (site name, description, url, and the field map /
selectors the agent identified). The agent never sees the values.

This module is the pure, package-side shape and the branch logic. It carries
NO I/O: the vault WRITE lives in the aidream host (``vault_create_item``), the
user input box lives in the executor (matrx-extend service worker / Cloud
Browser worker), and recipe/attempt persistence lives behind the injected
stores below (S1 ``browser.login_recipe`` / ``browser.login_attempt``).

🚨 THE ONE INVARIANT: no credential VALUE ever appears in this module — not in
an argument, not on a field, not in a return. Everything here is a field KEY, a
selector, a label, a signal descriptor, or a page-HTML capture with values
stripped. The value goes user-box → vault write, and nowhere else.

The known/unknown branch (D-11):

* **KNOWN** — an active ``LoginRecipe`` exists for this origin. The capture
  returns the recipe so the agent maps the exact fields/selectors it already
  knows, and the fields the user must type are driven by the recipe's
  ``field_map``.
* **UNKNOWN** — no recipe. The capture takes the page HTML (redacted) and asks
  the agent, right then, to document the experience / quirks / selectors-by-name
  into a PROPOSED recipe (``build_proposed_recipe``). Proposals are written at
  ``status='proposed'`` and a human activates them (never auto-promoted).
"""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from .recipe import LoginRecipe, RecipeFieldMap, SignalDescriptor

# ─────────────────────────────────────────────────────────────────────────────
# What the agent tells us — metadata ONLY, never a value.
# ─────────────────────────────────────────────────────────────────────────────


class CaptureFieldSpec(BaseModel):
    """One field the agent identified on the login form. ``field_key`` names the
    vault secret the user's typed value will be stored under (``username`` /
    ``password`` / ``account_id`` / …). ``label`` is what to show the user beside
    the input box. ``secret`` decides whether the box masks the typed value.

    There is NO ``value`` here and there never will be — the value is typed by
    the user into the box, not supplied by the agent."""

    model_config = ConfigDict(extra="forbid")

    field_key: str = Field(min_length=1)
    selector: str = Field(min_length=1)
    label: str | None = None
    secret: bool = True
    step: int = 0
    clear_first: bool = True

    def as_recipe_field(self) -> RecipeFieldMap:
        return RecipeFieldMap(
            step=self.step,
            selector=self.selector,
            field_key=self.field_key,
            clear_first=self.clear_first,
        )


class CredentialCaptureSpec(BaseModel):
    """The agent-supplied metadata for a captured credential. Site identity, a
    human description, the login URL, and the field map the agent identified —
    all things the agent legitimately knows. NO credential value rides here."""

    model_config = ConfigDict(extra="forbid")

    display_name: str = Field(min_length=1)  # e.g. "Acme Admin — personal"
    normalized_origin: str = Field(min_length=1)  # scheme://host[:port]
    login_url: str = Field(min_length=1)  # origin + pathname, no query/hash
    description: str | None = None
    provider_key: str | None = None
    fields: list[CaptureFieldSpec] = Field(min_length=1)
    submit_selector: str | None = None
    # URL match mode for future browser-fill (mirrors credential_items.uri_match_mode)
    uri_match_mode: Literal["host", "exact", "never"] = "host"
    notes: str | None = None

    @property
    def field_keys(self) -> list[str]:
        return [f.field_key for f in self.fields]

    @property
    def secret_field_keys(self) -> list[str]:
        return [f.field_key for f in self.fields if f.secret]


class DocumentedRecipeSpec(BaseModel):
    """The agent's documented experience of an UNKNOWN login, offered right after
    a capture so a proposed recipe is written while the page is fresh. Selectors
    and signal descriptors only — never a value, never cookie contents."""

    model_config = ConfigDict(extra="forbid")

    normalized_origin: str = Field(min_length=1)
    match_pattern: str | None = None
    provider_key: str | None = None
    field_map: list[RecipeFieldMap] = Field(min_length=1)
    submit: dict = Field(default_factory=dict)  # same shape as the Attempt submit
    success_signals: list[SignalDescriptor] = Field(default_factory=list)
    failure_signals: list[SignalDescriptor] = Field(default_factory=list)
    challenge_signals: list[SignalDescriptor] = Field(default_factory=list)
    notes: str | None = None


# ─────────────────────────────────────────────────────────────────────────────
# The branch result the agent receives.
# ─────────────────────────────────────────────────────────────────────────────

CaptureBranch = Literal["known", "unknown"]


class CaptureContext(BaseModel):
    """What the tool learns BEFORE showing the user a box — the known/unknown
    branch. On ``known`` the recipe drives the field boxes; on ``unknown`` the
    agent is asked to document a proposed recipe after the write."""

    model_config = ConfigDict(extra="forbid")

    branch: CaptureBranch
    normalized_origin: str
    recipe: LoginRecipe | None = None
    # A prompt telling the agent what to do next (document a recipe on unknown).
    guidance: str


class CaptureReceipt(BaseModel):
    """The receipt handed back to the agent after the user typed and the vault
    write landed. ``proceed`` is the "ready, go" signal. NO value appears."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["captured", "cancelled", "spec_incomplete"] = "captured"
    credential_item_id: str | None = None
    branch: CaptureBranch | None = None
    field_keys: list[str] = Field(default_factory=list)  # NAMES only
    proceed: bool = False
    recipe_id: str | None = None
    recipe_version: int | None = None
    login_attempt_id: str | None = None
    # On unknown, tell the agent to document a recipe right now.
    propose_recipe: bool = False
    guidance: str | None = None
    detail: str | None = None


# ─────────────────────────────────────────────────────────────────────────────
# Persistence seams — the S1 tables are FROZEN but not yet created, so the host
# injects a store. A store that is missing degrades LOUDLY (returns None with a
# reason) rather than silently dropping the proposal.
# ─────────────────────────────────────────────────────────────────────────────


@runtime_checkable
class RecipeStore(Protocol):
    async def get_active_recipe(
        self, normalized_origin: str, path: str = ""
    ) -> LoginRecipe | None: ...

    async def write_proposed_recipe(self, recipe: LoginRecipe) -> str | None:
        """Persist a proposed recipe; return its recipe_id or None if unavailable."""
        ...


@runtime_checkable
class LoginAttemptStore(Protocol):
    async def write_capture_attempt(
        self,
        *,
        actor_id: str,
        run_id: str | None,
        profile_id: str | None,
        normalized_origin: str,
        credential_item_id: str | None,
        field_keys: list[str],
        before_capture_id: str | None,
        after_capture_id: str | None,
        recipe_id: str | None,
        recipe_version: int | None,
    ) -> str | None:
        """Persist a browser.login_attempt row; return its id or None."""
        ...


# ─────────────────────────────────────────────────────────────────────────────
# Pure branch + proposal builders.
# ─────────────────────────────────────────────────────────────────────────────

_UNKNOWN_GUIDANCE = (
    "No login recipe exists for this site yet. After the user enters their "
    "credential, document what you observed — the exact fields and selectors "
    "(by name, never a value), the submit control, and what success, failure and "
    "a challenge look like on THIS page — by calling capture_credential with "
    "action 'propose_recipe'. That proposal turns this fragile guess into a "
    "reliable login next time. A human activates it; you only propose it."
)

_KNOWN_GUIDANCE = (
    "A login recipe exists for this site. Use its field_map selectors and its "
    "success/failure/challenge signals; the user's credential will be stored "
    "under the recipe's field keys."
)


async def resolve_capture_context(
    normalized_origin: str,
    path: str,
    store: RecipeStore | None,
) -> CaptureContext:
    """The known/unknown branch. Consults the recipe store (DB) when present, else
    the seeded package recipes as an offline fallback."""
    recipe: LoginRecipe | None = None
    if store is not None:
        recipe = await store.get_active_recipe(normalized_origin, path)
    if recipe is None:
        # Offline / standalone fallback — the seeded recipes.
        from .recipe import match_seeded_recipe

        recipe = match_seeded_recipe(normalized_origin, path)
    if recipe is not None and recipe.status == "active":
        return CaptureContext(
            branch="known",
            normalized_origin=normalized_origin,
            recipe=recipe,
            guidance=_KNOWN_GUIDANCE,
        )
    return CaptureContext(
        branch="unknown",
        normalized_origin=normalized_origin,
        recipe=None,
        guidance=_UNKNOWN_GUIDANCE,
    )


def build_proposed_recipe(
    documented: DocumentedRecipeSpec,
    *,
    provenance: Literal["human", "hindsight_proposal", "imported"] = "human",
) -> LoginRecipe:
    """Turn an agent's documented experience into a PROPOSED recipe row shape.

    ``provenance='human'`` is correct for a user-captured login the agent
    documented on the user's behalf during a live session — the human was in the
    loop typing the credential. It always lands at ``status='proposed'``; a human
    activates it (recipes are never auto-promoted)."""
    return LoginRecipe(
        normalized_origin=documented.normalized_origin,
        match_pattern=documented.match_pattern,
        provider_key=documented.provider_key,
        field_map=list(documented.field_map),
        submit=dict(documented.submit),
        success_signals=list(documented.success_signals),
        failure_signals=list(documented.failure_signals),
        challenge_signals=list(documented.challenge_signals),
        notes=documented.notes,
        provenance=provenance,
        status="proposed",
    )


__all__ = [
    "CaptureBranch",
    "CaptureContext",
    "CaptureFieldSpec",
    "CaptureReceipt",
    "CredentialCaptureSpec",
    "DocumentedRecipeSpec",
    "LoginAttemptStore",
    "RecipeStore",
    "build_proposed_recipe",
    "resolve_capture_context",
]
