from agentic_devtools.ai_providers import copilot as copilot_module


def test_string_leaves_none_returns_empty_set() -> None:
    assert copilot_module._string_leaves(None) == set()


def test_string_leaves_nested_list_returns_leaf_string() -> None:
    assert copilot_module._string_leaves({"outer": ["secret"]}) == {"secret"}


def test_string_leaves_integer_returns_string_repr() -> None:
    assert copilot_module._string_leaves(42) == {"42"}


def test_string_leaves_bool_returns_empty_set() -> None:
    assert copilot_module._string_leaves(True) == set()


def test_string_leaves_unsupported_object_returns_empty_set() -> None:
    assert copilot_module._string_leaves(object()) == set()


def test_string_leaves_already_seen_cyclic_mapping_returns_empty_set() -> None:
    cyclic: dict[str, object] = {}
    cyclic["self"] = cyclic
    assert copilot_module._string_leaves(cyclic, frozenset({id(cyclic)})) == set()


def test_string_leaves_already_seen_cyclic_list_returns_empty_set() -> None:
    cyclic: list[object] = []
    cyclic.append(cyclic)
    assert copilot_module._string_leaves(cyclic, frozenset({id(cyclic)})) == set()
