"""THE ARCHIVED-ITEMS LAW at the workflow list reader.

Arman, 2026-09-09 (``common-docs/policies/archived-items.md``): every list over
an archivable entity carries an archive filter, the default hides archived
rows, and revealing them is one click. ``DefinitionStore.list_for_user`` is the
reader behind workflow-studio's ``/workflows`` list, so the tri-state has to be
real HERE — a control over a reader that cannot express "archived only" is a
control that lies.

These assert the predicate the ORM receives, which is what decides which rows
the database returns; they fail if the default ever stops hiding archived rows,
if ``all`` starts filtering, or if a typo'd value is silently swallowed.
"""

from __future__ import annotations

import pytest

from matrx_graph.db.definition_store import (
    ARCHIVED_FILTER_VALUES,
    DEFAULT_ARCHIVED_FILTER,
    _archived_predicate,
)
from matrx_graph.errors import DefinitionError


def test_the_default_hides_archived_rows() -> None:
    # Clause 2 of the law. If this flips, every workflow list in every client
    # starts showing archived rows on first open.
    assert DEFAULT_ARCHIVED_FILTER == "active"
    assert _archived_predicate(DEFAULT_ARCHIVED_FILTER) == {"is_archived": False}


def test_the_three_states_are_the_platform_vocabulary() -> None:
    # Same words as the wfx_list_scoped / agx_list_scoped `p_archived` RPC
    # parameter and the clients' shared ArchiveFilter control.
    assert ARCHIVED_FILTER_VALUES == {"active", "archived", "all"}


def test_archived_only_is_expressible() -> None:
    # The reason a boolean was not enough: "show me what I archived" is a real
    # question and the old include_archived=True could only answer "both".
    assert _archived_predicate("archived") == {"is_archived": True}


def test_all_applies_no_archive_predicate() -> None:
    assert _archived_predicate("all") == {}


@pytest.mark.parametrize("value", ["Active", "ARCHIVED", "  all  "])
def test_case_and_whitespace_are_tolerated(value: str) -> None:
    # A URL param arrives as text; tolerating case is not the same as
    # tolerating an unknown word.
    assert _archived_predicate(value) == _archived_predicate(value.strip().lower())


@pytest.mark.parametrize("value", ["both", "true", "yes", "unarchived", "", "  "])
def test_an_unrecognised_value_screams_instead_of_leaking(value: str) -> None:
    # NOTHING FAILS SILENTLY. A caller who believes it is filtering and is not
    # would ship archived rows into a list that promises they are hidden —
    # except "" / whitespace, which is an absent value and takes the default.
    if value.strip():
        with pytest.raises(DefinitionError) as excinfo:
            _archived_predicate(value)
        assert "archived must be one of" in str(excinfo.value)
    else:
        assert _archived_predicate(value) == {"is_archived": False}
