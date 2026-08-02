"""Tests for all ormar_rust_utils exported functions."""

import copy

import ormar_rust_utils


def test_encode_bytes_utf8():
    """Test encoding bytes as UTF-8 string."""
    result = ormar_rust_utils.encode_bytes(b"hello")
    assert result == "hello"


def test_encode_bytes_already_string():
    """Test that strings pass through unchanged."""
    result = ormar_rust_utils.encode_bytes("hello")
    assert result == "hello"


def test_encode_bytes_base64():
    """Test encoding bytes as base64 string."""
    result = ormar_rust_utils.encode_bytes(b"hello", represent_as_string=True)
    assert result == "aGVsbG8="


def test_decode_bytes_utf8():
    """Test decoding UTF-8 string to bytes."""
    result = ormar_rust_utils.decode_bytes("hello")
    assert result == b"hello"


def test_decode_bytes_already_bytes():
    """Test that bytes pass through unchanged."""
    result = ormar_rust_utils.decode_bytes(b"hello")
    assert result == b"hello"


def test_decode_bytes_base64():
    """Test decoding base64 string to bytes."""
    result = ormar_rust_utils.decode_bytes("aGVsbG8=", represent_as_string=True)
    assert result == b"hello"


def test_encode_json_string():
    """Test encoding a JSON string value."""
    result = ormar_rust_utils.encode_json('{"key": "value"}')
    assert result == '{"key":"value"}'


def test_encode_json_dict():
    """Test encoding a dict to JSON."""
    result = ormar_rust_utils.encode_json({"key": "value"})
    assert result == '{"key":"value"}'


def test_encode_json_non_json_string():
    """Test that non-JSON strings pass through."""
    result = ormar_rust_utils.encode_json("not json")
    assert result == "not json"


def test_hash_item_dict():
    """Test hashing a simple dict."""
    result = ormar_rust_utils.hash_item({"b": 2, "a": 1})
    # Should be a sorted tuple of (key, value) pairs
    assert isinstance(result, tuple)
    assert result == (("a", 1), ("b", 2))


def test_hash_item_nested_dict():
    """Test hashing a nested dict."""
    result = ormar_rust_utils.hash_item({"a": {"x": 1}})
    assert isinstance(result, tuple)


def test_hash_item_list():
    """Test hashing a list."""
    result = ormar_rust_utils.hash_item([10, 20, 30])
    assert isinstance(result, tuple)
    assert result == ((0, 10), (1, 20), (2, 30))


def test_translate_list_to_dict_simple():
    """Test translating simple list to dict."""
    result = ormar_rust_utils.translate_list_to_dict(["a", "b"])
    assert "a" in result
    assert "b" in result


def test_translate_list_to_dict_nested():
    """Test translating nested list with __ separator."""
    result = ormar_rust_utils.translate_list_to_dict(["a__b", "a__c"])
    assert "a" in result
    assert isinstance(result["a"], dict)
    assert "b" in result["a"]
    assert "c" in result["a"]


def test_translate_list_to_dict_with_default():
    """Test translate_list_to_dict with custom default."""
    default = {"key": "val"}
    result = ormar_rust_utils.translate_list_to_dict(["x"], copy.deepcopy(default))
    assert result["x"] == default


def test_group_related_list_simple():
    """Test grouping simple related list."""
    result = ormar_rust_utils.group_related_list(["people__houses", "people__cars"])
    assert "people" in result
    assert set(result["people"]) == {"cars", "houses"}


def test_group_related_list_nested():
    """Test grouping with nested relations."""
    result = ormar_rust_utils.group_related_list(
        ["people__cars__models", "people__cars__colors"]
    )
    assert "people" in result
    assert isinstance(result["people"], dict)
    assert "cars" in result["people"]


def test_unique_list_empty():
    """Test creating an empty UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    assert len(ul) == 0


def test_unique_list_append():
    """Test appending to UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    ul.append(1)
    ul.append(2)
    ul.append(1)  # duplicate
    assert len(ul) == 2


def test_unique_list_contains():
    """Test membership check in UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    ul.append(42)
    assert 42 in ul
    assert 99 not in ul


def test_unique_list_getitem():
    """Test indexing UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    ul.append("a")
    ul.append("b")
    assert ul[0] == "a"
    assert ul[1] == "b"
    assert ul[-1] == "b"


def test_unique_list_iter():
    """Test iterating over UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    ul.append(1)
    ul.append(2)
    assert list(ul) == [1, 2]


def test_unique_list_bool():
    """Test bool conversion of UniqueList."""
    ul = ormar_rust_utils.UniqueList()
    assert not ul
    ul.append(1)
    assert ul


def test_unique_list_initial():
    """Test creating UniqueList with initial values."""
    ul = ormar_rust_utils.UniqueList([1, 2, 3, 2])
    assert len(ul) == 3


def test_group_by_pk():
    """Test grouping by primary key."""
    pks = [1, 2, 1, 3, 2]
    result = ormar_rust_utils.group_by_pk(pks)
    assert len(result) == 3
    # First group should be indices of pk=1
    assert result[0] == [0, 2]
    assert result[1] == [1, 4]
    assert result[2] == [3]


def test_plan_merge_items_lists():
    """Test creating a merge plan."""
    current_pks = [1, 2, 3]
    other_pks = [2, 4]
    plan = ormar_rust_utils.plan_merge_items_lists(current_pks, other_pks)
    assert len(plan) == 3
    # pk=1 not in other
    assert plan[0] == (0, None)
    # pk=2 is at index 0 in other
    assert plan[1] == (1, 0)
    # pk=3 not in other
    assert plan[2] == (2, None)


def test_plan_merge_items_lists_empty():
    """Test merge plan with empty lists."""
    plan = ormar_rust_utils.plan_merge_items_lists([], [])
    assert plan == []


def test_build_reverse_alias_map_basic():
    """Test building reverse alias map with aliases."""
    field_alias_map = {"name": "user_name", "age": "user_age"}
    result = ormar_rust_utils.build_reverse_alias_map(field_alias_map)
    # alias -> field_name
    assert result["user_name"] == "name"
    assert result["user_age"] == "age"
    # identity entries for field names
    assert result["name"] == "name"
    assert result["age"] == "age"


def test_build_reverse_alias_map_identity():
    """Test reverse alias map when alias equals field name."""
    field_alias_map = {"name": "name", "age": "age"}
    result = ormar_rust_utils.build_reverse_alias_map(field_alias_map)
    assert result["name"] == "name"
    assert result["age"] == "age"
    assert len(result) == 2


def test_build_reverse_alias_map_empty():
    """Test reverse alias map with empty input."""
    result = ormar_rust_utils.build_reverse_alias_map({})
    assert len(result) == 0
