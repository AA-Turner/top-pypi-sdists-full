"""Run one step in another organization the run's person belongs to (``data.in_organization``).

THE GENERAL PROBLEM. A person belongs to several organizations; a run starts in ONE of them. Some
work must happen in each of the others — read, ingest, ask an agent, save — and bill there (a
person's knowledge across their organizations, a cross-organization digest, an agency acting for
several client organizations). Without this setting every step runs, and bills, in the run's own
organization.

Authored on a node (opt-in, per step)::

    "data": {"in_organization": {"input": "organization_id"}}   # a dotted path into the step's
                                                                 # resolved inputs (fan-out item,
                                                                 # edge value, static input)
    "data": {"in_organization": {"organization_id": "<uuid>"}}  # a fixed organization
    "data": {"in_organization": "organization_id"}              # shorthand for {"input": ...}

THE RULES (each one has a test in ``tests/test_in_organization.py``):

* The organization is ADMITTED by the host before the step works, never assumed: the run's person
  (the carried actor, ``ctx.user_id``) must be an active member of it. The engine never compares
  organization ids to decide that; the host's admission seam
  (:func:`configure_organization_switch`) is the one answer. A host that installs none refuses
  every switch, in words — a standalone install never switches unchecked.
* The step's own context carries the target organization for the length of the executor call
  only: every AI call, record write and charge the step makes lands in that organization. The run,
  its events, outcome rows and the steps around it stay in the run's organization.
* The target is named by the step's resolved inputs or its setting — never by a request body,
  never by the person's preferences, the signup organization or a default. A named input that is
  missing or blank REFUSES the step (it never falls back to the run's organization).
* The same organization as the run's → no switch, nothing asked.
* An input the setting reads that the step itself does not take (a fan-out item's
  ``organization_id`` handed to a step whose inputs are closed) is consumed by the setting: it is
  removed before the step's inputs are checked.
* A refusal is a routable step failure (ERROR edge, fan-out hole) carrying one plain sentence.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

_MISSING = object()


class InOrganizationPolicy(BaseModel):
    """A parsed ``data.in_organization`` setting: exactly one of ``input`` / ``organization_id``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    input: str | None = Field(default=None, min_length=1, max_length=200)
    organization_id: str | None = Field(default=None, min_length=1, max_length=64)

    @model_validator(mode="after")
    def _exactly_one(self) -> InOrganizationPolicy:
        if (self.input is None) == (self.organization_id is None):
            raise ValueError("name exactly one of 'input' (a dotted path into the step's inputs) or 'organization_id'")
        if self.organization_id is not None and _as_organization_id(self.organization_id) is None:
            raise ValueError(f"organization_id {self.organization_id!r} is not an organization id")
        return self


def _as_organization_id(value: str) -> str | None:
    """The canonical (lowercase) form of an organization id, or None when ``value`` is not one."""
    try:
        return str(UUID(value.strip()))
    except (ValueError, AttributeError):
        return None


def parse_in_organization(raw: Any) -> InOrganizationPolicy | None:
    """``data.in_organization`` → :class:`InOrganizationPolicy`; None when absent. Raises ``ValueError``
    on a malformed setting — the compiler turns it into a CompilationError."""
    if raw is None or raw is False or raw == "":
        return None
    if isinstance(raw, str):
        return InOrganizationPolicy(input=raw)
    if not isinstance(raw, dict):
        raise ValueError(f"expected an object or an input path, got {type(raw).__name__}")
    return InOrganizationPolicy.model_validate(raw)


class OrganizationNotAdmitted(Exception):  # noqa: N818 — a refusal, named for what the person reads
    """The step may not run in the organization it names. ``person_message`` is the sentence shown."""

    def __init__(self, person_message: str, *, organization_id: str | None = None, reason: str = "refused") -> None:
        super().__init__(person_message)
        self.person_message = person_message
        self.organization_id = organization_id
        self.reason = reason
        self.node_error_details = {"in_organization": organization_id, "reason": reason}


#: The host's admission: ``(step app context, target organization id) -> async context manager``
#: yielding the step's context IN that organization (actor carried), or raising
#: :class:`OrganizationNotAdmitted` when the actor is not a member.
OrganizationSwitch = Callable[[Any, str], AbstractAsyncContextManager[Any]]

_switch: OrganizationSwitch | None = None


def configure_organization_switch(fn: OrganizationSwitch | None) -> OrganizationSwitch | None:
    """Install the host's admission + context seam (returns the previous one; None uninstalls)."""
    global _switch
    previous, _switch = _switch, fn
    return previous


def organization_switch() -> OrganizationSwitch | None:
    return _switch


def _read_path(inputs: dict[str, Any], path: str) -> Any:
    value: Any = inputs
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return _MISSING
        value = value[part]
    return value


def target_organization(policy: InOrganizationPolicy, inputs: dict[str, Any]) -> str:
    """The organization this invocation runs in. Raises :class:`OrganizationNotAdmitted` when the
    named input is missing or blank — the step never falls back to the run's organization."""
    if policy.organization_id is not None:
        return str(_as_organization_id(policy.organization_id))
    value = _read_path(inputs, str(policy.input))
    if value is _MISSING or value is None or not str(value).strip():
        raise OrganizationNotAdmitted(
            f"This step runs in the organization named by '{policy.input}', but it got none, so it did not run.",
            reason="no_organization",
        )
    organization_id = _as_organization_id(value) if isinstance(value, str) else None
    if organization_id is None:
        # Refused here, typed and in words — never handed to the host's membership read, where a
        # malformed id surfaced as a raw database error instead of a refusal.
        raise OrganizationNotAdmitted(
            f"This step runs in the organization named by '{policy.input}', but that is not an organization id, "
            "so it did not run.",
            reason="not_an_organization_id",
        )
    return organization_id


def consume_setting_input(policy: InOrganizationPolicy, inputs: dict[str, Any], schema: type[BaseModel]) -> dict[str, Any]:
    """Drop the top-level input the setting reads when the step itself does not take it."""
    if policy.input is None:
        return inputs
    head = policy.input.split(".", 1)[0]
    if head not in inputs or head in schema.model_fields:
        return inputs
    return {k: v for k, v in inputs.items() if k != head}


@asynccontextmanager
async def in_organization(ctx: Any, organization_id: str) -> AsyncIterator[None]:
    """Run the enclosed executor call with ``ctx`` (a NodeExecutionContext) in ``organization_id``.

    Same organization as the step's own → nothing changes. Otherwise the host admits the run's person
    and mints the context; ``ctx.app`` and the ambient AppContext carry it until the block ends."""
    current = str(getattr(ctx.app, "organization_id", "") or "").strip().lower()
    if organization_id.strip().lower() == current:
        yield
        return
    switch = _switch
    if switch is None:
        raise OrganizationNotAdmitted(
            "This step is set to run in another organization, but this server cannot check membership "
            "of another organization, so it did not run.",
            organization_id=organization_id,
            reason="no_admission_seam",
        )
    if not str(getattr(ctx.app, "user_id", "") or ""):
        raise OrganizationNotAdmitted(
            "This step is set to run in another organization, but the run has no person to admit there, "
            "so it did not run.",
            organization_id=organization_id,
            reason="no_actor",
        )
    async with switch(ctx.app, organization_id) as switched:
        if str(getattr(switched, "organization_id", "") or "") != organization_id:
            raise OrganizationNotAdmitted(
                "The server could not open the organization this step names, so it did not run.",
                organization_id=organization_id,
                reason="switch_mismatch",
            )
        token = None
        try:
            from matrx_connect.context.app_context import clear_app_context, set_app_context

            token = set_app_context(switched)
        except ImportError:  # pragma: no cover — matrx-connect is a hard dependency
            clear_app_context = None  # type: ignore[assignment]
        previous = ctx.app
        ctx.app = switched
        try:
            yield
        finally:
            ctx.app = previous
            if token is not None and clear_app_context is not None:
                try:
                    clear_app_context(token)
                except (ValueError, LookupError):
                    pass


async def admit_organization(ctx: Any, organization_id: str) -> None:
    """Admit the run's person to ``organization_id`` now, without running anything there.

    The scheduler asks this BEFORE anything that can stand in for the executor call — a saved
    result reused by ``data.once`` is handed out before ``in_organization`` would ever be entered,
    so without this a person who is not a member received what a member's run saved there."""
    async with in_organization(ctx, organization_id):
        pass


__all__ = [
    "InOrganizationPolicy",
    "admit_organization",
    "OrganizationNotAdmitted",
    "OrganizationSwitch",
    "configure_organization_switch",
    "consume_setting_input",
    "in_organization",
    "organization_switch",
    "parse_in_organization",
    "target_organization",
]
