"""Workspace variables — the configuration a run reads at execution time.

Variables live on the workspace's data plane rather than with the rest of its
record. Reaching them asks nothing of the caller: the SDK obtains and renews
the access they need.
"""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Awaitable, Final, Mapping, Sequence, overload

# Current package
from dlthub_sdk._glue.base import Namespace
from dlthub_sdk._glue.context import Async, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind, StrEnum
from dlthub_sdk._glue.keep import KEEP, Keep
from dlthub_sdk.errors import InvalidResponse, NotFound

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.dataplane_api.models import (
        PlainPublicVariable,
        ScopeVariablesResponse,
        SecretPublicVariable,
        VariablesChangeResponse,
        WorkspaceVariablesResponse,
    )

    VariablePayload = PlainPublicVariable | SecretPublicVariable

#: The scope no profile owns: variables every profile inherits. Pass it as
#: ``profile`` to read only that scope.
WORKSPACE_PROFILE: Final[None] = None


class VariableChangeStatus(StrEnum):
    """What became of one name in a change.

    Attributes:
        UPSERTED: Stored, whether it existed before or not.
        REMOVED: Deleted.
        NOT_FOUND: Asked to be deleted, but was not there.
        UNKNOWN: A status this SDK version does not know.
    """

    UPSERTED = "upserted"
    REMOVED = "removed"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class VariableChange:
    """What a change did to one name.

    Attributes:
        name: The variable named in the request.
        status: What the platform did with it.
    """

    name: str
    status: VariableChangeStatus

    @staticmethod
    def _all_from_payload(
        _ctx: _Ctx[Any], payload: VariablesChangeResponse
    ) -> tuple[VariableChange, ...]:
        return tuple(
            VariableChange(name=r.name, status=VariableChangeStatus(str(r.status)))
            for r in payload.results
        )


@dataclass(frozen=True)
class Variable:
    """One variable, as the platform reports it.

    A secret's ``value`` is ``None`` because it is withheld, not empty.

    Attributes:
        name: The variable's name, unique within its scope.
        secret: Whether the platform stores it as a secret.
        value: The value, or ``None`` for a secret.
        created_at: When it was first set.
        created_by: Who first set it.
        updated_at: When it was last changed.
        updated_by: Who last changed it.
    """

    name: str
    secret: bool
    value: str | None
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    @staticmethod
    def _from_payload(payload: VariablePayload) -> Variable:
        secret = str(payload.type_) == "secret"
        raw = getattr(payload, "value", None)
        return Variable(
            name=payload.name,
            secret=secret,
            value=None if secret or not isinstance(raw, str) else raw,
            created_at=payload.created_at,
            created_by=str(payload.created_by),
            updated_at=payload.updated_at,
            updated_by=str(payload.updated_by),
        )


@dataclass(frozen=True)
class VariableScope:
    """The variables one profile sees, or the workspace-level set.

    Attributes:
        profile: The profile these belong to, or ``None`` for the
            workspace-level scope every profile inherits.
        variables: The scope's variables, in the platform's order.
    """

    profile: str | None
    variables: tuple[Variable, ...]

    @staticmethod
    def _from_payload(payload: ScopeVariablesResponse) -> VariableScope:
        return VariableScope(
            profile=payload.profile,
            variables=tuple(Variable._from_payload(v) for v in payload.variables),
        )

    @staticmethod
    def _all_from_payload(
        _ctx: _Ctx[Any], payload: WorkspaceVariablesResponse
    ) -> tuple[VariableScope, ...]:
        return tuple(VariableScope._from_payload(s) for s in payload.scopes)


class Variables(Namespace[M]):
    """The variables of one workspace, across its scopes.

    A whole scope is read at once — there is no paging and no per-variable
    address.
    """

    @overload
    def list(
        self: Variables[Sync], *, profile: str | None | Keep = KEEP
    ) -> tuple[VariableScope, ...]: ...

    @overload
    def list(
        self: Variables[Async], *, profile: str | None | Keep = KEEP
    ) -> Awaitable[tuple[VariableScope, ...]]: ...

    def list(
        self, *, profile: str | None | Keep = KEEP
    ) -> tuple[VariableScope, ...] | Awaitable[tuple[VariableScope, ...]]:
        """Read the workspace's variables, by scope.

        Args:
            profile: Omit for every scope. Pass a profile name for that
                profile's scope, or :data:`WORKSPACE_PROFILE` for the
                workspace-level one.

        Returns:
            One entry per scope read, always as scopes even when one was
            selected; awaitable in async mode.

        Raises:
            NotAuthorized: The caller may not read this workspace's variables.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        # One argument in, so the wire's exclusive pair cannot both be set.
        workspace = profile is None
        wanted: str | Keep = KEEP if profile is None else profile
        return self._ctx.run(
            lambda t: t.list_variables(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                profile=wanted,
                workspace=workspace,
            ),
            VariableScope._all_from_payload,
        )

    @overload
    def apply(
        self: Variables[Sync],
        *,
        profile: str | None,
        upserts: Mapping[str, str] | None = None,
        secrets: Mapping[str, str] | None = None,
        deletes: Sequence[str] | None = None,
    ) -> tuple[VariableChange, ...]: ...

    @overload
    def apply(
        self: Variables[Async],
        *,
        profile: str | None,
        upserts: Mapping[str, str] | None = None,
        secrets: Mapping[str, str] | None = None,
        deletes: Sequence[str] | None = None,
    ) -> Awaitable[tuple[VariableChange, ...]]: ...

    def apply(
        self,
        *,
        profile: str | None,
        upserts: Mapping[str, str] | None = None,
        secrets: Mapping[str, str] | None = None,
        deletes: Sequence[str] | None = None,
    ) -> tuple[VariableChange, ...] | Awaitable[tuple[VariableChange, ...]]:
        """Store and remove variables in one scope, in a single request.

        Args:
            profile: The scope to write to, or :data:`WORKSPACE_PROFILE` for the
                workspace-level one. Required: a write always names one scope.
            upserts: Names and values to store as plain text.
            secrets: Names and values to store as secrets.
            deletes: Names to remove. Removing an absent name is reported, not
                raised.

        Returns:
            One result per name in the request; awaitable in async mode.

        Raises:
            ValueError: Nothing to do, or a name appears in more than one of the
                three arguments, where the outcome would be undefined.
            NotAuthorized: The caller may not write this workspace's variables.
            ScopeMissing: Reached without a workspace in scope.
        """
        plain = dict(upserts or {})
        hidden = dict(secrets or {})
        removed = list(deletes or ())
        if not plain and not hidden and not removed:
            raise ValueError("pass upserts, secrets or deletes — one must be set")
        for label, first, second in (
            ("upserts and secrets", plain, hidden),
            ("upserts and deletes", plain, set(removed)),
            ("secrets and deletes", hidden, set(removed)),
        ):
            clash = sorted(set(first) & set(second))
            if clash:
                raise ValueError(f"{clash} named in both {label}")
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.change_variables(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                profile=profile,
                plain=plain,
                secret=hidden,
                deletes=removed,
            ),
            VariableChange._all_from_payload,
        )

    @overload
    def set(
        self: Variables[Sync],
        name: str,
        value: str,
        *,
        profile: str | None,
        secret: bool = False,
    ) -> VariableChange: ...

    @overload
    def set(
        self: Variables[Async],
        name: str,
        value: str,
        *,
        profile: str | None,
        secret: bool = False,
    ) -> Awaitable[VariableChange]: ...

    def set(
        self,
        name: str,
        value: str,
        *,
        profile: str | None,
        secret: bool = False,
    ) -> VariableChange | Awaitable[VariableChange]:
        """Store one variable.

        Args:
            name: The variable's name.
            value: Its value.
            profile: The scope to write to, or :data:`WORKSPACE_PROFILE`.
            secret: Store it as a secret, so reads never return the value.

        Returns:
            What the platform did with it; awaitable in async mode.

        Raises:
            NotAuthorized: The caller may not write this workspace's variables.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        pair = {name: value}
        return self._ctx.run(
            lambda t: t.change_variables(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                profile=profile,
                plain={} if secret else pair,
                secret=pair if secret else {},
                deletes=(),
            ),
            _one_change,
        )

    @overload
    def delete(
        self: Variables[Sync], name: str, *, profile: str | None
    ) -> VariableChange: ...

    @overload
    def delete(
        self: Variables[Async], name: str, *, profile: str | None
    ) -> Awaitable[VariableChange]: ...

    def delete(
        self, name: str, *, profile: str | None
    ) -> VariableChange | Awaitable[VariableChange]:
        """Remove one variable.

        Args:
            name: The variable's name.
            profile: The scope to remove it from, or :data:`WORKSPACE_PROFILE`.

        Returns:
            What the platform did; a name that was not there comes back as
            :data:`VariableChangeStatus.NOT_FOUND` rather than raising.
            Awaitable in async mode.

        Raises:
            NotAuthorized: The caller may not write this workspace's variables.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.change_variables(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                profile=profile,
                plain={},
                secret={},
                deletes=(name,),
            ),
            _one_change,
        )

    @overload
    def get(self: Variables[Sync], name: str, *, profile: str | None) -> Variable: ...

    @overload
    def get(
        self: Variables[Async], name: str, *, profile: str | None
    ) -> Awaitable[Variable]: ...

    def get(self, name: str, *, profile: str | None) -> Variable | Awaitable[Variable]:
        """Return one variable from one scope.

        There is no single-variable endpoint, so this reads the whole scope.

        Args:
            name: The variable's name.
            profile: The scope to read, or :data:`WORKSPACE_PROFILE`.

        Returns:
            The variable; awaitable in async mode.

        Raises:
            NotFound: No variable of that name in that scope.
            NotAuthorized: The caller may not read this workspace's variables.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.list_variables(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                profile=KEEP if profile is None else profile,
                workspace=profile is None,
            ),
            lambda ctx, payload: _named(name, payload, ctx),
        )


def _one_change(ctx: _Ctx[Any], payload: VariablesChangeResponse) -> VariableChange:
    """Unwrap a single-name change.

    Args:
        ctx: The calling context.
        payload: The change response, which carries one result.

    Returns:
        That result.

    Raises:
        InvalidResponse: The platform reported no result for the name.
    """
    changes = VariableChange._all_from_payload(ctx, payload)
    if not changes:
        raise InvalidResponse("the platform reported no result for the change")
    return changes[0]


def _named(name: str, payload: WorkspaceVariablesResponse, ctx: _Ctx[Any]) -> Variable:
    """Pick one variable out of a scope read.

    Args:
        name: The variable to find.
        payload: The scopes the platform returned.
        ctx: The calling context.

    Returns:
        The matching variable.

    Raises:
        NotFound: No variable of that name in the scope read.
    """
    for scope in VariableScope._all_from_payload(ctx, payload):
        for variable in scope.variables:
            if variable.name == name:
                return variable
    raise NotFound(EntityKind.VARIABLE, name)
