"""Sphinx directives: the flag bits and the flag criteria, read from the code.

    .. flag-bits::
    .. flag-criteria::

``flag-bits`` draws the 24 bits of the observation flag -- number, value
and meaning -- from ``BIT_DESCRIPTIONS`` in pikobs/configobs/flag_groups.py.

``flag-criteria`` draws the criteria accepted by FLAGS_CRITERIA -- name,
bits that must be set, bits that must not, what it keeps -- from the
docstring of ``pikobs.configobs.flags_criteria.flag_criteria``, where
every criterion is written as

    ``name``
        **What it keeps:** * **Required Active Bits:** **BIT12** (4096) ...
        * **Required Inactive Bits:** **BIT9** (512) ...

Both are read when the site is built, so the page follows the code.
"""
import importlib
import inspect
import re

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

ENTRY = re.compile(r"^    ``(?P<name>\w+)``\s*$")
TITLE = re.compile(r"\*\*(?P<t>[^*]+?):?\*\*")
BITS = re.compile(r"BIT(\d+)")


def _list_table(header, rows, widths):
    out = [".. list-table::", "   :header-rows: 1", f"   :widths: {widths}", ""]
    for i, row in enumerate([header] + rows):
        for j, cell in enumerate(row):
            out.append(("   * - " if j == 0 else "     - ") + (cell or " "))
    return out


def _depends(directive, mod):
    """Rebuild the page when the module it was read from changes."""
    env = getattr(directive.state.document.settings, "env", None)
    if env is not None and getattr(mod, "__file__", None):
        env.note_dependency(mod.__file__)


def _parse(directive, lines):
    holder = nodes.container()
    directive.state.nested_parse(StringList(lines, source=directive.name),
                                 directive.content_offset, holder)
    return holder.children


def _bits_of(block, label):
    """Bit numbers listed after 'Required <label> Bits', up to the next rule."""
    m = re.search(rf"Required {label} Bits:(.*?)(?:Required \w+ Bits:|$)", block, re.S)
    if not m:
        return []
    return sorted(set(BITS.findall(m.group(1))), key=int)


def criteria_rows(doc):
    """(name, title, set, not set) of every criterion of the docstring."""
    lines = inspect.cleandoc("    " + doc).splitlines() if doc else []
    # cleandoc drops the common indent; put the 4-space entry indent back
    lines = ["    " + l if l.strip() else l for l in lines]
    rows, i = [], 0
    while i < len(lines):
        m = ENTRY.match(lines[i])
        if not m:
            i += 1
            continue
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or lines[j].startswith("        ")):
            j += 1
        block = " ".join(l.strip() for l in lines[i + 1:j])
        t = TITLE.search(block)
        title = t.group("t").strip() if t else ""
        on, off = _bits_of(block, "Active"), _bits_of(block, "Inactive")
        if "No restrictions" in block:
            on = off = []
        rows.append((m["name"], title, on, off))
        i = j
    return rows


class FlagBits(Directive):
    has_content = False

    def run(self):
        mod = importlib.import_module("pikobs.configobs.flag_groups")
        _depends(self, mod)
        rows = [[f"``{b}``", f"``{1 << b}``", d]
                for b, d in sorted(mod.BIT_DESCRIPTIONS.items())]
        return _parse(self, _list_table(["Bit", "Value", "Meaning"], rows, "10 16 74"))


class FlagCriteria(Directive):
    has_content = False

    def run(self):
        mod = importlib.import_module("pikobs.configobs.flags_criteria")
        _depends(self, mod)
        rows = []
        for name, title, on, off in criteria_rows(mod.flag_criteria.__doc__ or ""):
            rows.append([f"``{name}``",
                         ", ".join(on) or "--",
                         ", ".join(off) or "--",
                         title])
        if not rows:
            return [self.state_machine.reporter.warning(
                "flag-criteria: no criterion found in the docstring of flag_criteria",
                line=self.lineno)]
        return _parse(self, _list_table(
            ["Criterion", "Bits set", "Bits not set", "What it keeps"], rows, "22 13 13 52"))


def setup(app):
    app.add_directive("flag-bits", FlagBits)
    app.add_directive("flag-criteria", FlagCriteria)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
