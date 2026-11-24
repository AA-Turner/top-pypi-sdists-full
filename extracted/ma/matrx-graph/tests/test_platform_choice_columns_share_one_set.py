"""#91 guard: every output table's platform choice columns name ONE shared choices set per organization.

The store (custom._options_table_shared_or_new, called by custom._field_declare_plan) finds or makes
the organization's single set by ``config.shared_choices``. Without the marker each "<Kind> outputs"
table made its own "State choices" and "Reason choices" tables (2 per output table, 169 in 3 days).
Red before the fix: the declarations carried no marker.
"""

from __future__ import annotations

from matrx_graph.kind_fields import PLATFORM_KEYS, _platform_fields


def test_each_platform_choice_column_names_its_shared_set() -> None:
    by_key = {f.declaration["key"]: f.declaration for f in _platform_fields()}
    choice_keys = [k for k in PLATFORM_KEYS if by_key[k].get("options")]
    assert set(choice_keys) == {"output_state", "output_reason"}
    for key in choice_keys:
        assert by_key[key]["config"].get("shared_choices") == f"agent_output.{key}", key
        assert by_key[key]["config"].get("kept_by") == "agent_output"


def test_a_non_choice_platform_column_carries_no_marker() -> None:
    for declaration in (f.declaration for f in _platform_fields()):
        if not declaration.get("options"):
            assert "shared_choices" not in declaration["config"], declaration["key"]
