"""Pick lists are ONE agent tool: ``pick_list``.

Also covers the retired table tools (``usertable_*``, ``user_table_add_row``, ``data_user_*``) and
the ``dataset`` tool, renamed ``table`` on 2026-10-07 (lexicon: Table; dataset is a retired alias):
a person's tables are read and written through ``records_*`` or the ``table`` tool. The old name
alias was removed 2026-10-07 once every running task served ``table``; ``dataset_id`` / ``dataset_name``
were renamed ``table_id`` / ``table_name`` (DB parameters 2026-10-07); no alias accepts them.

Breaks if the retired tool names come back: the ``picklist`` tool, the six ``userlist_*``
helpers, the ``picklists_tools`` module, or the ``PicklistArgs`` model. The scan covers this
package's code and tests (tool names are plain strings, so the registry check alone could not
see a stray executor or a test calling a name that no longer exists).
"""

from __future__ import annotations

import re
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent
RETIRED = re.compile(
    r"\buserlist_(create|create_simple|get_all|get_details|update_item|batch_update)\b"
    r"|picklists_tools|\bPicklistArgs\b|\bPicklistToolResult\b|\bpicklist_(id|name)\b"
    r"|tool_name\s*=\s*[\"']picklist[\"']"
    # Tables: the usertable_* family was retired with the old data tables.
    r"|\busertable_\w+|\buser_table_add_row\b|\bdata_user_(lists|tables)\w*"
    # The table tool's retired name: its module, args model, call name and census keys.
    r"|datasets_tools|\bDatasetArgs\b|tool_name\s*=\s*[\"']dataset[\"']|[\"']dataset:[a-z_]+[\"']"
    r"|\bdef dataset\(|frozenset\(\{[^}]*[\"']dataset[\"']"
    # The table tool's retired wire names, as the implementation would read them back.
    # The table tool's retired result kinds (renamed table_* 2026-10-07; the registry rows are retired).
    r"|\bdataset_(tool|metadata|fields)_result\b|\bDataset(Tool|Metadata|Fields)Result\b"
    r"|args\.get\(\s*[\"']dataset_(id|name)[\"']|AliasChoices\([^)]*[\"']dataset_(id|name)[\"']|\bDataset(List|Get|Search|Create|AddRows|UpdateRow|DeleteRow)Wire\b"
)
SELF = Path(__file__).name


def scan(root: Path) -> list[str]:
    hits: list[str] = []
    for path in root.rglob("*.py"):
        if SELF == path.name or ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if RETIRED.search(line):
                hits.append(f"{path.relative_to(root)}:{number}: {line.strip()[:100]}")
    return hits


def test_the_registry_has_one_pick_list_tool_and_no_old_names():
    import matrx_ai.tools._generated_declarations  # noqa: F401 - registers every tool
    from matrx_ai.tools import declared
    from matrx_ai.tools.declared import declared_tools

    names = set(declared_tools())
    assert "pick_list" in names
    assert not {"picklist"} & names
    assert not {n for n in names if n.startswith("userlist_")}
    assert not {n for n in names if n.startswith(("usertable_", "user_table_"))}
    assert "table" in names and "dataset" not in names
    # The rename window is closed: no tool answers to `dataset` any more.
    assert "dataset" not in declared._ALIAS_INDEX


def test_the_guard_sees_the_retired_dataset_tool_name(tmp_path):
    (tmp_path / "a.py").write_text('KEYS = {"dataset:add_rows": 1}\nctx = Ctx(tool_name="dataset")\n')
    assert len(scan(tmp_path)) == 2


def test_the_guard_sees_the_retired_dataset_result_kinds(tmp_path):
    (tmp_path / "a.py").write_text(
        'ToolResult(output_kind="dataset_fields_result")\nclass DatasetToolResult: ...\n'
        '@kind("dataset_metadata_result")\n'
    )
    assert len(scan(tmp_path)) == 3


def test_the_server_kind_modules_name_only_the_table_result_kinds():
    root = PACKAGE.parent.parent / "aidream" / "kinds"
    assert (root / "ci_boundary_contracts.py").exists()
    assert scan(root) == []
    import aidream.kinds.ci_boundary_contracts  # noqa: F401 - registers its kinds
    import matrx_ai.tools.kinds.personal_content  # noqa: F401
    from matrx_graph.content_ir.sdk import kind_catalog

    slugs = set(kind_catalog())
    assert {"table_tool_result", "table_metadata_result", "table_fields_result"} <= slugs
    assert not {"dataset_tool_result", "dataset_metadata_result", "dataset_fields_result"} & slugs


def test_every_success_of_the_table_tool_declares_a_table_kind():
    from matrx_ai.tools.implementations import table_tools

    ctx = type("Ctx", (), {"call_id": "c1"})()
    ok = table_tools._stamp(table_tools.ToolResult(success=True, output={"rows": []}), 0.0, ctx)
    assert ok.output_kind == "table_tool_result"
    held = table_tools._stamp(
        table_tools.ToolResult(success=True, output={"held_for_approval": True}), 0.0, ctx
    )
    assert not held.output_kind
    failed = table_tools._stamp(table_tools.ToolResult(success=False), 0.0, ctx)
    assert not failed.output_kind


def test_the_guard_sees_a_retired_table_tool_name(tmp_path):
    (tmp_path / "a.py").write_text('call("usertable_create")\n')
    assert scan(tmp_path)


def test_no_code_or_test_in_the_package_uses_a_retired_name():
    assert scan(PACKAGE) == []
