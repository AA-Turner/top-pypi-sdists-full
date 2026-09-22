"""Tests for the LimiX-2 wrapper (geocif.ml.limix).

These do NOT need LimiX, torch-CUDA or the checkpoint: they exercise the
plumbing that broke in practice — the process-wide predictor cache, and the
import guard that fires when someone runs model='limix' in the production
Python 3.11 env instead of the side env.
"""

import pytest

from geocif.ml import limix as limix_mod


@pytest.fixture(autouse=True)
def _clear_caches():
    limix_mod._PREDICTOR_CACHE.clear()
    limix_mod._CKPT_CACHE.clear()
    yield
    limix_mod._PREDICTOR_CACHE.clear()
    limix_mod._CKPT_CACHE.clear()


def test_predictor_is_built_once_per_key():
    """Regression: geocif builds a model object per fold.

    Before the cache, each fold re-loaded the 1.63 GB checkpoint onto the GPU
    and never freed the previous one — a Kenya run reached 22.1 GB of the
    RTX 6000's 23.0 GB within four folds. Same key must build exactly once.
    """
    calls = []

    def build():
        calls.append(1)
        return object()

    key = ("/ckpt/LimiX-2.ckpt", "/cfg/reg.json", "cuda")
    first = limix_mod._cached_predictor(key, build)
    for _ in range(25):  # stand-in for 25 folds
        assert limix_mod._cached_predictor(key, build) is first
    assert len(calls) == 1


def test_changing_key_rebuilds_and_keeps_only_one():
    """A different checkpoint/device rebuilds, and the old one is released."""
    made = []

    def build():
        obj = object()
        made.append(obj)
        return obj

    a = limix_mod._cached_predictor(("ckpt-a", "cfg", "cuda"), build)
    b = limix_mod._cached_predictor(("ckpt-b", "cfg", "cuda"), build)
    assert a is not b
    assert len(made) == 2
    # Only the newest is retained, so the old backbone can be collected.
    assert len(limix_mod._PREDICTOR_CACHE) == 1
    assert list(limix_mod._PREDICTOR_CACHE.values()) == [b]


def test_import_guard_names_the_side_env():
    """The failure mode is running in the 3.11 production env.

    The message must point at the side env rather than surfacing a bare
    ``ModuleNotFoundError: inference``.
    """
    with pytest.raises(ImportError) as exc:
        limix_mod._limix_api("/definitely/not/a/limix/checkout")
    msg = str(exc.value)
    assert "limix_env" in msg
    assert "3.12" in msg


def test_regressor_defaults_point_at_side_env():
    reg = limix_mod.LimiXYieldRegressor()
    assert reg.limix_root.endswith("LimiX")
    assert "limix" in reg.cache_dir
    assert reg.device == "auto"
    assert reg._predictor is None
