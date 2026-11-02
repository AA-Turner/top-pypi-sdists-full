"""Guard — canonical cluster expansion must stay OPT-IN.

Cluster expansion broadens the entity-recall lane to a matched entity's KG-cluster
siblings. That is a recall-vs-precision trade whose right default is an EVAL
decision, not a blind on. If a refactor ever flips `expand_entity_clusters` /
`expand_clusters` to default True, precision could silently regress for every
search. This locks the default to False at both the public `search()` boundary
and the internal `_entity_recall` lane. Pure signature introspection — no DB.

(The cluster-expansion behavior itself is DB-coupled and is verified live against
the backfilled corpus, not mocked here — see scripts/backfill_entity_clustering.py.)
"""

from __future__ import annotations

import inspect

from matrx_rag.search import _ENTITY_CLUSTER_EXPANSION_CAP, _recall_entity_door as _entity_recall, search


def test_search_expand_entity_clusters_defaults_off():
    default = inspect.signature(search).parameters["expand_entity_clusters"].default
    assert default is False, (
        f"search() expand_entity_clusters must default to False (opt-in recall "
        f"broadening); got {default!r}."
    )


def test_entity_recall_expand_clusters_defaults_off():
    default = inspect.signature(_entity_recall).parameters["expand_clusters"].default
    assert default is False, (
        f"_entity_recall expand_clusters must default to False; got {default!r}."
    )


def test_expansion_cap_is_bounded():
    # A cluster can be large; the cap keeps a single theme from flooding the
    # entity lane. Must be a small positive int.
    assert isinstance(_ENTITY_CLUSTER_EXPANSION_CAP, int)
    assert 0 < _ENTITY_CLUSTER_EXPANSION_CAP <= 200
