"""Credential resolution contract — typed request/response, NO storage, NO crypto.

matrx-connect carries the *shape* of a credential resolution across the
package boundary; it never persists or decrypts anything (Unified Credential
Vault plan, "Package consumers"). The trusted host (aidream) implements
:class:`CredentialResolver` over the matrx-orm secrets battery and injects it
into consumer packages (matrx-ai via ``matrx_ai.configure(credential_resolver=…)``,
matrx-scraper analogously). Consumer packages type-hint against this protocol
and NEVER import the host or the battery.

References are STABLE: ``field_id`` or ``{item_id, field_key}``. Mutable
environment-key strings are the legacy form this contract exists to retire —
they are deliberately not representable here.
"""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, model_validator

CredentialConsumer = Literal["agent", "mcp", "sandbox", "scraper", "integration", "broker"]
CredentialOutput = Literal["value", "headers", "env_map", "token_set"]
CredentialResolutionReason = Literal[
    "resolution_failed", "protected_execution_required", "organization_vault_closed"
]


class CredentialRef(BaseModel):
    """One stable reference: ``field_id`` alone, or ``item_id`` + ``field_key``,
    or ``item_id`` alone (whole item — required for ``env_map``/``token_set``)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    field_id: str | None = None
    item_id: str | None = None
    field_key: str | None = None

    @model_validator(mode="after")
    def _one_valid_form(self) -> CredentialRef:
        if self.field_id is not None:
            if self.item_id is not None or self.field_key is not None:
                raise ValueError("field_id is exclusive with item_id/field_key")
            return self
        if self.item_id is None:
            raise ValueError("a stable reference requires field_id or item_id")
        return self

    @property
    def is_item_level(self) -> bool:
        return self.field_id is None and self.field_key is None


class CredentialRequest(BaseModel):
    """A fully-attributed resolution request. The host authorizes
    ``actor_user_id`` (and org membership when ``organization_id`` is set)
    against the referenced item before any plaintext leaves the battery."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    actor_user_id: str
    organization_id: str | None = None
    ref: CredentialRef
    consumer: CredentialConsumer
    purpose: str
    invocation_id: str | None = None
    output: CredentialOutput = "value"

    @model_validator(mode="after")
    def _output_matches_ref(self) -> CredentialRequest:
        if self.output in ("env_map", "token_set") and not self.ref.is_item_level:
            raise ValueError(f"output={self.output!r} requires an item-level reference")
        if self.output in ("value", "headers") and self.ref.is_item_level:
            raise ValueError(f"output={self.output!r} requires a field-level reference")
        return self


class CredentialResolution(BaseModel):
    """Exactly ONE payload attribute is set, matching the requested output.
    Values are plaintext for immediate in-process use — never persist, log,
    or return them to a browser."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    output: CredentialOutput
    value: str | None = None
    headers: dict[str, str] | None = None
    env_map: dict[str, str] | None = None
    token_set: dict[str, str] | None = None

    @model_validator(mode="after")
    def _payload_matches_output(self) -> CredentialResolution:
        populated = {
            name
            for name in ("value", "headers", "env_map", "token_set")
            if getattr(self, name) is not None
        }
        if populated != {self.output}:
            raise ValueError(
                f"exactly the {self.output!r} payload must be set; got {sorted(populated)}"
            )
        return self


class CredentialResolutionError(PermissionError):
    """Raised by a resolver when the actor is not authorized for the
    reference, the reference does not exist, or the value cannot be
    decrypted. The message must never contain a credential value."""

    def __init__(
        self,
        message: str = "credential resolution failed",
        *,
        code: CredentialResolutionReason = "resolution_failed",
    ) -> None:
        self.code = code
        super().__init__(message)


@runtime_checkable
class CredentialResolver(Protocol):
    """The one host-injected seam consumer packages call for credentials."""

    async def resolve(self, request: CredentialRequest) -> CredentialResolution: ...


__all__ = [
    "CredentialConsumer",
    "CredentialOutput",
    "CredentialResolutionReason",
    "CredentialRef",
    "CredentialRequest",
    "CredentialResolution",
    "CredentialResolutionError",
    "CredentialResolver",
]
