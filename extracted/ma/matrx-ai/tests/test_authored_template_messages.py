"""The one shared selection of authored template messages (aidream + matrx-local call it)."""

from matrx_ai.config.template_substitution import authored_template_messages

CONFIG = ["authored", "reply", "typed"]


def test_dict_wire_messages_system_lifted_out() -> None:
    wire = [
        {"role": "system", "content": "s"},
        {"role": "user", "content": "a"},
        {"role": "assistant", "content": "r"},
        {"role": "user", "content": "t"},
    ]
    assert authored_template_messages(wire, 2, CONFIG) == ["authored"]


def test_absent_or_zero_count_fills_nothing() -> None:
    wire = [{"role": "user", "content": "a"}]
    assert authored_template_messages(wire, None, CONFIG) == []
    assert authored_template_messages(wire, 0, CONFIG) == []


def test_object_wire_messages() -> None:
    class M:
        def __init__(self, role: str) -> None:
            self.role = role

    assert authored_template_messages([M("developer"), M("user"), M("user")], 3, CONFIG) == [
        "authored",
        "reply",
    ]
