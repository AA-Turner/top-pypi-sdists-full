"""The project-naming pass sees file CONTENT, not just the tree.

A contract test, deliberately narrow. The recursive-descent design that was
considered for deep folders proposed a "structure only" survey -- name the
projects from the directory tree, then assign subtrees against that fixed list.
It was rejected because the module's own doctrine says the tree is the one
signal that does not carry the answer, and because a wrong global list is
unrecoverable: `classify_chunked` parks out-of-list slugs into the first spec
at low confidence, so every later chunk is force-fitted to it.

If someone builds recursion later, this is the constraint they must not break.
"""

from __future__ import annotations

import inspect

from probe.cli import backfill_prompts as prompts
from probe.cli import backfill_run


def test_the_survey_prompt_takes_evidence():
    """Not a directory listing. `evidence_jsonl` carries the sampled heads."""
    assert "evidence_jsonl" in inspect.signature(prompts.survey).parameters


def test_the_survey_is_called_with_evidence_not_a_tree():
    source = inspect.getsource(backfill_run.classify_chunked)
    assert "prompts.survey(" in source
    assert "evidence_jsonl=" in source


def test_naming_and_assignment_are_separate_passes():
    """The global pass is what keeps a project that spans three directories
    from fragmenting across three subtree-local decisions."""
    source = inspect.getsource(backfill_run.classify_chunked)
    assert "prompts.assign_chunk(" in source, "assignment is its own pass"


def test_the_doctrine_is_written_down_where_it_will_be_read():
    """The reason lives next to the code it constrains, not only in a review."""
    doc = inspect.getdoc(prompts.classify) or ""
    module_doc = inspect.getdoc(prompts) or ""
    assert "per-file" in (doc + module_doc).lower()
