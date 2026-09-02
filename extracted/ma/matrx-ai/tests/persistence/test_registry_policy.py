from __future__ import annotations

import ast
from pathlib import Path

from matrx_ai.persistence.registry import (
    RegisteredTable,
    configure_policy_registrar,
    get_model,
    register_table,
)


class _RegistryPolicyModel:
    pass


class _ConflictingModel:
    pass


def test_registration_automatically_installs_policy() -> None:
    observed: list[RegisteredTable] = []
    configure_policy_registrar(observed.append)
    try:
        register_table("public.automatic_policy_test", _RegistryPolicyModel)
        assert any(
            entry.name == "public.automatic_policy_test"
            and entry.model_cls is _RegistryPolicyModel
            and entry.write_owner == "coordinator"
            for entry in observed
        )
    finally:
        configure_policy_registrar(None)


def test_configuring_registrar_replays_existing_tables() -> None:
    register_table("public.policy_replay_test", _RegistryPolicyModel)
    observed: list[RegisteredTable] = []
    configure_policy_registrar(observed.append)
    try:
        assert any(entry.name == "public.policy_replay_test" for entry in observed)
    finally:
        configure_policy_registrar(None)


def test_conflicting_registration_is_loud_but_keeps_original(caplog) -> None:
    register_table("public.policy_conflict_test", _RegistryPolicyModel)
    register_table("public.policy_conflict_test", _ConflictingModel)
    assert get_model("public.policy_conflict_test") is _RegistryPolicyModel
    assert "COORDINATOR REGISTRY CONFLICT" in caplog.text


def test_unambiguous_bare_lookup_is_reconciled_not_dropped(caplog) -> None:
    """A bare key the caller can only have meant ONE way must resolve.

    Regression: 2026-08-15. Three call sites still passed bare relation names
    after the registry went schema-qualified; ``get_model`` raised, the
    Coordinator counted a queue-time drop, and the request's commit barrier
    killed live chats. There is exactly one thing ``"tool_call"`` can mean —
    reconcile it loudly, never lose the write.
    """
    register_table("public.coercion_target_test", _RegistryPolicyModel)
    assert get_model("coercion_target_test") is _RegistryPolicyModel
    assert "PERSISTENCE REGISTRY KEY COERCED" in caplog.text or "COERCED" in caplog.text


def test_wrong_schema_lookup_is_reconciled() -> None:
    """A right relation under the wrong schema is the same single meaning."""
    register_table("public.wrong_schema_target_test", _RegistryPolicyModel)
    assert get_model("chat.wrong_schema_target_test") is _RegistryPolicyModel


def test_ambiguous_bare_lookup_still_raises_and_names_candidates() -> None:
    """Two registered tables share the relation name → no single meaning."""
    register_table("public.ambiguous_relation_test", _RegistryPolicyModel)
    register_table("chat.ambiguous_relation_test", _ConflictingModel)
    try:
        get_model("ambiguous_relation_test")
    except KeyError as exc:
        assert "AMBIGUOUS" in str(exc)
        assert "public.ambiguous_relation_test" in str(exc)
        assert "chat.ambiguous_relation_test" in str(exc)
    else:
        raise AssertionError("ambiguous bare key unexpectedly resolved")


def test_unknown_relation_still_raises() -> None:
    try:
        get_model("nothing.ever_registered_this")
    except KeyError as exc:
        assert "no Model registered" in str(exc)
    else:
        raise AssertionError("unknown key unexpectedly resolved")


def test_bare_table_registration_is_rejected() -> None:
    try:
        register_table("ambiguous_name", _RegistryPolicyModel)
    except ValueError as exc:
        assert "schema.table" in str(exc)
    else:
        raise AssertionError("bare registry key unexpectedly accepted")


def test_literal_coordinator_queue_targets_are_schema_qualified() -> None:
    """A direct Coordinator.queue call must obey the registry's exact identity."""
    package_root = Path(__file__).resolve().parents[2] / "matrx_ai"
    bare_targets: list[str] = []

    for source_path in package_root.rglob("*.py"):
        tree = ast.parse(source_path.read_text(), filename=str(source_path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "queue" or not node.args:
                continue
            target = node.args[0]
            if isinstance(target, ast.Constant) and isinstance(target.value, str):
                if "." not in target.value:
                    bare_targets.append(f"{source_path.relative_to(package_root)}:{node.lineno}")

    assert bare_targets == [], f"bare Coordinator.queue target(s): {bare_targets}"
