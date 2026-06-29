"""BEAST-based yield-anomaly detector.

Identifies years where reported yield jumps abnormally high above the
local trend and then snaps back — the classic "data error" or
"reporting anomaly" pattern (sudden one-time spike + reversion). BEAST
distinguishes such noise spikes (low change-point probability) from
genuine regime shifts (high change-point probability), so we can flag
the spikes without false-positives on real productivity jumps.

Three categories:
    * spike_revert         — large positive residual, low cp_prob, next
                              year reverts close to trend. HIGH confidence.
    * end_of_series_spike  — same as above but at the LAST year, so we
                              can't verify reversion. MEDIUM confidence.
                              The detector still flags it so analysts can
                              treat the latest-year datum cautiously.
    * spike_no_revert      — large residual but t+1 stays elevated. Could
                              be a regime shift BEAST didn't fully isolate.
                              LOW confidence; included for audit.

API:
    detect_spikes_one_series(years, yields, **thresholds) -> dict
    detect_spikes_batch(df, group_cols, year_col, target_col, **thresholds) -> pd.DataFrame
    plot_series_with_flags(beast_out, flags, out_path) -> None

Notes
-----
BEAST is invoked in trend-only mode (``season="none"``) — annual yield
data has no subseasonal component for BEAST to decompose. Series with
fewer than ``min_years`` finite years are skipped (BEAST inference is
unreliable on very short series).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class AnomalyThresholds:
    """All tunable thresholds in one place. Defaults are sensible for
    annual crop yield series with 20-30 years of data."""

    z_threshold: float = 2.0
    """Residual std-devs above trend to qualify as a spike candidate."""

    cp_threshold: float = 0.5
    """Maximum BEAST change-point probability at year t for the spike
    to count as noise (not a regime shift)."""

    revert_threshold: float = 1.0
    """Year t+1 must be within this many std-devs of trend to confirm
    revert (HIGH confidence spike_revert classification)."""

    min_years: int = 10
    """Skip series with fewer finite-yield years than this."""

    include_negative_spikes: bool = False
    """If True, also detect large NEGATIVE residuals (yield dips).
    User explicitly asked for spikes only — keep False by default."""

    mcmc_seed: int = 42
    """BEAST MCMC seed for reproducibility."""


def detect_spikes_one_series(
    years,
    yields,
    thresholds: Optional[AnomalyThresholds] = None,
    logger: Optional[logging.Logger] = None,
) -> dict:
    """Run BEAST + spike classifier on ONE time series.

    Args:
        years: 1-D array-like of integer years.
        yields: 1-D array-like of yield values (same length as years).
            NaN allowed; BEAST handles gaps.
        thresholds: detection thresholds (default AnomalyThresholds()).
        logger: optional logger for diagnostic info.

    Returns:
        dict with keys:
          ``years``         np.ndarray int — the contiguous year axis BEAST used
          ``yields``        np.ndarray float — y aligned to years, NaN for gaps
          ``trend``         np.ndarray float — BEAST posterior trend
          ``cp_prob``       np.ndarray float — BEAST cpOccPr at each year
          ``residual``      np.ndarray float — yields - trend (NaN where yield NaN)
          ``z_score``       np.ndarray float — residual / sqrt(sig2)
          ``sig2``          float — BEAST posterior noise variance
          ``flags``         list[dict] — one entry per detected spike with
                            year, yield, trend, z_score, cp_prob, next_z,
                            anomaly_type, confidence
          ``n_years_used``  int — finite-yield years that fed BEAST
          ``status``        str — "ok" | "too_short" | "all_nan" | "beast_failed"
    """
    if thresholds is None:
        thresholds = AnomalyThresholds()

    years = np.asarray(years, dtype=float)
    yields = np.asarray(yields, dtype=float)
    valid_input = (
        years.shape == yields.shape
        and years.ndim == 1
        and years.size > 0
    )
    if not valid_input:
        return _empty_result("bad_input")

    finite = np.isfinite(yields) & np.isfinite(years)
    n_finite = int(finite.sum())
    if n_finite == 0:
        return _empty_result("all_nan")
    if n_finite < thresholds.min_years:
        return _empty_result("too_short", n_years_used=n_finite)

    # Build a CONTIGUOUS annual series with NaN gaps — BEAST requires
    # evenly-spaced timesteps. Years in the middle that have no
    # observation become NaN; BEAST treats them as missing.
    y0 = int(years[finite].min())
    y1 = int(years[finite].max())
    n_steps = y1 - y0 + 1
    contiguous_years = np.arange(y0, y1 + 1, dtype=int)
    contiguous_yields = np.full(n_steps, np.nan, dtype=float)
    for yr, val in zip(years[finite].astype(int), yields[finite]):
        contiguous_yields[yr - y0] = float(val)

    try:
        import Rbeast as rb
    except ImportError:
        if logger is not None:
            logger.error("  Rbeast not installed; skipping anomaly detection.")
        return _empty_result("beast_unavailable")

    try:
        o = rb.beast(
            contiguous_yields,
            start=y0, deltat=1, season="none",
            mcmc_seed=thresholds.mcmc_seed,
            quiet=True, print_param=False,
            print_progress=False, print_warning=False,
        )
    except Exception as exc:  # noqa: BLE001
        if logger is not None:
            logger.warning(f"  BEAST failed: {exc}; skipping series.")
        return _empty_result("beast_failed", n_years_used=n_finite)

    trend = np.atleast_1d(np.asarray(o.trend.Y, dtype=float)).ravel()
    # cpOccPr — accumulated change-point occurrence probability per year.
    cp_prob = np.atleast_1d(np.asarray(o.trend.cpOccPr, dtype=float)).ravel()
    # BEAST's posterior noise variance (sigma squared). For trend-only
    # mode in pure-python Rbeast it lives at o.sig2; in some versions
    # it's o.sig2[0] (an array of 1). Handle both.
    sig2_raw = getattr(o, "sig2", np.nan)
    sig2 = float(np.atleast_1d(sig2_raw).ravel()[0]) if sig2_raw is not None else float("nan")

    # Robust noise scale via MAD (median absolute deviation) on the
    # detrended residuals — NOT the BEAST posterior variance and NOT
    # plain std. Why: past spikes (which ARE the anomalies we want to
    # detect) inflate variance-based sigma and push later-year spikes
    # below the z-threshold. The Mozambique-2022 case is exactly this:
    # historical spikes in 2010 raise sigma so that the genuine 2022
    # anomaly (1.7-2.0 t/ha vs ~0.9 baseline) registers only z~1.9,
    # below the default 2.0 cut. MAD-based sigma is robust — outlier
    # years don't inflate it.
    #
    # MAD->sigma scaling constant 1.4826 makes MAD a consistent
    # estimator of std for normally-distributed residuals.
    residuals_finite = (contiguous_yields - trend)
    residuals_finite = residuals_finite[np.isfinite(residuals_finite)]
    if residuals_finite.size < 3:
        return _empty_result("zero_variance", n_years_used=n_finite)
    median_resid = float(np.median(residuals_finite))
    mad = float(np.median(np.abs(residuals_finite - median_resid)))
    mad_sigma = 1.4826 * mad
    if mad_sigma <= 0:
        # MAD can be 0 when >half of residuals are identical (very
        # short series or constant trend). Fall back to std as last
        # resort.
        std_sigma = float(np.std(residuals_finite, ddof=1))
        if std_sigma <= 0:
            return _empty_result("zero_variance", n_years_used=n_finite)
        sigma = std_sigma
    else:
        sigma = mad_sigma
    sig2 = float(sigma * sigma)
    residual = contiguous_yields - trend
    with np.errstate(invalid="ignore"):
        z_score = residual / sigma

    # Spike classification.
    flags: list = []
    last_idx = n_steps - 1
    for t in range(n_steps):
        if not np.isfinite(z_score[t]):
            continue
        z = float(z_score[t])
        cp = float(cp_prob[t]) if np.isfinite(cp_prob[t]) else 0.0
        # Positive spikes (and optionally negative).
        is_positive_spike = z >= thresholds.z_threshold
        is_negative_spike = (
            thresholds.include_negative_spikes and z <= -thresholds.z_threshold
        )
        if not (is_positive_spike or is_negative_spike):
            continue
        # Spike candidate. Now check: is it a regime shift (high cp_prob)
        # or a noise spike (low cp_prob — what we want)?
        if cp >= thresholds.cp_threshold:
            # Likely a real regime shift; don't flag.
            continue

        # Classify based on the next finite year (scanning forward
        # through NaN gaps up to ``revert_lookahead`` years). A gap
        # between the spike and the next observation should NOT
        # automatically mean "end of series" — Cabo Delgado / Mozambique
        # maize 2010 has a real revert at 2012 even though 2011 is
        # missing. Only when we reach the actual end of the contiguous
        # series without finding a finite year do we tag as
        # ``end_of_series_spike``.
        revert_lookahead = 3
        next_z = float("nan")
        next_finite_idx = -1
        for k in range(1, revert_lookahead + 1):
            j = t + k
            if j > last_idx:
                break
            if np.isfinite(z_score[j]):
                next_z = float(z_score[j])
                next_finite_idx = j
                break

        if next_finite_idx < 0:
            # No finite observation within revert_lookahead years.
            # Either truly the end of series, or the trailing window
            # is all gaps — both qualify as "can't verify revert".
            anomaly_type = "end_of_series_spike"
            confidence = "medium"
        else:
            # Revert criterion: next year is AT OR BELOW the trend
            # (residual ≤ +revert_threshold·σ). Deep negative residuals
            # (next year fell well below trend) still count as a snap-
            # back from a positive spike — that's the physical pattern
            # we're after. Only when next_z stays STRICTLY ABOVE the
            # threshold do we call it "no revert" (= sustained
            # elevation = likely regime shift BEAST didn't isolate).
            if next_z <= thresholds.revert_threshold:
                anomaly_type = "spike_revert"
                confidence = "high"
            else:
                anomaly_type = "spike_no_revert"
                confidence = "low"

        flags.append({
            "year":          int(contiguous_years[t]),
            "yield_observed": float(contiguous_yields[t]),
            "trend_estimate": float(trend[t]),
            "residual":      float(residual[t]),
            "z_score":       z,
            "cp_prob":       cp,
            "next_year_z":   next_z,
            "anomaly_type":  anomaly_type,
            "confidence":    confidence,
        })

    return {
        "years":        contiguous_years,
        "yields":       contiguous_yields,
        "trend":        trend,
        "cp_prob":      cp_prob,
        "residual":     residual,
        "z_score":      z_score,
        "sig2":         sig2,
        "flags":        flags,
        "n_years_used": n_finite,
        "status":       "ok",
    }


def _empty_result(status: str, n_years_used: int = 0) -> dict:
    return {
        "years":        np.array([], dtype=int),
        "yields":       np.array([], dtype=float),
        "trend":        np.array([], dtype=float),
        "cp_prob":      np.array([], dtype=float),
        "residual":     np.array([], dtype=float),
        "z_score":      np.array([], dtype=float),
        "sig2":         float("nan"),
        "flags":        [],
        "n_years_used": n_years_used,
        "status":       status,
    }


def detect_spikes_batch(
    df: pd.DataFrame,
    group_cols: tuple,
    year_col: str,
    target_col: str,
    thresholds: Optional[AnomalyThresholds] = None,
    n_jobs: int = 1,
    logger: Optional[logging.Logger] = None,
    return_series_outputs: bool = False,
) -> pd.DataFrame:
    """Run the detector on every group in ``df``.

    Args:
        df: long-format DataFrame with one row per (group, year, value).
        group_cols: tuple of column names identifying a series, e.g.
            ``("country", "crop", "region", "season")``. Each unique
            combination of values across these columns becomes one
            BEAST run.
        year_col: name of the year column (int).
        target_col: name of the value column (yield).
        thresholds: detection thresholds.
        n_jobs: joblib parallelism. 1 = serial; -1 = all cores.
        logger: optional logger.
        return_series_outputs: when True, also return per-series BEAST
            output dicts (for plotting). Keyed by the group tuple.

    Returns:
        DataFrame with one row per FLAGGED year (groups with no flags
        contribute zero rows). Columns: ``*group_cols``, ``year``,
        ``yield_observed``, ``trend_estimate``, ``residual``,
        ``z_score``, ``cp_prob``, ``next_year_z``, ``anomaly_type``,
        ``confidence``, ``n_years_in_series``.

        When ``return_series_outputs=True``, returns ``(df, outputs)``
        where ``outputs`` is a dict[tuple, per-series result dict].
    """
    if thresholds is None:
        thresholds = AnomalyThresholds()

    if df.empty:
        empty = pd.DataFrame(columns=list(group_cols) + [
            "year", "yield_observed", "trend_estimate", "residual",
            "z_score", "cp_prob", "next_year_z", "anomaly_type",
            "confidence", "n_years_in_series",
        ])
        if return_series_outputs:
            return empty, {}
        return empty

    groups = list(df.groupby(list(group_cols), sort=True, dropna=False))

    def _one(key, sub):
        sub_sorted = sub.sort_values(year_col)
        years = sub_sorted[year_col].to_numpy()
        yields = sub_sorted[target_col].to_numpy()
        res = detect_spikes_one_series(
            years, yields, thresholds=thresholds, logger=None,
        )
        return key, res

    if n_jobs == 1:
        results = [_one(key, sub) for key, sub in groups]
    else:
        from joblib import Parallel, delayed
        results = Parallel(n_jobs=n_jobs, backend="loky")(
            delayed(_one)(key, sub) for key, sub in groups
        )

    rows = []
    outputs: dict = {}
    n_ok = 0
    n_too_short = 0
    n_failed = 0
    for key, res in results:
        if not isinstance(key, tuple):
            key = (key,)
        if return_series_outputs:
            outputs[key] = res
        status = res.get("status", "unknown")
        if status == "ok":
            n_ok += 1
        elif status == "too_short":
            n_too_short += 1
        elif status in ("beast_failed", "beast_unavailable", "zero_variance"):
            n_failed += 1
        for flag in res.get("flags", []):
            row = {col: val for col, val in zip(group_cols, key)}
            row.update({
                "year":              int(flag["year"]),
                "yield_observed":    flag["yield_observed"],
                "trend_estimate":    flag["trend_estimate"],
                "residual":          flag["residual"],
                "z_score":           flag["z_score"],
                "cp_prob":           flag["cp_prob"],
                "next_year_z":       flag["next_year_z"],
                "anomaly_type":      flag["anomaly_type"],
                "confidence":        flag["confidence"],
                "n_years_in_series": res.get("n_years_used", 0),
            })
            rows.append(row)

    if logger is not None:
        logger.info(
            f"  detect_spikes_batch: {n_ok} series OK, {n_too_short} skipped "
            f"(too_short), {n_failed} skipped (BEAST/variance issue); "
            f"{len(rows)} total flags."
        )

    out_df = (
        pd.DataFrame(rows)
        if rows
        else pd.DataFrame(columns=list(group_cols) + [
            "year", "yield_observed", "trend_estimate", "residual",
            "z_score", "cp_prob", "next_year_z", "anomaly_type",
            "confidence", "n_years_in_series",
        ])
    )
    if return_series_outputs:
        return out_df, outputs
    return out_df


def plot_series_with_flags(
    series_result: dict,
    title: str,
    out_path,
) -> None:
    """Two-panel diagnostic plot for a single series.

    Top panel: yield observations + BEAST trend overlay + flagged years
        highlighted with colored markers (red=spike_revert,
        orange=end_of_series_spike, gray=spike_no_revert).
    Bottom panel: cp_prob bars per year + threshold line.

    Args:
        series_result: output of detect_spikes_one_series.
        title: figure title.
        out_path: file path to save PNG.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    years = series_result["years"]
    if years.size == 0:
        return  # nothing to plot

    yields = series_result["yields"]
    trend = series_result["trend"]
    cp_prob = series_result["cp_prob"]
    flags = series_result["flags"]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9, 5.5), sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    ax1.plot(years, yields, "o-", color="#1f77b4", markersize=5,
             linewidth=1.2, label="observed", alpha=0.8)
    ax1.plot(years, trend, "-", color="#2ca02c", linewidth=2.0,
             label="BEAST trend", alpha=0.85)
    color_map = {
        "spike_revert":         "#d62728",
        "end_of_series_spike":  "#ff7f0e",
        "spike_no_revert":      "#7f7f7f",
    }
    for flag in flags:
        ax1.scatter([flag["year"]], [flag["yield_observed"]],
                    color=color_map.get(flag["anomaly_type"], "black"),
                    s=120, zorder=5, edgecolors="black", linewidths=1.0)
        ax1.annotate(
            f"{flag['anomaly_type']}\nz={flag['z_score']:.2f}",
            xy=(flag["year"], flag["yield_observed"]),
            xytext=(6, 8), textcoords="offset points",
            fontsize=8, color=color_map.get(flag["anomaly_type"], "black"),
        )
    ax1.set_ylabel("yield (t/ha)")
    ax1.set_title(title)
    ax1.legend(loc="best", fontsize=9)
    ax1.grid(True, alpha=0.3)

    ax2.bar(years, cp_prob, color="#8c564b", alpha=0.7, width=0.7)
    ax2.axhline(0.5, color="black", linewidth=0.6, linestyle="--",
                alpha=0.5, label="cp_threshold")
    ax2.set_ylabel("cp_prob")
    ax2.set_xlabel("year")
    ax2.set_ylim(0, 1.05)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
