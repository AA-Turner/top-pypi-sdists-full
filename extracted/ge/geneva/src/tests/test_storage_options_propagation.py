# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""AST guard: every call to ``lance.dataset(...)``, ``open_lance_dataset(...)``,
``lance.write_dataset(...)``, or ``filesystem_from_uri(...)`` outside the
sanctioned wrappers must pass ``storage_options=``.

This catches the class of bug where a new call site silently drops cloud
credentials, causing Azure / S3 / GCS reads to fail when the customer
supplies credentials via ``storage_options`` instead of env vars.

If a new violation appears, prefer fixing it by passing ``storage_options=``
from the surrounding context (Table, TableReference, or an explicit
function parameter). Add a path to ``ALLOWED_FILES`` only when the call
site genuinely cannot obtain storage_options (e.g. a primitive wrapper
that is itself the destination of storage_options, or a top-level setup
hook with no Table context).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).resolve().parents[1] / "geneva"

# Files allowed to call lance.dataset / open_lance_dataset / lance.write_dataset
# without an explicit storage_options=. Add entries sparingly and document why.
ALLOWED_FILES: frozenset[str] = frozenset(
    {
        # The wrapper itself — storage_options is the kwarg it forwards.
        "geneva/db.py",
    }
)

_BARE_NAMES: frozenset[str] = frozenset({"open_lance_dataset", "filesystem_from_uri"})
_ATTR_NAMES: frozenset[str] = frozenset({"dataset", "write_dataset"})


def _is_guarded_call(node: ast.Call) -> bool:
    """Return True if this call is one we want to enforce storage_options on.

    Matches:
      * ``open_lance_dataset(...)``
      * ``filesystem_from_uri(...)`` (the public Geneva helper)
      * ``lance.dataset(...)`` / ``_lance.dataset(...)``
      * ``lance.write_dataset(...)`` / ``_lance.write_dataset(...)``
    """
    func = node.func
    if isinstance(func, ast.Name) and func.id in _BARE_NAMES:
        return True
    if isinstance(func, ast.Attribute) and func.attr in _ATTR_NAMES:
        value = func.value
        if isinstance(value, ast.Name) and value.id in {"lance", "_lance"}:
            return True
    return False


def _has_storage_options(node: ast.Call) -> bool:
    """True if storage_options is passed as a keyword arg or via **kwargs."""
    for kw in node.keywords:
        if kw.arg == "storage_options":
            return True
        # **kwargs forwarding — assume the caller has already validated.
        if kw.arg is None:
            return True
    return False


def _is_raw_open_table_call(node: ast.Call) -> bool:
    """True for ``open_table(...)`` on a *raw lancedb* connection.

    Geneva's own ``Connection.open_table`` forwards storage_options
    internally, so calls like ``self._conn.open_table(...)`` or
    ``connect(...).open_table(...)`` are safe and not matched here.

    The dangerous case is calling ``open_table`` directly on the underlying
    lancedb connection, which does NOT inherit credentials passed via
    ``storage_options``. Those receivers in this codebase are:
      * ``<x>._connect`` (the cached lancedb connection on a Connection)
      * a local ``inner`` / ``direct_conn`` holding a lancedb connection
      * ``lancedb.connect(...)`` / ``ldb.connect(...)`` inline
    Such calls must pass ``storage_options=`` explicitly.
    """
    func = node.func
    if not (isinstance(func, ast.Attribute) and func.attr == "open_table"):
        return False
    recv = func.value
    if isinstance(recv, ast.Name) and recv.id in {"inner", "direct_conn"}:
        return True
    if isinstance(recv, ast.Attribute) and recv.attr == "_connect":
        return True
    if isinstance(recv, ast.Call):
        rfunc = recv.func
        if (
            isinstance(rfunc, ast.Attribute)
            and rfunc.attr == "connect"
            and isinstance(rfunc.value, ast.Name)
            and rfunc.value.id in {"lancedb", "ldb"}
        ):
            return True
    return False


def _find_violations(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    return [
        (node.lineno, ast.unparse(node)[:160])
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _is_guarded_call(node)
        and not _has_storage_options(node)
    ]


def _iter_python_files() -> list[Path]:
    return sorted(p for p in SRC_ROOT.rglob("*.py") if "__pycache__" not in p.parts)


@pytest.mark.parametrize(
    "py_file",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(SRC_ROOT.parent)),
)
def test_dataset_calls_forward_storage_options(py_file: Path) -> None:
    rel = py_file.relative_to(SRC_ROOT.parent).as_posix()
    if rel in ALLOWED_FILES:
        return
    violations = _find_violations(py_file)
    if violations:
        lines = "\n".join(f"  line {ln}: {snippet}" for ln, snippet in violations)
        pytest.fail(
            f"{rel} calls lance.dataset / open_lance_dataset / lance.write_dataset "
            f"without passing storage_options=:\n{lines}\n\n"
            "Pass storage_options= from the surrounding context (Table, "
            "TableReference, or a function parameter). If this call genuinely "
            "has no storage_options source, add the file to ALLOWED_FILES in "
            f"{Path(__file__).name} with a one-line justification."
        )


def _find_open_table_violations(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    return [
        (node.lineno, ast.unparse(node)[:160])
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _is_raw_open_table_call(node)
        and not _has_storage_options(node)
    ]


@pytest.mark.parametrize(
    "py_file",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(SRC_ROOT.parent)),
)
def test_open_table_calls_forward_storage_options(py_file: Path) -> None:
    """Calling open_table on a raw lancedb connection must pass storage_options.

    Unlike the dataset guard above, this runs on every file (no ALLOWED_FILES
    exemption): there is no legitimate wrapper that needs to open a raw lancedb
    table without forwarding credentials.
    """
    violations = _find_open_table_violations(py_file)
    if violations:
        rel = py_file.relative_to(SRC_ROOT.parent).as_posix()
        lines = "\n".join(f"  line {ln}: {snippet}" for ln, snippet in violations)
        pytest.fail(
            f"{rel} calls open_table on a raw lancedb connection "
            f"(inner / *._connect / direct_conn / lancedb.connect(...)) without "
            f"passing storage_options=:\n{lines}\n\n"
            "Forward storage_options= from the surrounding Connection so cloud "
            "credentials reach the open. Geneva's Connection.open_table forwards "
            "them automatically — prefer that over the raw connection when possible."
        )


class _RecordingInner:
    """Stand-in for the lancedb inner connection that records open_table args."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def open_table(
        self,
        name: str,
        namespace_path: list[str] | None = None,
        storage_options: dict[str, str] | None = None,
        **_kwargs: object,
    ) -> object:
        self.calls.append(
            {
                "name": name,
                "namespace_path": namespace_path,
                "storage_options": storage_options,
            }
        )
        return object()


class _FakeConn:
    """Minimal Connection stand-in for exercising NativeTable._ltbl."""

    uri = "az://container/root"

    def __init__(self, storage_options: dict[str, str] | None) -> None:
        self._storage_options = storage_options
        self._connect = _RecordingInner()

    def is_remote_uri(self) -> bool:
        return False


def test_native_table_open_forwards_storage_options() -> None:
    """NativeTable._ltbl must forward the table's storage_options to open_table.

    Regression: opening a table (e.g. a __system table on Azure) dropped
    storage_options, failing with "no Azure account name in URI, and no
    storage account configured".
    """
    from geneva.table import NativeTable

    conn = _FakeConn(storage_options=None)
    NativeTable(
        conn,  # type: ignore[arg-type]  # duck-typed Connection stand-in
        "geneva_cluster_definitions",
        namespace=["__system"],
        storage_options={"account_name": "acct"},
    )

    call = conn._connect.calls[0]
    assert call["storage_options"] == {"account_name": "acct"}
    assert call["namespace_path"] == ["__system"]


def test_native_table_open_falls_back_to_connection_storage_options() -> None:
    """When the table has no storage_options, fall back to the connection's."""
    from geneva.table import NativeTable

    conn = _FakeConn(storage_options={"account_name": "from_conn"})
    NativeTable(conn, "geneva_jobs", namespace=["__system"])  # type: ignore[arg-type]

    call = conn._connect.calls[0]
    assert call["storage_options"] == {"account_name": "from_conn"}


def test_native_table_open_merges_partial_table_storage_options() -> None:
    """A truthy-but-partial table dict must not drop the connection's creds.

    View creation builds storage_options like
    {"new_table_enable_stable_row_ids": "true"} (no credentials). With ``or``
    semantics that partial dict would win and the connection's Azure creds
    would be dropped, reproducing "no Azure account name in URI". The open must
    receive the merged options (connection creds + the table's flag).
    """
    from geneva.table import NativeTable

    conn = _FakeConn(storage_options={"account_name": "acct", "account_key": "k"})
    NativeTable(
        conn,  # type: ignore[arg-type]  # duck-typed Connection stand-in
        "geneva_udtf_view",
        namespace=[],
        storage_options={"new_table_enable_stable_row_ids": "true"},
    )

    call = conn._connect.calls[0]
    assert call["storage_options"] == {
        "account_name": "acct",
        "account_key": "k",
        "new_table_enable_stable_row_ids": "true",
    }
