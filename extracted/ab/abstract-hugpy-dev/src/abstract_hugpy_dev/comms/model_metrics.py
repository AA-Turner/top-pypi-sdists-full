"""MODEL METRICS (2026-08-28) — measured load/serve timings per (model,
variant, worker card), logged as a side effect of every real load and call.
Measure, don't bench: rows exist only because work actually happened.

Operator concept: groups rank their members, but rank alone can't answer
"which member/worker pair answers FASTEST right now?" — that needs

    total_time_to_output = time_to_download + time_to_evict_to_fit
                         + time_to_upload + time_to_output

where upload time and tok/s differ per variant (split | moe | gpu_only_4bit
| ram_only_4bit), per card, and hot vs cold. This store holds the measured
terms as EMAs; the decision-time terms (download presence, evict-to-fit dry
run) are the scheduler's, passed into ``estimate_total_time``. Stage
transitions that displace a model the next stage needs again charge the
displaced model's hot re-upload too — pass it as ``displaced_reupload_s``.
"""
from __future__ import annotations

import os
import sqlite3
import threading
import time
from typing import Any, Dict, Optional

from .shared import retry_on_emfile

VARIANTS = ("split", "moe", "gpu_only_4bit", "ram_only_4bit")
TEMPERATURES = ("loaded", "unloaded")   # LOADED-at-pick (STATE-MODEL.md #3); never "hot"/"cold" (that named a VRAM condition)

# EMA weight for a new sample. High enough to track a card whose behavior
# drifts (thermals, contention), low enough that one anomalous load doesn't
# repaint the picture.
EMA_ALPHA = float(os.environ.get("HUGPY_MODEL_METRICS_EMA_ALPHA", "0.3") or 0.3)


def _ema(prev: Optional[float], sample: float, n_prev: int) -> float:
    # First sample IS the estimate; after that, standard exponential blend.
    if prev is None or n_prev <= 0:
        return float(sample)
    return (1.0 - EMA_ALPHA) * float(prev) + EMA_ALPHA * float(sample)


def derive_variant(n_gpu_layers: Any, total_layers: Optional[int] = None,
                   *, moe_capable: bool = False) -> Optional[str]:
    """Derive the VARIANTS member from what the serving contract actually did,
    so the enum can't drift from reality — callers should never pass a variant
    string by hand.

    Inputs mirror the serving contract's own vocabulary: ``n_gpu_layers`` as
    llama.cpp uses it (-1 = all layers on GPU, 0 or the chaos sweep's "off" =
    none), ``total_layers`` when known, ``moe_capable`` from model_physical's
    capability pair. MoE is checked first (MoE fit math is its own regime —
    expert bytes are mmap-eligible, dense partial math doesn't apply). The
    "_4bit" in the gpu/ram-only names is the operator's deployment vocabulary
    (those tiers run quantized on this fleet), not re-derived here. Returns
    None when the split is unknowable — an unknown variant is unrecorded, not
    guessed.
    """
    if moe_capable:
        return "moe"
    if n_gpu_layers in ("off", 0):
        return "ram_only_4bit"
    if n_gpu_layers is None:
        return None
    try:
        n = int(n_gpu_layers)
    except (TypeError, ValueError):
        return None
    if n == -1 or (total_layers is not None and n >= int(total_layers)):
        return "gpu_only_4bit"
    if total_layers is None:
        # A positive layer count with no total is ambiguous (could be all of
        # them) — unrecorded beats misfiled.
        return None
    return "split"


def default_db_path() -> str:
    env = (os.environ.get("HUGPY_MODEL_METRICS_DB") or "").strip()
    if env:
        return env
    base = (os.environ.get("PROJECTS_HOME") or "").strip()
    if not base:
        try:
            from abstract_hugpy_dev.imports.src.constants.constants import (
                PROJECTS_HOME as _PH)
            base = str(_PH)
        except Exception:  # noqa: BLE001 — degrade to a per-user durable file
            base = os.path.expanduser("~/.hugpy")
    return os.path.join(base, "model_metrics.db")


class ModelMetricsStore:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path or default_db_path()
        self._disabled = False
        self._init_lock = threading.Lock()
        self._initialized = False

    # -- plumbing ------------------------------------------------------------
    def _connect(self) -> sqlite3.Connection:
        # Retry the store-open past the restart-burst EMFILE (see
        # comms.shared.retry_on_emfile) before running the handle-local PRAGMAs.
        conn = retry_on_emfile(lambda: sqlite3.connect(self.path, timeout=2.0))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=2000")
        return conn

    def _ensure(self) -> bool:
        if self._disabled:
            return False
        if self._initialized:
            return True
        with self._init_lock:
            if self._initialized:
                return True
            try:
                conn = self._connect()
                try:
                    conn.execute(
                        "CREATE TABLE IF NOT EXISTS load_metrics ("
                        " model TEXT NOT NULL,"
                        " variant TEXT NOT NULL,"
                        " worker_card TEXT NOT NULL,"
                        " temperature TEXT NOT NULL,"
                        " upload_time_s REAL,"
                        " tok_per_s REAL,"
                        " n_samples INTEGER NOT NULL DEFAULT 0,"
                        " updated_at REAL NOT NULL,"
                        " PRIMARY KEY (model, variant, worker_card,"
                        "              temperature))")
                    # Canon migration (STATE-MODEL.md #3): legacy temperature
                    # values hot/cold named a VRAM condition "hot" — rebucket
                    # to loaded/unloaded (keyed on LOADED-at-pick). Idempotent.
                    conn.execute("UPDATE OR IGNORE load_metrics"
                                 " SET temperature='loaded' WHERE temperature='hot'")
                    conn.execute("UPDATE OR IGNORE load_metrics"
                                 " SET temperature='unloaded' WHERE temperature='cold'")
                    conn.execute(
                        "CREATE TABLE IF NOT EXISTS call_metrics ("
                        " model TEXT PRIMARY KEY,"
                        " avg_tok_output_per_call REAL,"
                        " n_calls INTEGER NOT NULL DEFAULT 0,"
                        " updated_at REAL NOT NULL)")
                    conn.commit()
                finally:
                    conn.close()
                self._initialized = True
                return True
            except Exception:  # noqa: BLE001 — metrics must never break serving
                self._disabled = True
                return False

    # -- writes --------------------------------------------------------------
    def record_load(self, model: str, variant: str, worker_card: str,
                    temperature: str, *,
                    upload_time_s: Optional[float] = None,
                    tok_per_s: Optional[float] = None) -> bool:
        """Fold one real load/serve observation into the EMAs.

        Either measurement may be absent (a load that never generated has no
        tok/s yet); the absent one keeps its previous estimate.
        """
        if variant not in VARIANTS or temperature not in TEMPERATURES:
            return False
        if not (model or "").strip() or not (worker_card or "").strip():
            return False
        if not self._ensure():
            return False
        try:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT upload_time_s, tok_per_s, n_samples"
                    " FROM load_metrics WHERE model=? AND variant=?"
                    " AND worker_card=? AND temperature=?",
                    (model, variant, worker_card, temperature)).fetchone()
                prev_up, prev_tok, n = row if row else (None, None, 0)
                new_up = (_ema(prev_up, upload_time_s, n)
                          if upload_time_s is not None else prev_up)
                new_tok = (_ema(prev_tok, tok_per_s, n)
                           if tok_per_s is not None else prev_tok)
                conn.execute(
                    "INSERT INTO load_metrics"
                    " (model, variant, worker_card, temperature,"
                    "  upload_time_s, tok_per_s, n_samples, updated_at)"
                    " VALUES (?,?,?,?,?,?,?,?)"
                    " ON CONFLICT(model, variant, worker_card, temperature)"
                    " DO UPDATE SET upload_time_s=excluded.upload_time_s,"
                    "  tok_per_s=excluded.tok_per_s,"
                    "  n_samples=excluded.n_samples,"
                    "  updated_at=excluded.updated_at",
                    (model, variant, worker_card, temperature,
                     new_up, new_tok, n + 1, time.time()))
                conn.commit()
            finally:
                conn.close()
            return True
        except Exception:  # noqa: BLE001
            return False

    def record_call(self, model: str, tok_output: float) -> bool:
        if not (model or "").strip():
            return False
        if not self._ensure():
            return False
        try:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT avg_tok_output_per_call, n_calls"
                    " FROM call_metrics WHERE model=?", (model,)).fetchone()
                prev, n = row if row else (None, 0)
                conn.execute(
                    "INSERT INTO call_metrics"
                    " (model, avg_tok_output_per_call, n_calls, updated_at)"
                    " VALUES (?,?,?,?)"
                    " ON CONFLICT(model) DO UPDATE SET"
                    "  avg_tok_output_per_call=excluded.avg_tok_output_per_call,"
                    "  n_calls=excluded.n_calls, updated_at=excluded.updated_at",
                    (model, _ema(prev, tok_output, n), n + 1, time.time()))
                conn.commit()
            finally:
                conn.close()
            return True
        except Exception:  # noqa: BLE001
            return False

    # -- reads ---------------------------------------------------------------
    def get_load(self, model: str, variant: str, worker_card: str,
                 temperature: str) -> Optional[Dict[str, Any]]:
        if not self._ensure():
            return None
        try:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT upload_time_s, tok_per_s, n_samples, updated_at"
                    " FROM load_metrics WHERE model=? AND variant=?"
                    " AND worker_card=? AND temperature=?",
                    (model, variant, worker_card, temperature)).fetchone()
            finally:
                conn.close()
        except Exception:  # noqa: BLE001
            return None
        if not row:
            return None
        return {"upload_time_s": row[0], "tok_per_s": row[1],
                "n_samples": row[2], "updated_at": row[3]}

    def get_call(self, model: str) -> Optional[Dict[str, Any]]:
        if not self._ensure():
            return None
        try:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT avg_tok_output_per_call, n_calls, updated_at"
                    " FROM call_metrics WHERE model=?", (model,)).fetchone()
            finally:
                conn.close()
        except Exception:  # noqa: BLE001
            return None
        if not row:
            return None
        return {"avg_tok_output_per_call": row[0], "n_calls": row[1],
                "updated_at": row[2]}

    # -- scoring -------------------------------------------------------------
    def estimate_total_time(self, model: str, variant: str, worker_card: str,
                            *, temperature: str = "loaded",
                            time_to_download_s: float = 0.0,
                            time_to_evict_s: float = 0.0,
                            displaced_reupload_s: float = 0.0,
                            ) -> Optional[float]:
        """Estimate total_time_to_output for one (member, worker) pair.

        The measured terms come from this store; the decision-time terms are
        the caller's: download is 0 when weights are cached on the worker's
        host, evict comes from the fit-check dry run — which MUST use the
        accounting of the loader that will actually run the member (the slot
        guard over-estimates GGUFs that llama-server's partial offload fits) —
        and ``displaced_reupload_s`` is the hot re-upload of a model this
        transition displaces but the next stage needs again.

        Returns None when the pair has no measurements yet — an unmeasured
        pair is unranked, not free.
        """
        load = self.get_load(model, variant, worker_card, temperature)
        call = self.get_call(model)
        if not load or load["upload_time_s"] is None or not load["tok_per_s"]:
            return None
        if not call or call["avg_tok_output_per_call"] is None:
            return None
        return (float(time_to_download_s) + float(time_to_evict_s)
                + float(load["upload_time_s"])
                + float(call["avg_tok_output_per_call"]) / float(load["tok_per_s"])
                + float(displaced_reupload_s))


model_metrics_store = ModelMetricsStore()


def record_loads_from_calibration(worker_name, samples) -> int:
    """The upload_time_s producer — the cold-load half ``_record_model_metrics``
    deliberately leaves to the load path. Folds worker-shipped calibration
    samples that carry a measured ``load_seconds`` into the cold-load EMA.

    The calibration wire is the SINGLE producer (the k119 follow-up's open
    question, resolved as: merge, don't duplicate — calibration_samples already
    had the ``load_seconds`` column and the heartbeat wire; a second reporter
    would just drift). ``worker_name`` maps to the card exactly as the
    completion seam does (``"<name>:0"``); variant is derived, never passed by
    hand. Skips, never guesses: no load_seconds, unknown variant, or a failed
    load leave the EMA untouched. Returns how many samples were folded.
    Fail-open per telemetry doctrine — this must never fail a heartbeat."""
    if not worker_name or not samples:
        return 0
    card = f"{worker_name}:0"
    folded = 0
    for s in samples:
        try:
            if not isinstance(s, dict) or not s.get("ok"):
                continue
            load_s = s.get("load_seconds")
            if not isinstance(load_s, (int, float)) or load_s <= 0:
                continue
            variant = derive_variant(
                s.get("n_gpu_layers"), s.get("total_layers"),
                moe_capable=bool(s.get("moe_capable")))
            if variant is None:
                continue
            if model_metrics_store.record_load(
                    str(s.get("model_key") or ""), variant, card, "unloaded",
                    upload_time_s=float(load_s)):
                folded += 1
        except Exception:  # noqa: BLE001 — one bad sample must not drop the rest
            continue
    return folded
