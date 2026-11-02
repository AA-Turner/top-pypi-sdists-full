"""Regression coverage for the eval CLI's independent host-bootstrap seam."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from matrx_rag.eval import _bootstrap
from matrx_mandate_scan.adapters.python import scan_source


@pytest.mark.asyncio
async def test_bootstrap_keeps_open_host_contract_and_awaits_callable(monkeypatch) -> None:
    called: list[str] = []

    async def configure() -> None:
        called.append("configured")

    seen: list[str] = []
    monkeypatch.setattr(
        _bootstrap.importlib,
        "import_module",
        lambda module_name: (seen.append(module_name), SimpleNamespace(configure=configure))[1],
    )

    await _bootstrap.run_bootstrap("consumer_host.wiring:configure")

    assert seen == ["consumer_host.wiring"]
    assert called == ["configured"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "spec", ["host", ":configure", "host.wiring:", "host-name.wiring:configure"]
)
async def test_bootstrap_rejects_invalid_open_contract(spec: str) -> None:
    with pytest.raises(SystemExit):
        await _bootstrap.run_bootstrap(spec)


def test_bootstrap_marker_does_not_hide_a_dynamic_import_from_the_scanner() -> None:
    source = _bootstrap.__file__
    assert source is not None
    result = scan_source(
        Path(source).read_text(encoding="utf-8"),
        "packages/matrx-rag/matrx_rag/eval/_bootstrap.py",
    )
    assert "UNRESOLVED_IMPORT" not in {finding.code for finding in result.findings}
