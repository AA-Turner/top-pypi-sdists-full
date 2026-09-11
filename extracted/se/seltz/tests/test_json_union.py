"""The projection is generic: it names no field, and it touches only marked oneofs.

Everything else is handed to the message constructor, which is what validates it --
protobuf refuses an unknown name and an unmarked oneof's group name, both by name.
"""

import pytest

from seltz import ContentOptions, SnippetOptions
from seltz import FieldsMessage as Fields
from seltz.services._json_union import _accepted_keys, from_json_unions


def test_a_marked_oneof_is_keyed_by_its_group_name() -> None:
    """The whole point: one JSON key carrying either member."""
    boolean = from_json_unions(Fields, {"content": True}, "fields")
    assert boolean.WhichOneof("content") == "content_enabled"

    bag = from_json_unions(
        Fields, {"content": ContentOptions(max_characters_per_result=500)}, "fields"
    )
    assert bag.WhichOneof("content") == "content_options"

    mapping = from_json_unions(
        Fields, {"content": {"max_characters_per_result": 500}}, "fields"
    )
    assert mapping.content_options.max_characters_per_result == 500


def test_a_key_the_json_body_lacks_is_refused() -> None:
    """The silent failure this exists to stop: a typo reaching the service as an empty
    selection returns whatever the defaults give, and says nothing about why."""
    typo = "cont" + "nt"  # codespell:ignore
    with pytest.raises(TypeError, match="fields has no member"):
        from_json_unions(Fields, {typo: True}, "fields")


def test_a_marked_oneofs_member_name_is_not_a_key() -> None:
    """A marked oneof is addressed by its group name only.

    `content_enabled` is a real protobuf field, so `Fields(**...)` would take it, but
    the JSON body has no such key: sending it over REST is ignored and the defaults
    apply. The accepted set is the JSON surface, not protobuf's field set.
    """
    with pytest.raises(TypeError, match="fields has no member 'content_enabled'"):
        from_json_unions(Fields, {"content_enabled": True}, "fields")


def test_the_accepted_keys_are_the_group_names() -> None:
    """Fields has two marked oneofs and no plain fields, so those are the only keys."""
    assert _accepted_keys(Fields.DESCRIPTOR) == {"content", "snippets"}


def test_a_value_that_is_neither_is_refused_by_name() -> None:
    """The one check the constructor cannot make: which arm a value belongs in."""
    with pytest.raises(TypeError, match=r"fields\['content'\] takes a boolean"):
        from_json_unions(Fields, {"content": "yes"}, "fields")


def test_a_built_message_passes_through() -> None:
    built = Fields(content_enabled=True)
    assert from_json_unions(Fields, built, "fields") is built


def test_the_parameter_name_is_used_in_errors() -> None:
    """The error names the SDK parameter, which is not always the message name."""
    with pytest.raises(TypeError, match=r"^selection\['content'\]"):
        from_json_unions(Fields, {"content": "yes"}, "selection")


def test_every_unknown_key_is_named_at_once() -> None:
    """One round trip per typo is one too many when the caller made two."""
    typos = ["cont" + "nt", "snip" + "ets"]  # codespell:ignore
    with pytest.raises(TypeError, match="has no member 'contnt', 'snipets'"):
        from_json_unions(Fields, {key: True for key in typos}, "fields")


def test_a_none_inside_a_bag_is_refused() -> None:
    """A computed limit that came back `None` asks for uncapped content silently."""
    with pytest.raises(TypeError, match=r"max_characters_per_result'\] is None"):
        from_json_unions(
            Fields, {"content": {"max_characters_per_result": None}}, "fields"
        )


def test_the_wrong_options_message_is_named() -> None:
    """protobuf's own rejection names neither the parameter nor the key."""
    with pytest.raises(TypeError, match="takes ContentOptions, not SnippetOptions"):
        from_json_unions(
            Fields, {"content": SnippetOptions(max_snippets_per_result=1)}, "fields"
        )
