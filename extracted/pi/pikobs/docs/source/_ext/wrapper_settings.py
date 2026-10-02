"""Sphinx directive: a module's configuration, read from its wrappers.

    .. wrapper-settings:: run_zone_exp.sh run_zone_cont_exp.sh

reads the USER SETTINGS block of the named wrappers (in pikobs/script) and
draws one table per group of variables -- default and what it sets -- with
pikobs/build_doc/settings_table.py. The page is rebuilt whenever one of
the wrappers changes, so the documentation never shows a default the
wrapper no longer has.
"""
import os
import sys

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SCRIPTS = os.path.join(REPO, "pikobs", "script")
sys.path.insert(0, os.path.join(REPO, "pikobs", "build_doc"))

from settings_table import settings_tables  # noqa: E402


class WrapperSettings(Directive):
    required_arguments = 1
    optional_arguments = 4
    has_content = False

    def run(self):
        paths = [os.path.join(SCRIPTS, a) for a in self.arguments]
        missing = [os.path.basename(p) for p in paths if not os.path.isfile(p)]
        if missing:
            return [self.state_machine.reporter.warning(
                f"wrapper-settings: no such wrapper: {', '.join(missing)}",
                line=self.lineno)]
        env = getattr(self.state.document.settings, "env", None)
        if env is not None:
            for p in paths:
                env.note_dependency(p)
        rst = settings_tables(paths)
        holder = nodes.container()
        self.state.nested_parse(StringList(rst.splitlines(), source="wrapper-settings"),
                                self.content_offset, holder)
        return holder.children


def setup(app):
    app.add_directive("wrapper-settings", WrapperSettings)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
