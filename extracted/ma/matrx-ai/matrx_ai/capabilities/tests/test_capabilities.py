"""Phase B1 tests — capability registry + ClientContext resolver.

Covers registration, idempotence, conflict detection, the resolver's three
error classes (unknown name, auth violation, invalid payload), payload
typing, and tool-spec emission.
"""
from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, Field

from matrx_ai.capabilities import (
    Capability,
    CapabilityResolutionError,
    ClientContext,
    clear_capabilities,
    get_capability,
    list_capabilities,
    register_capability,
    resolve_client_capabilities,
)
from matrx_ai.capabilities.built_in import _register_built_ins
from matrx_ai.tools.specs import RegisteredToolSpec


@pytest.fixture(autouse=True)
def _isolated_registry() -> Any:
    """Snapshot + restore registry around every test so cross-test pollution
    is impossible. The package's built-in bundles are restored afterward."""
    snapshot = dict(list_capabilities())
    yield
    clear_capabilities()
    for cap in snapshot.values():
        register_capability(cap)


class _EditorPayload(BaseModel):
    file_path: str = Field(min_length=1)
    cursor_line: int = 0


def _editor_capability() -> Capability:
    return Capability(
        name="editor-state",
        description="Test editor capability",
        payload_model=_EditorPayload,
        enabled_tools=(RegisteredToolSpec(name="vsc_get_state"),),
        requires_auth=True,
    )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:
    def test_register_then_get(self) -> None:
        cap = _editor_capability()
        register_capability(cap)
        assert get_capability("editor-state") is cap

    def test_register_unknown_returns_none(self) -> None:
        assert get_capability("does-not-exist") is None

    def test_re_register_same_instance_is_idempotent(self) -> None:
        cap = _editor_capability()
        register_capability(cap)
        register_capability(cap)
        assert get_capability("editor-state") is cap

    def test_re_register_different_instance_raises(self) -> None:
        register_capability(_editor_capability())
        with pytest.raises(ValueError, match="already registered"):
            register_capability(_editor_capability())

    def test_replace_overrides(self) -> None:
        register_capability(_editor_capability())
        replacement = Capability(
            name="editor-state",
            description="Replaced",
            payload_model=_EditorPayload,
        )
        register_capability(replacement, replace=True)
        assert get_capability("editor-state") is replacement


# ---------------------------------------------------------------------------
# Built-in bundles
# ---------------------------------------------------------------------------

class TestBuiltIns:
    def test_sandbox_fs_is_registered_after_import(self) -> None:
        _register_built_ins()
        cap = get_capability("sandbox-fs")
        assert cap is not None
        assert cap.requires_auth is True
        # The sandbox-fs bundle statically enables the fs_* / shell_* / git_ingest
        # tools (built_in.py::_SANDBOX_FS_TOOLS) — they route through the sandbox
        # proxy when the capability is present.
        enabled = {t.name for t in cap.enabled_tools}
        assert {"fs_read", "fs_write", "shell_execute", "shell_python", "git_ingest"} <= enabled
        assert len(cap.enabled_tools) == 10


# ---------------------------------------------------------------------------
# Resolution — happy paths
# ---------------------------------------------------------------------------

class TestResolveHappyPath:
    def test_empty_client_context_is_noop(self) -> None:
        specs, _optional, payloads = resolve_client_capabilities(ClientContext())
        assert specs == []
        assert payloads == {}

    def test_capability_with_no_payload_model_just_emits_specs(self) -> None:
        cap = Capability(
            name="aux",
            enabled_tools=(RegisteredToolSpec(name="aux_tool"),),
            requires_auth=False,
        )
        register_capability(cap)
        specs, _optional, payloads = resolve_client_capabilities(
            ClientContext(capabilities=["aux"]), is_authenticated=False,
        )
        assert [s.name for s in specs] == ["aux_tool"]
        assert payloads == {}

    def test_capability_with_payload_validates(self) -> None:
        register_capability(_editor_capability())
        ctx = ClientContext(
            capabilities=["editor-state"],
            state={"editor-state": {"file_path": "/foo.py", "cursor_line": 10}},
        )
        specs, _optional, payloads = resolve_client_capabilities(ctx)
        assert [s.name for s in specs] == ["vsc_get_state"]
        assert isinstance(payloads["editor-state"], _EditorPayload)
        assert payloads["editor-state"].file_path == "/foo.py"

    def test_payload_optional_when_state_omitted(self) -> None:
        # When the capability declares a payload_model but the client doesn't
        # send the state, the resolver still enables the tools — payload is
        # optional. Tools that need it check try_get_app_context() at exec time.
        register_capability(_editor_capability())
        specs, _optional, payloads = resolve_client_capabilities(
            ClientContext(capabilities=["editor-state"])
        )
        assert [s.name for s in specs] == ["vsc_get_state"]
        assert payloads == {}

    def test_duplicate_names_in_request_dedupe(self) -> None:
        register_capability(_editor_capability())
        ctx = ClientContext(capabilities=["editor-state", "editor-state"])
        specs, _optional, _ = resolve_client_capabilities(ctx)
        # Single ToolSpec, not two.
        assert len(specs) == 1


# ---------------------------------------------------------------------------
# Resolution — error paths (strict, no silent drops)
# ---------------------------------------------------------------------------

class TestResolveErrors:
    def test_unknown_capability_raises(self) -> None:
        ctx = ClientContext(capabilities=["does-not-exist"])
        with pytest.raises(CapabilityResolutionError, match="unknown capability"):
            resolve_client_capabilities(ctx)

    def test_auth_required_unauthenticated_raises(self) -> None:
        register_capability(_editor_capability())
        ctx = ClientContext(capabilities=["editor-state"])
        with pytest.raises(CapabilityResolutionError, match="requires authentication"):
            resolve_client_capabilities(ctx, is_authenticated=False)

    def test_invalid_payload_raises(self) -> None:
        register_capability(_editor_capability())
        ctx = ClientContext(
            capabilities=["editor-state"],
            state={"editor-state": {"cursor_line": 10}},  # missing file_path
        )
        with pytest.raises(CapabilityResolutionError, match="payload invalid"):
            resolve_client_capabilities(ctx)

    def test_multiple_errors_aggregated(self) -> None:
        # Different problems on different capabilities — both surfaced in
        # one error message, not just the first one.
        register_capability(_editor_capability())
        ctx = ClientContext(
            capabilities=["editor-state", "totally-unknown"],
            state={"editor-state": {"cursor_line": 10}},  # invalid payload
        )
        with pytest.raises(CapabilityResolutionError) as excinfo:
            resolve_client_capabilities(ctx)
        assert "payload invalid" in str(excinfo.value)
        assert "unknown capability" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Top-level matrx_ai exports
# ---------------------------------------------------------------------------

class TestTopLevelExports:
    def test_capability_importable_from_matrx_ai(self) -> None:
        import matrx_ai

        assert matrx_ai.Capability is Capability
        assert matrx_ai.ClientContext is ClientContext

    def test_configure_capabilities_kwarg(self) -> None:
        # configure() with capabilities=[...] should register each one.
        # We use a uniquely-named capability so we don't pollute other tests.
        import matrx_ai

        unique = Capability(
            name="test-only-via-configure",
            description="Registered through matrx_ai.configure() in tests",
            requires_auth=False,
        )
        matrx_ai.configure(capabilities=[unique])
        assert get_capability("test-only-via-configure") is unique
