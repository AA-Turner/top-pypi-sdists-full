"""Config-declared output handles are read from the NORMALIZED config.

THE BREAK: ``config_output_handles`` read the raw stored marker list. A list
the config model DERIVES (keys from labels) could then be stale — edges on it
validate and never fire — or missing — valid edges are refused. Any node with
config-derived handles is covered, so the guard uses a toy node, not a real one.
"""

from __future__ import annotations

from types import SimpleNamespace

from pydantic import BaseModel, model_validator

from matrx_graph.types.handle import (
    CONFIG_OUTPUT_HANDLE_PREFIX,
    CONFIG_OUTPUT_HANDLES,
    config_output_handles,
)


class _DerivedConfig(BaseModel):
    labels: list[str]
    keys: list[str] = []

    @model_validator(mode="after")
    def _derive(self) -> _DerivedConfig:
        if not self.labels:
            raise ValueError("labels required")
        self.keys = [label.lower() for label in self.labels]
        return self


_DerivedConfig.model_fields["keys"].json_schema_extra = {
    CONFIG_OUTPUT_HANDLES: True,
    CONFIG_OUTPUT_HANDLE_PREFIX: "k.",
}
_DerivedConfig.model_rebuild(force=True)

_SPEC = SimpleNamespace(config_schema=_DerivedConfig)


def _node(config: object) -> SimpleNamespace:
    return SimpleNamespace(data={"config": config})


def test_stale_stored_keys_are_recomputed() -> None:
    handles = config_output_handles(_SPEC, _node({"labels": ["A", "B"], "keys": ["old"]}))
    assert handles == {"k.a", "k.b"}


def test_missing_stored_keys_are_derived() -> None:
    assert config_output_handles(_SPEC, _node({"labels": ["Cc"]})) == {"k.cc"}


def test_invalid_config_declares_no_config_handles() -> None:
    assert config_output_handles(_SPEC, _node({"labels": [], "keys": ["x"]})) == set()
    assert config_output_handles(_SPEC, _node("not a dict")) == set()
