from agentic_devtools.cli.setup.copilot_settings import _json_values_match


def test_returns_false_for_type_equivalent_scalar_mismatch():
    assert not _json_values_match(1, True)


def test_returns_false_for_dict_key_mismatch():
    assert not _json_values_match({"enabled": True}, {"missing": True})


def test_returns_false_for_list_length_mismatch():
    assert not _json_values_match([True], [True, True])


def test_returns_true_for_nested_json_value_match():
    assert _json_values_match([{"enabled": True}], [{"enabled": True}])
