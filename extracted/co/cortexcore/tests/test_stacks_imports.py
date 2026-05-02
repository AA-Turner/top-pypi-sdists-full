import importlib
import sys


def test_cortex_stacks_import_does_not_require_transformers(monkeypatch):
    monkeypatch.setitem(sys.modules, "transformers", None)
    monkeypatch.delitem(sys.modules, "cortex.stacks", raising=False)
    monkeypatch.delitem(sys.modules, "cortex.stacks.hf", raising=False)

    stacks = importlib.import_module("cortex.stacks")

    assert callable(stacks.build_cortex_auto_config)
    assert callable(stacks.build_hf_stack)
