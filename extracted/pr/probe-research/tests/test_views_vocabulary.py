"""The generated view vocabulary must be current, and must cover what we serve.

Two failures this catches, and they are different:

  * the generated file is STALE -- somebody changed the vocabulary in research-os
    and did not run `make gen-views`, so this package speaks last release's words
    while the backend has moved on;
  * this server serves a (kind, view) pair the vocabulary has never heard of --
    the divergence the whole generated-vocabulary arrangement exists to prevent,
    which is how two agent surfaces end up with two words for one read.

The first check is skipped when a research-os checkout is not importable, which
in `agent-ci` is ALWAYS -- that lane runs with `working-directory: agent` and
`pythonpath = ["."]`, so `app.core` is never on the path. It is kept here for the
developer running it locally against a checkout, and the check that actually
gates CI lives in the backend suite
(`tests/unit/test_agent_view_vocabulary_is_generated.py`), which is the one lane
that installs BOTH trees. A guard that can only skip is not a guard, and this
file used to be the only home for it.

The second never skips: it needs nothing but this package.
"""

from __future__ import annotations

import pytest

from probe.mcp.contract import VIEW_MATRIX, View
from probe.mcp.service import _VIEWS


def test_every_served_pair_is_in_the_shared_vocabulary() -> None:
    """`_VIEWS` is what this server actually answers. A pair in it that the
    matrix does not hold is a word this surface invented alone."""
    unknown = sorted(
        f"{kind}/{view}"
        for (kind, view) in _VIEWS
        if view not in VIEW_MATRIX.get(kind, frozenset())
    )
    assert not unknown, (
        f"this server serves {unknown}, which the shared vocabulary does not "
        "declare. Add it to research-os app/core/agent_views.py and run "
        "`make gen-views` -- do not hand-edit the generated file."
    )


def test_the_generated_vocabulary_is_current() -> None:
    """Regenerating must be a no-op. If it is not, this package is speaking a
    vocabulary the backend has already changed."""
    agent_views = pytest.importorskip(
        "app.core.agent_views",
        reason="research-os is not importable here; run this where it is",
    )
    # NAMES AND VALUES BOTH. Values alone let a RENAME through -- `README` to
    # `READ_ME` with the string unchanged -- and the next regen then renames the
    # symbol out from under every `View.README` in this package.
    source_views = {(v.name, v.value) for v in agent_views.View}
    generated = {(v.name, v.value) for v in View}
    assert generated == source_views, (
        "the generated view vocabulary is stale -- run `make gen-views`. "
        f"missing here: {sorted(source_views - generated)}; "
        f"extra here: {sorted(generated - source_views)}"
    )
    source_matrix = {
        k.value: {v.value for v in vs} for k, vs in agent_views.VIEW_MATRIX.items()
    }
    generated_matrix = {k.value: {v.value for v in vs} for k, vs in VIEW_MATRIX.items()}
    assert generated_matrix == source_matrix, (
        "the generated view MATRIX is stale -- run `make gen-views`"
    )
