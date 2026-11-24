"""An enum value that differs only in spelling is accepted at any depth; a different word never is."""

from __future__ import annotations

from typing import Annotated, Literal

import pytest
from matrx_ai.tools._dispatch_util import heal_choice_spelling, resolve_choice
from pydantic import BaseModel, Field, RootModel, ValidationError


class Item(BaseModel):
    type: Literal["choice", "choice_many"]


class Flat(BaseModel):
    mode: Literal["get", "set"]
    items: list[Item] = []


class Search(BaseModel):
    action: Literal["search"]


class Read(BaseModel):
    action: Literal["read"]


class Dispatch(RootModel):
    root: Annotated[Search | Read, Field(discriminator="action")]


def heal(model: type[BaseModel], args: dict):
    with pytest.raises(ValidationError) as caught:
        model.model_validate(args)
    return heal_choice_spelling(args, caught.value)


@pytest.mark.parametrize("value", ["choice_many", "Choice-Many", "choiceMany", "CHOICE MANY"])
def test_spelling_resolves(value):
    assert resolve_choice(value, ["choice", "choice_many"]) == "choice_many"


def test_a_different_word_never_resolves_without_a_declared_synonym():
    assert resolve_choice("choose", ["choice", "choice_many"]) is None
    assert resolve_choice("get", ["set", "delete"]) is None
    assert resolve_choice("choose", ["choice"], {"choose": "choice"}) == "choice"


def test_a_nested_value_is_respelled_and_the_input_is_left_alone():
    args = {"mode": "GET", "items": [{"type": "choice"}, {"type": "Choice_Many"}]}
    healed, changes = heal(Flat, args)
    Flat.model_validate(healed)
    assert healed["items"][1]["type"] == "choice_many"
    assert {c[1] for c in changes} == {"GET", "Choice_Many"}
    assert args["mode"] == "GET"


def test_an_action_tag_is_respelled():
    healed, _ = heal(Dispatch, {"action": "Search"})
    assert Dispatch.model_validate(healed).root.action == "search"


def test_get_is_never_turned_into_set():
    assert heal(Flat, {"mode": "fetch"}) is None
