"""
Content-addressed disk cache for feature selection.

Feature selection depends only on ``(X, y, method)`` — never on the ML model
that consumes the result. Every model in a run therefore recomputes an
identical selection for the same fold / stage / region: with catboost +
cubist + tabpfn configured, the same greedy search runs three times over the
same matrix. On county-scale runs feature selection is ~74% of a fold
(gOMP_high) so this is the single largest source of redundant compute.

Fold-model tasks execute in separate multiprocessing workers, so an
in-memory cache cannot be shared between models. The cache therefore lives
on disk (one small JSON per key, under the project's ``ml/cache`` tree).

Keying is *content-addressed*: the key is a hash of the training matrix, the
target vector and the method string. Anything that legitimately changes the
selection — fold year, stage, region group, detrending, region filters,
``use_cids``, an upstream CID regeneration — changes the data and therefore
the key. There is consequently no invalidation logic to get wrong and no way
to serve a stale hit for different data; a changed input is simply a miss.

Two deliberate consequences:

1. Stochastic selectors (BorutaShap, Genetic, ``multi``) return the *first*
   draw to every later caller instead of an independent draw. Within a fold
   this is desirable — all models are then compared on an identical feature
   set — but it does remove run-to-run selection variability.
2. Selectors that write per-region diagnostic artifacts do not rewrite them
   on a hit; the files from the computing call stand.

Every failure path (unhashable frame, unwritable directory, corrupt JSON)
degrades to "recompute normally" — the cache can never break a run.
"""

import hashlib
import json
import logging
import os
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Bump when the payload schema or the hashing recipe changes; old entries
# then simply miss instead of being misread.
CACHE_VERSION = "1"

CACHE_SUBDIR = Path("cache") / "feature_selection"

# Entries live under the project's ml/ tree and therefore outlive a run and a
# geocif upgrade. Folding a fingerprint of the selector *code* into the key
# means editing a selector invalidates old entries automatically, while an
# unrelated version bump keeps them usable.
_SELECTOR_SOURCES = ("feature_selection.py", "gomp.py")

_code_fingerprint = None


def selector_code_fingerprint():
    """
    Short digest of the feature-selection source files plus the library
    versions that drive selector behaviour. Computed once per process.
    """
    global _code_fingerprint
    if _code_fingerprint is not None:
        return _code_fingerprint

    h = hashlib.sha256()
    here = Path(__file__).resolve().parent
    for name in _SELECTOR_SOURCES:
        try:
            h.update(f"{name}:".encode())
            h.update((here / name).read_bytes())
        except OSError:
            # Source not readable (zipped/frozen install) — fall back to the
            # package version so an upgrade is still a miss.
            try:
                from geocif import __version__ as geocif_version
            except Exception:
                geocif_version = "unknown"
            h.update(f"{name}:version={geocif_version}".encode())

    for module_name in ("numpy", "pandas", "sklearn"):
        try:
            module = __import__(module_name)
            h.update(f"{module_name}={getattr(module, '__version__', '?')}".encode())
        except Exception:
            h.update(f"{module_name}=unimportable".encode())

    _code_fingerprint = h.hexdigest()[:16]
    return _code_fingerprint


def cache_dir_for(dir_ml):
    """
    Standard cache location for a project.

    Args:
        dir_ml: project ``ml`` directory (``self.dir_ml``)

    Returns:
        Path to the feature-selection cache directory
    """
    return Path(dir_ml) / CACHE_SUBDIR


def compute_key(X, y, method, extra=None):
    """
    Content hash of the feature-selection inputs.

    Args:
        X: pd.DataFrame of candidate features (post string-categorical drop)
        y: target vector (Series or array-like)
        method: feature-selection method name
        extra: optional dict of additional scalars to fold into the key

    Returns:
        str hex digest, or None if the inputs could not be hashed (caller
        then runs uncached)
    """
    try:
        h = hashlib.sha256()
        h.update(f"v={CACHE_VERSION}".encode())
        # pandas' hash is stable within a version but not guaranteed across
        # them — folding the version in turns an upgrade into a miss rather
        # than a wrong hit.
        h.update(f"pandas={pd.__version__}".encode())
        # Selector source + library versions: editing a selector (e.g. the
        # gOMP caps) must not serve results from the previous behaviour.
        h.update(f"code={selector_code_fingerprint()}".encode())
        h.update(f"method={method}".encode())

        if extra:
            for k in sorted(extra):
                h.update(f"{k}={extra[k]}".encode())

        # Column names are NOT part of pandas' frame hash — add them
        # explicitly so a renamed/reordered feature set is a different key.
        columns = [str(c) for c in X.columns]
        h.update(f"shape={X.shape[0]}x{X.shape[1]}".encode())
        h.update("\x1f".join(columns).encode())

        h.update(pd.util.hash_pandas_object(X, index=False).values.tobytes())

        y_series = y if isinstance(y, pd.Series) else pd.Series(np.asarray(y).ravel())
        h.update(pd.util.hash_pandas_object(y_series, index=False).values.tobytes())

        return h.hexdigest()
    except Exception as e:
        logger.warning(f"[fs_cache] could not hash selection inputs ({e}); running uncached")
        return None


def _path_for(cache_dir, key):
    """Shard by the first two hex characters to keep directories small."""
    return Path(cache_dir) / key[:2] / f"{key}.json"


def load(cache_dir, key, log=None):
    """
    Read a cached selection.

    Returns:
        list[str] of selected features on a hit (possibly empty — an empty
        selection is a legitimate cached result), or None on a miss / any
        read problem.
    """
    log = log or logger
    if not cache_dir or not key:
        return None

    path = _path_for(cache_dir, key)
    try:
        if not path.is_file():
            return None
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception as e:
        log.warning(f"[fs_cache] unreadable cache entry {path} ({e}); recomputing")
        return None

    features = payload.get("selected_features") if isinstance(payload, dict) else None
    if not isinstance(features, list) or not all(isinstance(c, str) for c in features):
        log.warning(f"[fs_cache] malformed cache entry {path}; recomputing")
        return None

    return features


def store(cache_dir, key, features, meta=None, log=None):
    """
    Write a selection atomically (temp file + rename), so a concurrent
    reader never observes a partial file and two workers computing the same
    key simply write identical content.

    Returns:
        True if the entry was written
    """
    log = log or logger
    if not cache_dir or not key:
        return False

    path = _path_for(cache_dir, key)
    tmp = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "key": key,
            "selected_features": list(features),
            "meta": meta or {},
        }
        tmp = path.parent / f".{path.name}.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        os.replace(tmp, path)
        return True
    except Exception as e:
        log.warning(f"[fs_cache] could not write cache entry {path} ({e}); continuing uncached")
        try:
            if tmp is not None and Path(tmp).exists():
                os.remove(tmp)
        except OSError:
            pass
        return False


def cached_select(X, y, method, cache_dir, compute_fn, log=None, extra=None, meta=None,
                  should_cache=None):
    """
    Return the feature selection for ``(X, y, method)``, computing it only if
    it is not already on disk.

    Args:
        X: candidate feature frame
        y: target vector
        method: feature-selection method name
        cache_dir: cache directory, or None to disable caching
        compute_fn: zero-arg callable returning list[str] of selected features
        log: logger to use
        extra: optional dict folded into the key
        meta: optional dict stored alongside the entry (diagnostics only —
            never read back for correctness)
        should_cache: optional zero-arg callable evaluated after compute_fn.
            Returning False keeps the result for this call but does not
            persist it. Use it whenever the computation may have silently
            degraded (e.g. a ``multi`` sub-selector died under memory
            pressure): because the key is content-addressed, a bad entry
            would otherwise be re-served to every later model AND to every
            re-run of the same experiment, which re-running cannot clear.

    Returns:
        (selected_features, was_cache_hit)
    """
    log = log or logger
    key = compute_key(X, y, method, extra=extra) if cache_dir else None

    if key:
        cached = load(cache_dir, key, log=log)
        if cached is not None:
            # Defense against a hand-edited entry or (astronomically
            # unlikely) collision: every cached name must exist in X.
            known = set(X.columns)
            missing = [c for c in cached if c not in known]
            if missing:
                log.warning(
                    f"[fs_cache] cached selection {key[:12]} references "
                    f"{len(missing)} unknown column(s) e.g. {missing[:3]}; recomputing"
                )
            else:
                log.info(
                    f"[fs_cache] HIT {key[:12]} — reusing {len(cached)} features "
                    f"(method={method}), skipping recompute"
                )
                return cached, True

    start = time.time()
    features = list(compute_fn() or [])
    elapsed = time.time() - start

    if key and should_cache is not None and not should_cache():
        log.warning(
            f"[fs_cache] not caching {key[:12]} — the selection completed but "
            f"was degraded (method={method}); using it for this model only so "
            f"a transient failure cannot poison later models or re-runs"
        )
        return features, False

    if key:
        entry_meta = dict(meta or {})
        entry_meta.update(
            {
                "method": method,
                "n_rows": int(X.shape[0]),
                "n_candidate_features": int(X.shape[1]),
                "n_selected": len(features),
                "compute_seconds": round(elapsed, 2),
                "code_fingerprint": selector_code_fingerprint(),
            }
        )
        store(cache_dir, key, features, meta=entry_meta, log=log)
        log.info(
            f"[fs_cache] MISS {key[:12]} — computed {len(features)} features "
            f"in {elapsed:.1f}s (method={method}), cached for other models"
        )

    return features, False
