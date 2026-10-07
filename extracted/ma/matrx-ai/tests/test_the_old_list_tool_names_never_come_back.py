"""Pick lists are ONE agent tool: ``pick_list``.

Also covers the retired table tools (``usertable_*``, ``user_table_add_row``, ``data_user_*``): a
person's tables are read and written through ``records_*`` or the ``dataset`` tool.

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
    from matrx_ai.tools.declared import declared_tools

    names = set(declared_tools())
    assert "pick_list" in names
    assert not {"picklist"} & names
    assert not {n for n in names if n.startswith("userlist_")}
    assert not {n for n in names if n.startswith(("usertable_", "user_table_"))}


def test_the_guard_sees_a_retired_table_tool_name(tmp_path):
    (tmp_path / "a.py").write_text('call("usertable_create")\n')
    assert scan(tmp_path)


def test_no_code_or_test_in_the_package_uses_a_retired_name():
    assert scan(PACKAGE) == []
