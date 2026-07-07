import copy
import json
import operator
import pickle
from collections.abc import Callable
from typing import Any

import pytest
from statsig_python_core._frozen_json import (
    _FrozenDict,
    _FrozenList,
    _deep_freeze_and_measure,
)


def _frozen_tree() -> _FrozenDict:
    frozen, retained_bytes = _deep_freeze_and_measure(
        {
            "mapping": {"key": "value"},
            "items": [2, 1, {"nested": ["value"]}],
        }
    )
    assert isinstance(frozen, _FrozenDict)
    assert isinstance(frozen["items"], _FrozenList)
    assert retained_bytes > 0
    return frozen


def test_frozen_json_preserves_builtin_compatibility_and_serialization():
    frozen = _frozen_tree()

    assert isinstance(frozen, dict)
    assert isinstance(frozen["mapping"], dict)
    assert isinstance(frozen["items"], list)
    assert isinstance(frozen["items"][2], dict)
    assert isinstance(frozen["items"][2]["nested"], list)
    assert json.loads(json.dumps(frozen)) == {
        "mapping": {"key": "value"},
        "items": [2, 1, {"nested": ["value"]}],
    }


def test_frozen_json_copy_operations_reuse_the_immutable_graph():
    frozen = _frozen_tree()

    assert copy.copy(frozen) is frozen
    assert copy.deepcopy(frozen) is frozen
    assert copy.copy(frozen["items"]) is frozen["items"]
    assert copy.deepcopy(frozen["items"]) is frozen["items"]


def test_frozen_json_rejects_reinitialization():
    frozen = _frozen_tree()
    items = frozen["items"]

    frozen.__init__()
    items.__init__()
    assert frozen["mapping"] == {"key": "value"}
    assert items == [2, 1, {"nested": ["value"]}]

    with pytest.raises(TypeError, match="immutable"):
        frozen.__init__({"poisoned": True})
    with pytest.raises(TypeError, match="immutable"):
        items.__init__(["poisoned"])


def test_frozen_json_pickle_round_trip_preserves_frozen_containers():
    frozen = _frozen_tree()

    restored = pickle.loads(pickle.dumps(frozen))

    assert restored == frozen
    assert restored is not frozen
    assert isinstance(restored, _FrozenDict)
    assert isinstance(restored["items"], _FrozenList)
    assert isinstance(restored["items"][2], _FrozenDict)

    with pytest.raises(TypeError, match="immutable"):
        restored["items"].append("changed")


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: operator.setitem(value, "new", 1),
        lambda value: operator.delitem(value, "key"),
        lambda value: operator.ior(value, {"new": 1}),
        lambda value: value.clear(),
        lambda value: value.pop("key"),
        lambda value: value.popitem(),
        lambda value: value.setdefault("new", 1),
        lambda value: value.update({"new": 1}),
    ],
)
def test_frozen_dict_rejects_ordinary_mutation(
    mutate: Callable[[dict[str, Any]], Any],
):
    mapping = _frozen_tree()["mapping"]

    with pytest.raises(TypeError, match="immutable"):
        mutate(mapping)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: operator.setitem(value, 0, 3),
        lambda value: operator.delitem(value, 0),
        lambda value: operator.iadd(value, [3]),
        lambda value: operator.imul(value, 2),
        lambda value: value.append(3),
        lambda value: value.clear(),
        lambda value: value.extend([3]),
        lambda value: value.insert(0, 3),
        lambda value: value.pop(),
        lambda value: value.remove(1),
        lambda value: value.reverse(),
        lambda value: value.sort(),
    ],
)
def test_frozen_list_rejects_ordinary_mutation(
    mutate: Callable[[list[Any]], Any],
):
    items = _frozen_tree()["items"]

    with pytest.raises(TypeError, match="immutable"):
        mutate(items)
