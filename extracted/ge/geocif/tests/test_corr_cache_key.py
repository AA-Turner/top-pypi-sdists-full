"""Regression test: the correlation/feature-selection cache key must depend on
the CID-selection knobs, not just simulation_stages.

Bug: _correlation_cache_path keyed the pickle on hash(simulation_stages) only.
The cached (dict_selected_features, dict_best_cid) depends on use_cids /
select_cid_by / feature_selection too, and the cache dir is date+country+crop+
year scoped, so two runs that differed only in use_cids (an index sweep, or a
use_cids edit re-run the same day) silently reused stale selected features.
"""
import inspect

from geocif import geocif as gmod


def _src():
    return inspect.getsource(gmod.Geocif._correlation_cache_path)


def test_cache_key_includes_cid_selection_knobs():
    src = _src()
    for attr in ("use_cids", "select_cid_by", "feature_selection"):
        assert attr in src, (
            f"_correlation_cache_path signature must include {attr} so different "
            f"CID selections don't collide on a stale cache"
        )


def test_cache_key_not_stages_only():
    # guard against regressing to the stages-only key
    src = _src()
    assert "correlation_threshold" in src or "use_cids" in src, (
        "cache key must incorporate more than simulation_stages"
    )
