from __future__ import annotations

import pytest

from agentic_devtools.cli.jira.creation_pipeline import (
    PipelineValidationError,
    _build_execution_order,
    _validate_start_from_prerequisites,
)

from .conftest import make_context, make_tree


def test_accepts_resume_when_skipped_prerequisites_are_mapped() -> None:
    tree = make_tree(with_blocking=True)
    base_context = make_context(tree)
    context = base_context.__class__(
        tree=tree,
        provider=base_context.provider,
        provider_name="github",
        node_index=base_context.node_index,
        start_from="s1",
    )
    ordered_refs = _build_execution_order(context)

    _validate_start_from_prerequisites(
        context,
        ordered_refs,
        ordered_refs.index("s1"),
        {"e1": "1", "f1": "2", "s2": "3"},
    )


def test_rejects_missing_blocker_mapping() -> None:
    tree = make_tree(with_blocking=True)
    base_context = make_context(tree)
    context = base_context.__class__(
        tree=tree,
        provider=base_context.provider,
        provider_name=base_context.provider_name,
        node_index=base_context.node_index,
        start_from="s1",
    )
    ordered_refs = _build_execution_order(context)

    with pytest.raises(PipelineValidationError, match="s2"):
        _validate_start_from_prerequisites(context, ordered_refs, ordered_refs.index("s1"), {"f1": "1"})


def test_rejects_missing_ancestor_mapping() -> None:
    tree = make_tree()
    base_context = make_context(tree)
    context = base_context.__class__(
        tree=tree,
        provider=base_context.provider,
        provider_name=base_context.provider_name,
        node_index=base_context.node_index,
        start_from="s1",
    )
    ordered_refs = _build_execution_order(context)

    with pytest.raises(PipelineValidationError, match="e1"):
        _validate_start_from_prerequisites(context, ordered_refs, ordered_refs.index("s1"), {"f1": "1"})


def test_rejects_any_unmapped_prefix_node() -> None:
    tree = make_tree(empty_feature=True)
    base_context = make_context(tree)
    context = base_context.__class__(
        tree=tree,
        provider=base_context.provider,
        provider_name=base_context.provider_name,
        node_index=base_context.node_index,
        start_from="f2",
    )
    ordered_refs = _build_execution_order(context)

    with pytest.raises(PipelineValidationError, match="f1"):
        _validate_start_from_prerequisites(context, ordered_refs, ordered_refs.index("f2"), {"e1": "1"})
