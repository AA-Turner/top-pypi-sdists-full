"""Remote-control bridge from messaging surfaces into the CLI runtime."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path
import threading
from typing import Any, Protocol

from apps.cli.runtime import CliRuntime
from packages.contracts.runtime import SessionState
from packages.gateway_core import GatewayInboundMessage


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _mapping(value: object) -> Mapping[str, object] | None:
    return value if isinstance(value, Mapping) else None


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _abbreviate_identifier(value: str, *, head: int = 12, tail: int = 6) -> str:
    text = value.strip()
    if not text:
        return ""
    if tail <= 0:
        return text if len(text) <= head else f"{text[:head]}…"
    if len(text) <= head + tail + 1:
        return text
    return f"{text[:head]}…{text[-tail:]}"


class CliRuntimeLike(Protocol):
    def list_clones(self, *, limit: int = 12) -> tuple[object, ...]:
        ...

    def latest_session_for_clone(self, clone_id: str) -> SessionState | None:
        ...

    def session_ids_for_clone(self, clone_id: str) -> tuple[str, ...]:
        ...

    def create_clone(
        self,
        *,
        clone_id: str,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
        session_id: str | None = None,
    ) -> SessionState:
        ...

    def inspect_session(self, session_id: str) -> SessionState:
        ...

    def prepare_session_surface(self, session_id: str) -> SessionState:
        ...

    def explain_next_step(
        self,
        *,
        session_id: str,
        prompt: str,
        goal_query: str | None = None,
        tool_name: str | None = None,
        tool_arguments: Mapping[str, Any] | None = None,
        delivery_payload: Mapping[str, Any] | None = None,
    ) -> Any:
        ...

    def wake(self, session_id: str, *, inspect_only: bool = False) -> Any:
        ...

    def compact_session_context(
        self,
        session_id: str,
        *,
        reason: str = "gateway-hygiene",
        force: bool = False,
    ) -> Any:
        ...


CliRuntimeFactory = Callable[[Path, Path], CliRuntimeLike]


@dataclass(frozen=True, slots=True)
class GatewayCliControlConfig:
    profile_dir: str | None = None
    state_dir: str | None = None
    default_clone_id: str | None = None
    default_session_id: str | None = None
    auto_create_clone: bool = False
    allow_group_chats: bool = False


@dataclass(frozen=True, slots=True)
class GatewayCliBinding:
    account_id: str
    conversation_id: str
    clone_id: str
    updated_at: str
    session_id: str | None = None


@dataclass(slots=True)
class GatewayCliBindingStore:
    path: Path | None = None
    _bindings: dict[str, GatewayCliBinding] = field(default_factory=dict, init=False, repr=False)
    _lock: threading.RLock = field(default_factory=threading.RLock, init=False, repr=False)

    def __post_init__(self) -> None:
        with self._lock:
            self._bindings = self._load()

    def get(self, *, account_id: str, conversation_id: str) -> GatewayCliBinding | None:
        with self._lock:
            return self._bindings.get(self._key(account_id, conversation_id))

    def set(
        self,
        *,
        account_id: str,
        conversation_id: str,
        clone_id: str,
        session_id: str | None = None,
    ) -> GatewayCliBinding:
        with self._lock:
            binding = GatewayCliBinding(
                account_id=account_id,
                conversation_id=conversation_id,
                clone_id=clone_id,
                session_id=session_id,
                updated_at=_utc_now().isoformat(),
            )
            self._bindings[self._key(account_id, conversation_id)] = binding
            self._persist()
            return binding

    def _key(self, account_id: str, conversation_id: str) -> str:
        return f"{account_id}:{conversation_id}"

    def _load(self) -> dict[str, GatewayCliBinding]:
        if self.path is None or not self.path.exists():
            return {}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        items = payload.get("bindings")
        if not isinstance(items, list):
            return {}
        loaded: dict[str, GatewayCliBinding] = {}
        for item in items:
            if not isinstance(item, dict):
                continue
            try:
                binding = GatewayCliBinding(
                    account_id=str(item["account_id"]),
                    conversation_id=str(item["conversation_id"]),
                    clone_id=str(item["clone_id"]),
                    session_id=_optional_text(item.get("session_id")),
                    updated_at=str(item["updated_at"]),
                )
            except KeyError:
                continue
            loaded[self._key(binding.account_id, binding.conversation_id)] = binding
        return loaded

    def _persist(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "bindings": [
                asdict(binding)
                for binding in sorted(
                    self._bindings.values(),
                    key=lambda item: (item.account_id, item.conversation_id),
                )
            ]
        }
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


@dataclass(frozen=True, slots=True)
class GatewayCliControlResult:
    body: str | None
    clone_id: str | None = None
    session_id: str | None = None
    handled: bool = True
    summary: str | None = None


def load_gateway_cli_control_config(
    manifest: Mapping[str, object],
    *,
    adapter_key: str,
) -> GatewayCliControlConfig | None:
    gateway_payload = _mapping(manifest.get("gateway")) or {}
    adapters_payload = _mapping(gateway_payload.get("adapters")) or {}
    adapter_payload = _mapping(adapters_payload.get(adapter_key)) or {}
    control_payload = _mapping(adapter_payload.get("control"))
    if control_payload is None:
        return None
    return GatewayCliControlConfig(
        profile_dir=_optional_text(control_payload.get("profile_dir")),
        state_dir=_optional_text(control_payload.get("state_dir")),
        default_clone_id=_optional_text(control_payload.get("default_clone_id")),
        default_session_id=_optional_text(control_payload.get("default_session_id")),
        auto_create_clone=bool(control_payload.get("auto_create_clone", False)),
        allow_group_chats=bool(control_payload.get("allow_group_chats", False)),
    )


def load_feishu_cli_control_config(manifest: Mapping[str, object]) -> GatewayCliControlConfig:
    config = load_gateway_cli_control_config(manifest, adapter_key="feishu")
    return config if config is not None else GatewayCliControlConfig()


@dataclass(slots=True)
class GatewayCliControlService:
    config: GatewayCliControlConfig
    runtime_factory: CliRuntimeFactory | None = None
    binding_store: GatewayCliBindingStore | None = None
    surface_label: str = "Gateway"
    binding_subject: str = "conversation"
    direct_chat_types: tuple[str | None, ...] = (None, "direct")
    direct_message_label: str = "direct message"
    control_config_path: str = "gateway.adapters.gateway.control"
    _runtime: CliRuntimeLike | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.binding_store is None:
            self.binding_store = GatewayCliBindingStore()

    def describe(self) -> Mapping[str, object]:
        clones: tuple[str, ...] = ()
        runtime_status = "uninitialized"
        error: str | None = None
        try:
            runtime = self.runtime()
        except RuntimeError as exc:
            runtime_status = "misconfigured"
            error = str(exc)
        else:
            runtime_status = "ready"
            clones = tuple(getattr(item, "clone_id", "") for item in runtime.list_clones(limit=8))
        return {
            "enabled": True,
            "runtime": "cli-runtime",
            "profile_dir": self.config.profile_dir,
            "state_dir": self.config.state_dir,
            "default_clone_id": self.config.default_clone_id,
            "default_session_id": self.config.default_session_id,
            "auto_create_clone": self.config.auto_create_clone,
            "allow_group_chats": self.config.allow_group_chats,
            "runtime_status": runtime_status,
            "runtime_error": error,
            "known_clones": clones,
        }

    def handle_message(self, inbound: GatewayInboundMessage) -> GatewayCliControlResult:
        if inbound.sender.is_bot:
            return GatewayCliControlResult(
                body=None,
                handled=False,
                summary="ignored bot sender",
            )
        if not self.config.allow_group_chats and inbound.chat_type not in self.direct_chat_types:
            return GatewayCliControlResult(
                body=(
                    f"{self.surface_label} remote control currently supports private chats only. "
                    f"Move this conversation to a {self.direct_message_label} or enable "
                    f"`{self.control_config_path}.allow_group_chats`."
                ),
                summary="group chat blocked",
            )

        body = inbound.body.strip()
        command, argument = self._parse_command(body)
        try:
            if command:
                return self._handle_command(inbound, command=command, argument=argument)

            runtime = self.runtime()
            clone_id, session, _ = self._session_selection(runtime, inbound)
            if clone_id is None or session is None:
                return GatewayCliControlResult(
                    body=self._clone_selection_hint(runtime),
                    summary="no clone binding",
                )

            assert self.binding_store is not None
            runtime.prepare_session_surface(session.session_id)
            outcome = runtime.explain_next_step(
                session_id=session.session_id,
                prompt=body,
                delivery_payload={"summary": f"{inbound.adapter_id}:{inbound.event_id}"},
            )
            compact = getattr(runtime, "compact_session_context", None)
            if callable(compact):
                compact(session.session_id, reason="gateway-hygiene", force=False)
            self.binding_store.set(
                account_id=inbound.account_id,
                conversation_id=inbound.conversation_id,
                clone_id=clone_id,
                session_id=session.session_id,
            )
            return GatewayCliControlResult(
                body=str(outcome.execution.summary),
                clone_id=clone_id,
                session_id=session.session_id,
                summary="forwarded to cli runtime",
            )
        except (RuntimeError, KeyError, ValueError) as exc:
            return GatewayCliControlResult(
                body=str(exc),
                summary="control error",
            )

    def runtime(self) -> CliRuntimeLike:
        if self._runtime is not None:
            return self._runtime
        if self.runtime_factory is None:
            if self.config.profile_dir is None or self.config.state_dir is None:
                raise RuntimeError(
                    f"{self.control_config_path} requires profile_dir and state_dir so the bridge can target the existing CLI runtime."
                )
            self._runtime = CliRuntime.create(
                profile_dir=Path(self.config.profile_dir),
                state_dir=Path(self.config.state_dir),
            )
            return self._runtime
        profile_dir = Path(self.config.profile_dir or ".")
        state_dir = Path(self.config.state_dir or ".")
        self._runtime = self.runtime_factory(profile_dir, state_dir)
        return self._runtime

    def _handle_command(
        self,
        inbound: GatewayInboundMessage,
        *,
        command: str,
        argument: str | None,
    ) -> GatewayCliControlResult:
        runtime = self.runtime()
        assert self.binding_store is not None
        if command in {"help", "start"}:
            return GatewayCliControlResult(body=self._help_text(), summary="help")
        if command in {"clones", "list"}:
            return GatewayCliControlResult(body=self._clone_listing(runtime), summary="list clones")
        if command == "sessions":
            clone_id = argument.strip() if argument else self._resolve_bound_clone(runtime, inbound)
            if not clone_id:
                return GatewayCliControlResult(
                    body=(
                        "Usage: /sessions <clone_id>\n"
                        "You can also bind first with /clone <clone_id> or /session <session_id>."
                    ),
                    summary="missing clone id",
                )
            return GatewayCliControlResult(
                body=self._session_listing(runtime, clone_id),
                clone_id=clone_id,
                summary="list sessions",
            )
        if command in {"clone", "use", "bind"}:
            if not argument:
                return GatewayCliControlResult(
                    body="Usage: /clone <clone_id>\nTry /clones to inspect the available clones first.",
                    summary="missing clone id",
                )
            clone_id = argument.strip()
            session = self._session_for_clone(runtime, clone_id)
            self.binding_store.set(
                account_id=inbound.account_id,
                conversation_id=inbound.conversation_id,
                clone_id=clone_id,
                session_id=session.session_id,
            )
            return GatewayCliControlResult(
                body=(
                    f"Bound this {self.binding_subject} to clone `{clone_id}`.\n"
                    f"session_id: `{session.session_id}`\n"
                    "Send plain text next and I will continue on that local Aegis line."
                ),
                clone_id=clone_id,
                session_id=session.session_id,
                summary="clone bound",
            )
        if command in {"session", "use-session", "bind-session"}:
            if not argument:
                return GatewayCliControlResult(
                    body=(
                        "Usage: /session <session_id>\n"
                        "   or: /session <clone_id> <session_number_or_prefix>\n"
                        "Use /sessions <clone_id> when you need the numbered shortcuts first."
                    ),
                    summary="missing session id",
                )
            clone_id, session = self._resolve_bind_session_target(
                runtime,
                inbound=inbound,
                argument=argument,
            )
            self.binding_store.set(
                account_id=inbound.account_id,
                conversation_id=inbound.conversation_id,
                clone_id=clone_id,
                session_id=session.session_id,
            )
            return GatewayCliControlResult(
                body=(
                    f"Bound this {self.binding_subject} to session `{session.session_id}`.\n"
                    f"clone_id: `{clone_id}`\n"
                    "Send plain text next and I will continue on that exact local Aegis session."
                ),
                clone_id=clone_id,
                session_id=session.session_id,
                summary="session bound",
            )
        if command == "status":
            clone_id, session, selection_mode = self._session_selection(runtime, inbound)
            if clone_id is None or session is None:
                return GatewayCliControlResult(
                    body=self._clone_selection_hint(runtime),
                    summary="status without clone",
                )
            selection_label = {
                "bound": "bound",
                "bound-session": "bound-session",
                "bound-recovered": "bound-session-recovered",
                "parent-bound": "parent-bound",
                "parent-bound-session": "parent-bound-session",
                "parent-bound-recovered": "parent-bound-session-recovered",
                "default": "configured-default-clone",
                "default-session": "configured-default-session",
                "default-session-recovered": "configured-default-session-recovered",
            }.get(selection_mode or "", "unknown")
            return GatewayCliControlResult(
                body=(
                    f"Current clone: `{clone_id}`\n"
                    f"selection: `{selection_label}`\n"
                    f"session_id: `{session.session_id}`\n"
                    f"status: `{session.status}`\n"
                    f"workspace_id: `{session.workspace_id or clone_id}`"
                ),
                clone_id=clone_id,
                session_id=session.session_id,
                summary="status",
            )
        if command == "wake":
            clone_id, session, _ = self._session_selection(runtime, inbound)
            if clone_id is None or session is None:
                return GatewayCliControlResult(
                    body=self._clone_selection_hint(runtime),
                    summary="wake without binding",
                )
            result = runtime.wake(session.session_id)
            return GatewayCliControlResult(
                body=(
                    f"Woke clone `{clone_id}`.\n"
                    f"session_id: `{result.session.session_id}`\n"
                    f"next_step: {result.decision.rationale.summary}"
                ),
                clone_id=clone_id,
                session_id=result.session.session_id,
                summary="wake",
            )
        return GatewayCliControlResult(
            body=(
                f"Unknown command `/{command}`.\n"
                "Try /help, /clones, /clone <clone_id>, /status, or /wake."
            ),
            summary="unknown command",
        )

    def _session_for_clone(self, runtime: CliRuntimeLike, clone_id: str) -> SessionState:
        session = runtime.latest_session_for_clone(clone_id)
        if session is not None:
            return session
        if not self.config.auto_create_clone:
            raise RuntimeError(
                f"unknown clone: {clone_id}. Create it locally first or enable "
                f"{self.control_config_path}.auto_create_clone."
            )
        return runtime.create_clone(clone_id=clone_id)

    def _session_selection(
        self,
        runtime: CliRuntimeLike,
        inbound: GatewayInboundMessage,
    ) -> tuple[str | None, SessionState | None, str | None]:
        clone_id, session_id, selection_mode, binding_conversation_id = self._clone_selection(
            runtime,
            inbound,
        )
        if clone_id is None:
            return None, None, selection_mode
        if session_id is not None:
            try:
                return clone_id, runtime.inspect_session(session_id), selection_mode
            except KeyError:
                recovered = self._session_for_clone(runtime, clone_id)
                assert self.binding_store is not None
                self.binding_store.set(
                    account_id=inbound.account_id,
                    conversation_id=binding_conversation_id or inbound.conversation_id,
                    clone_id=clone_id,
                    session_id=recovered.session_id,
                )
                if selection_mode in {"parent-bound", "parent-bound-session"}:
                    return clone_id, recovered, "parent-bound-recovered"
                if selection_mode == "default-session":
                    return clone_id, recovered, "default-session-recovered"
                return clone_id, recovered, "bound-recovered"
        return clone_id, self._session_for_clone(runtime, clone_id), selection_mode

    def _clone_selection(
        self,
        runtime: CliRuntimeLike,
        inbound: GatewayInboundMessage,
    ) -> tuple[str | None, str | None, str | None, str | None]:
        assert self.binding_store is not None
        lookup_order = self._binding_lookup_order(inbound)
        for conversation_id in lookup_order:
            binding = self.binding_store.get(
                account_id=inbound.account_id,
                conversation_id=conversation_id,
            )
            if binding is None:
                continue
            if conversation_id == inbound.conversation_id:
                return (
                    binding.clone_id,
                    binding.session_id,
                    "bound-session" if binding.session_id else "bound",
                    conversation_id,
                )
            return (
                binding.clone_id,
                binding.session_id,
                "parent-bound-session" if binding.session_id else "parent-bound",
                conversation_id,
            )
        if self.config.default_session_id is not None:
            try:
                default_session = runtime.inspect_session(self.config.default_session_id)
                default_clone_id = self._clone_id_for_session(default_session)
            except (KeyError, RuntimeError):
                pass
            else:
                return default_clone_id, default_session.session_id, "default-session", None
        if self.config.default_clone_id is not None:
            return self.config.default_clone_id, None, "default", None
        return None, None, None, None

    def _resolve_bound_clone(
        self,
        runtime: CliRuntimeLike,
        inbound: GatewayInboundMessage,
    ) -> str | None:
        clone_id, _, _, _ = self._clone_selection(runtime, inbound)
        return clone_id

    def _binding_lookup_order(
        self,
        inbound: GatewayInboundMessage,
    ) -> tuple[str, ...]:
        candidates = [inbound.conversation_id]
        if (
            inbound.parent_conversation_id is not None
            and inbound.parent_conversation_id != inbound.conversation_id
        ):
            candidates.append(inbound.parent_conversation_id)
        return tuple(dict.fromkeys(candidates))

    def _clone_id_for_session(self, session: SessionState) -> str:
        clone_id = _optional_text(session.workspace_id)
        if clone_id is not None:
            return clone_id
        profile_id = session.profile_id.strip()
        if profile_id.startswith("clone:"):
            resolved = profile_id.split(":", 1)[1].strip()
            if resolved:
                return resolved
        raise RuntimeError(
            f"session {session.session_id} is not attached to a named clone, so {self.surface_label} cannot bind it by clone."
        )

    def _resolve_bind_session_target(
        self,
        runtime: CliRuntimeLike,
        *,
        inbound: GatewayInboundMessage,
        argument: str,
    ) -> tuple[str, SessionState]:
        tokens = tuple(part.strip() for part in argument.split() if part.strip())
        if not tokens:
            raise RuntimeError(
                "Usage: /session <session_id>\n"
                "   or: /session <clone_id> <session_number_or_prefix>"
            )
        if len(tokens) == 1:
            session_ref = tokens[0]
            try:
                session = runtime.inspect_session(session_ref)
            except KeyError:
                clone_id = self._resolve_bound_clone(runtime, inbound)
                if not clone_id:
                    raise RuntimeError(
                        "Short session references need a clone context. Bind a clone first with "
                        "`/clone <clone_id>`, or send `/session <clone_id> <session_number_or_prefix>`."
                    ) from None
                session = self._resolve_session_reference(
                    runtime,
                    clone_id=clone_id,
                    session_ref=session_ref,
                )
                return clone_id, session
            return self._clone_id_for_session(session), session
        if len(tokens) == 2:
            clone_id, session_ref = tokens
            session = self._resolve_session_reference(
                runtime,
                clone_id=clone_id,
                session_ref=session_ref,
            )
            return clone_id, session
        raise RuntimeError(
            "Usage: /session <session_id>\n"
            "   or: /session <clone_id> <session_number_or_prefix>\n"
            "Use /sessions <clone_id> to inspect the available numbered shortcuts first."
        )

    def _resolve_session_reference(
        self,
        runtime: CliRuntimeLike,
        *,
        clone_id: str,
        session_ref: str,
    ) -> SessionState:
        session_ids = runtime.session_ids_for_clone(clone_id)
        if not session_ids:
            raise RuntimeError(
                f"unknown clone: {clone_id}. Try /clones to inspect the available clones first."
            )
        reference = session_ref.strip()
        if not reference:
            raise RuntimeError(
                f"missing session reference for clone `{clone_id}`. Try /sessions {clone_id}."
            )
        ordinal_reference = reference[1:] if reference.startswith("#") else reference
        if ordinal_reference.isdigit():
            ordinal = int(ordinal_reference)
            if 1 <= ordinal <= len(session_ids):
                return runtime.inspect_session(session_ids[ordinal - 1])
            raise RuntimeError(
                f"session selection `{reference}` is out of range for clone `{clone_id}`. "
                f"Try /sessions {clone_id}."
            )
        if reference in session_ids:
            return runtime.inspect_session(reference)
        prefix_matches = tuple(session_id for session_id in session_ids if session_id.startswith(reference))
        if len(prefix_matches) == 1:
            return runtime.inspect_session(prefix_matches[0])
        if len(prefix_matches) > 1:
            match_summary = ", ".join(
                f"`{_abbreviate_identifier(session_id)}`" for session_id in prefix_matches[:4]
            )
            extra = "" if len(prefix_matches) <= 4 else ", ..."
            raise RuntimeError(
                f"session reference `{reference}` is ambiguous for clone `{clone_id}`: "
                f"{match_summary}{extra}. Try /sessions {clone_id}."
            )
        raise RuntimeError(
            f"unknown session reference `{reference}` for clone `{clone_id}`. Try /sessions {clone_id}."
        )

    def _clone_listing(self, runtime: CliRuntimeLike) -> str:
        clones = runtime.list_clones(limit=12)
        if not clones:
            return (
                "No local Aegis clones are available yet.\n"
                "Create one from the CLI first, or configure "
                f"`{self.control_config_path}.auto_create_clone` together with a default clone."
            )
        lines = ["Available local Aegis clones:"]
        for clone in clones:
            clone_id = str(getattr(clone, "clone_id", ""))
            latest_session_id = str(getattr(clone, "latest_session_id", ""))
            latest_status = str(getattr(clone, "latest_status", ""))
            session_count = int(getattr(clone, "session_count", 0) or 0)
            lines.append(
                f"- {clone_id} · latest {latest_session_id[:8]} · "
                f"{session_count} session{'s' if session_count != 1 else ''} · {latest_status}"
            )
        lines.append(
            f"Plain text does not route until this {self.binding_subject} is pinned. "
            f"Send `/clone <clone_id>` when you want to bind this {self.binding_subject} to a specific clone."
        )
        lines.append("Use `/sessions <clone_id>` to inspect that clone's known session ids.")
        return "\n".join(lines)

    def _session_listing(self, runtime: CliRuntimeLike, clone_id: str) -> str:
        session_ids = runtime.session_ids_for_clone(clone_id)
        if not session_ids:
            raise RuntimeError(
                f"unknown clone: {clone_id}. Try /clones to inspect the available clones first."
            )
        lines = [f"Known sessions for clone `{clone_id}`:"]
        for ordinal, session_id in enumerate(session_ids, start=1):
            session = runtime.inspect_session(session_id)
            line = (
                f"- {ordinal} · `{_abbreviate_identifier(session.session_id)}` · {session.status} · "
                f"updated {session.updated_at.isoformat()}"
            )
            if ordinal == 1:
                line += " · latest"
            if session.parent_session_id:
                line += f" · resumed from {_abbreviate_identifier(session.parent_session_id, head=8, tail=4)}"
            lines.append(line)
        sample_prefix = _abbreviate_identifier(session_ids[0], head=12, tail=0).rstrip("…")
        lines.append(
            f"Send `/session {clone_id} 1` when you want to pin this {self.binding_subject} by number."
        )
        lines.append(
            f"You can also send `/session {clone_id} {sample_prefix}` or the full session id when you need an exact continuity line."
        )
        return "\n".join(lines)

    def _clone_selection_hint(self, runtime: CliRuntimeLike) -> str:
        clones = runtime.list_clones(limit=8)
        if not clones:
            return (
                f"This {self.binding_subject} is not connected to a local Aegis clone yet, and no clones are "
                "available. Create one in the CLI first."
            )
        return (
            f"This {self.binding_subject} is not pinned yet. Plain text will not continue until you bind it.\n"
            "Send `/clone <clone_id>` when you want to pin this conversation to a clone.\n"
            "Send `/sessions <clone_id>` to inspect numbered session shortcuts, then `/session <clone_id> <number_or_prefix>` if you need one exact continuity line.\n"
            "Full session ids still work too with `/session <session_id>`.\n\n"
            + self._clone_listing(runtime)
        )

    def _help_text(self) -> str:
        return "\n".join(
            (
                f"{self.surface_label} remote control commands:",
                "- /clones · list the local Aegis clones this bridge can see",
                "- /sessions <clone_id> · inspect the known local sessions for one clone",
                f"- /clone <clone_id> · pin this {self.binding_subject} to a clone",
                f"- /session <session_id> · pin this {self.binding_subject} to one exact local session",
                f"- /session <clone_id> <number_or_prefix> · pin by the numbered or prefixed shortcut shown in /sessions",
                f"- /status · inspect the clone/session currently handling this {self.binding_subject}",
                "- /wake · ask the active clone to refresh its next-step plan",
                f"- plain text · forward the message into the active clone after this {self.binding_subject} is pinned",
            )
        )

    def _parse_command(self, body: str) -> tuple[str | None, str | None]:
        normalized = body.strip()
        while normalized:
            if normalized.startswith("/"):
                break
            stripped = False
            for prefix in ("-", "•", "*", "—", "·", ">"):
                if normalized.startswith(prefix):
                    normalized = normalized[len(prefix) :].lstrip()
                    stripped = True
                    break
            if not stripped:
                return None, None
        if not normalized.startswith("/"):
            return None, None
        parts = normalized[1:].split(None, 1)
        command = parts[0].strip().lower()
        argument = parts[1].strip() if len(parts) > 1 else None
        return (command or None, argument)


FeishuCliControlConfig = GatewayCliControlConfig
FeishuCliBinding = GatewayCliBinding
FeishuCliBindingStore = GatewayCliBindingStore
FeishuCliControlResult = GatewayCliControlResult
FeishuCliControlService = GatewayCliControlService


__all__ = [
    "CliRuntimeFactory",
    "CliRuntimeLike",
    "GatewayCliBinding",
    "GatewayCliBindingStore",
    "GatewayCliControlConfig",
    "GatewayCliControlResult",
    "GatewayCliControlService",
    "FeishuCliBinding",
    "FeishuCliBindingStore",
    "FeishuCliControlConfig",
    "FeishuCliControlResult",
    "FeishuCliControlService",
    "load_feishu_cli_control_config",
    "load_gateway_cli_control_config",
]
