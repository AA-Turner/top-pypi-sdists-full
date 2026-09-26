"""THE ONE ``{{variable}}`` substitution rule: only placeholders the AUTHOR wrote
are slots; everything a value brings in is data.

A variable's value is data — a document, an answer, a transcript. When it
contains ``{{something}}`` (a mail-merge template, a chat answer quoting its own
variables, a Handlebars snippet) those braces are part of the data. Before this
module they were not:

* the per-variable ``str.replace`` loop re-scanned text it had just inserted, so
  a value holding ``{{other_var}}`` was filled with ``other_var``'s value, and
* substitution runs in several passes (agent definition, then the run's
  variables), and every later pass took the previous pass's OUTPUT as its
  "template" — so braces that arrived inside a value were counted as authored
  placeholders and announced to the model as "NOT DELIVERED". A Clean up run on
  a chat answer holding ``{{pilot_region}}`` replied only "{{pilot_region}} was
  not delivered." (verify-RC-B5 round 3, conversation 119f9545).

So every pass substitutes against the text's FIRST-SEEN form (its authored
template): a name is a slot only if ``{{name}}`` is in that template, all slots
are filled in ONE pass (inserted text is never re-scanned), and the unresolved
check reads the same template.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from typing import Any


def authored_names(template: str, variables: Mapping[str, Any]) -> list[str]:
    """Variable names whose ``{{name}}`` the author wrote in ``template``."""
    return [name for name in variables if f"{{{{{name}}}}}" in template]


def substitute_authored(
    text: str,
    template: str,
    variables: Mapping[str, Any],
    render: Callable[[Any], str],
) -> str:
    """Fill the author's slots in ``text`` in one pass; never touch braces a value brought."""
    names = authored_names(template, variables)
    if not names or "{{" not in text:
        return text
    names.sort(key=len, reverse=True)
    pattern = re.compile(r"\{\{(" + "|".join(re.escape(n) for n in names) + r")\}\}")
    rendered = {name: render(variables[name]) for name in names}
    return pattern.sub(lambda m: rendered[m.group(1)], text)
