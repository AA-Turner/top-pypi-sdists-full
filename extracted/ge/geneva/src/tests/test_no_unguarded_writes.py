# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Regression guard: durable writes should go through their injectable indirection.

geneva routes durable writes through swappable indirections so a test can install a
fault-injecting implementation once and cover every site. A raw call that bypasses the
indirection is invisible to fault injection. This is a textual guard over the known
direct-call patterns below; it fails if a new raw durable-write call appears under
``src/geneva`` (it does not catch a call reached through an alias or rebound name, or
prose inside a docstring):

* ``lance.LanceDataset.commit(`` -> ``get_committer().commit``
* ``._ltbl.add/update/delete(`` -> ``get_table_writer()``
* ``._ltbl.update_field_metadata(`` -> ``get_field_metadata_writer().update``
* ``write_fragment_file(`` -> ``get_fragment_file_writer().write``
* ``lance.write_dataset(`` -> no indirection; only the empty-table fallback uses it
* ``lance.fragment.write_fragments(`` / ``.delete_rows(`` -> sparse-update writes, not
  yet routed; the sparse sweep flavor faults only at the commit boundary today
* ``LanceFragment.create(`` -> chunker/UDTF fragment write, not yet routed; the chunker
  sweep flavor faults only at the commit boundary today

A site that is itself the routed default (or genuinely must call raw) carries an opt-out
marker ``# write-guard-ok: <reason>`` on the call line or the line above. ``def`` lines
(the definition, not a call) are ignored.
"""

import pathlib

_GENEVA_SRC = pathlib.Path(__file__).resolve().parents[1] / "geneva"
_MARKER = "write-guard-ok"
_FORBIDDEN = (
    "lance.LanceDataset.commit(",
    "._ltbl.add(",
    "._ltbl.update(",
    "._ltbl.delete(",
    "._ltbl.update_field_metadata(",
    "write_fragment_file(",
    "lance.write_dataset(",
    "lance.fragment.write_fragments(",
    ".delete_rows(",
    "LanceFragment.create(",
)


def _code_part(line: str) -> str:
    """The line with any trailing comment stripped, so a token that only appears in a
    comment (prose or the opt-out marker) does not count as a call site."""
    return line.split("#", 1)[0]


def test_no_unguarded_durable_writes() -> None:
    violations: list[str] = []
    for path in sorted(_GENEVA_SRC.rglob("*.py")):
        lines = path.read_text().splitlines()
        in_docstring = False
        for i, line in enumerate(lines):
            # Skip lines inside triple-quoted strings so a forbidden token mentioned in
            # prose (a docstring) does not count as a call site. An odd number of triple
            # quotes on a line toggles in/out of a multi-line string.
            if (line.count('"""') + line.count("'''")) % 2 == 1:
                in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            code = _code_part(line)
            if code.lstrip().startswith("def "):
                continue  # the function definition, not a call site
            if not any(tok in code for tok in _FORBIDDEN):
                continue
            prev = lines[i - 1] if i > 0 else ""
            if _MARKER in line or _MARKER in prev:
                continue
            rel = path.relative_to(_GENEVA_SRC.parent)
            violations.append(f"{rel}:{i + 1}: {line.strip()}")

    assert not violations, (
        "raw durable-write call(s) that bypass the injectable indirection "
        "(get_committer / get_table_writer / get_field_metadata_writer / "
        "get_fragment_file_writer). Route through the indirection so fault injection "
        "covers the site, or add an opt-out comment '# write-guard-ok: <reason>':\n  "
        + "\n  ".join(violations)
    )
