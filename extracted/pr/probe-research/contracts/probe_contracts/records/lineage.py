"""Lineage vocabulary: what an edge may connect, and the closed set of relations it may carry."""

from __future__ import annotations

from ..compat import StrEnum


class LineageEntityType(StrEnum):
    """The endpoints a lineage edge can connect (closed set)."""

    RUN = "run"
    ARTIFACT = "artifact"
    ARTIFACT_VERSION = "artifact_version"
    #: 0180. Papers share this edge table: 0166 spent a per-tenant backfill closing a split between two
    #: systems that said the same thing, and a second edge table would reopen it.
    PAPER = "paper"
    #: 0278 (lineage plan 2, L12): a project or experiment (both `projects` rows). Takes the relations in
    #: `PROJECT_END_RELATIONS` (app/lineage/schemas.py), plus `forked_from` via `create_fork_edge` only.
    PROJECT = "project"
    #: 0342 (data catalog): an external source (Hub dataset, bucket prefix, url, base model) at a chain's
    #: start (`external_sources`). Allowed edges: `EdgeCreate._source_ends`; DESIGN.md (lineage.py).
    SOURCE = "source"


class LineageRelation(StrEnum):
    """The closed relation vocabulary.

    Two families, and the split is what the prompt teaches:

    GENEALOGY (run -> run) is "another attempt at the same thing". A run may have
    more than one such parent since 0275 (a retry of one run and a branch of
    another); the FIRST one is mirrored in `runs.parent_run_id`.
    DATAFLOW is "this used that", stays many-to-many, and is the only family with an
    artifact at either end today.

    `retried_from`/`branched_from` arrived in 0166 with run -> run genealogy;
    `retry` and `branch` were 18 of the 24 rows migrated out of
    `runs.parent_relation` and had no equivalent here at all.
    """

    # Dataflow (many-to-many).
    CONSUMES = "consumes"
    PRODUCES = "produces"
    EVALUATES_ON = "evaluates_on"
    PROMOTED_TO = "promoted_to"
    DERIVED_FROM = "derived_from"
    # Genealogy (run -> run; the first one is runs.parent_run_id).
    FORKED_FROM = "forked_from"
    RESUMED_FROM = "resumed_from"
    RETRIED_FROM = "retried_from"
    BRANCHED_FROM = "branched_from"
    # Discovery (paper -> paper, many-to-many).
    #: 0180. Source = the paper FOUND, target = the paper it was found FROM (genealogy's direction). Not
    #: `derived_from`, and not in GENEALOGY_RELATIONS (app/lineage/schemas.py): DESIGN.md (lineage.py).
    DISCOVERED_VIA = "discovered_via"
    # Replacement and sources (0276).
    #: Source REPLACES target (a rerun after a fix supersedes the buggy run); run -> run for now. Says
    #: which result to trust, not where it came from, so never touches `runs.parent_run_id`.
    SUPERSEDES = "supersedes"
    #: A run or file -> the paper whose method or finding it uses. Carries a
    #: provenance like every edge that touches a paper.
    INFORMED_BY = "informed_by"
    # How two papers relate (0357).
    #: Paper -> an EARLIER paper in the same project, with a reason (`paper add --relates-to`); no cycle check.
    #: Reason required by the API, never a CHECK: app/sessions/erasure.py nulls one that quotes a session.
    RELATES_TO = "relates_to"
