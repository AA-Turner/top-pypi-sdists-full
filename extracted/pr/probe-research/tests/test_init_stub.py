"""`probe/__init__.pyi` is generated from the lazy maps the package resolves names through,
so it names every public name, each from the module that defines it, and never drifts."""

from __future__ import annotations

import ast
import importlib
import importlib.util
from pathlib import Path

import probe

# Loaded by path, as other tests load agent/scripts: the repo root's `scripts` package can
# shadow `agent/scripts` on sys.path.
_SPEC = importlib.util.spec_from_file_location(
    "gen_init_stub", Path(__file__).resolve().parents[1] / "scripts" / "gen_init_stub.py"
)
gen_init_stub = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(gen_init_stub)


def test_the_committed_stub_is_current():
    assert gen_init_stub.STUB.read_text(encoding="utf-8") == gen_init_stub.render(), (
        "src/probe/__init__.pyi is stale: run `make -C agent gen-init-stub`"
    )


def test_every_public_name_is_in_the_stub_from_its_real_module():
    tree = ast.parse(Path(gen_init_stub.STUB).read_text(encoding="utf-8"))
    stubbed: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                stubbed[alias.asname or alias.name] = "." * node.level + (node.module or "")
    assert set(probe.__all__) - {"__version__"} <= set(stubbed)
    for name, module in stubbed.items():
        if name in ("errors", "expr"):
            continue
        assert getattr(importlib.import_module(module, "probe"), name) is getattr(probe, name), name
