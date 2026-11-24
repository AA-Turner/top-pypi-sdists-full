"""A self-referencing args model generates a finite parameters map (was RecursionError)."""

from __future__ import annotations

from pydantic import BaseModel

from matrx_ai.tools.validation.params_from_model import build_parameters


class Node(BaseModel):
    label: str
    children: list[Node] = []


class Args(BaseModel):
    root: Node
    name: str


def test_recursive_model_terminates_and_expands_one_level():
    params = build_parameters(Args, action_description="x")
    root = params["root"]
    assert root["required"] is True
    kids = root["properties"]["children"]["items"]
    assert kids["type"] == "object"
    assert "label" not in kids.get("properties", {})  # the recursion point is closed, not expanded
