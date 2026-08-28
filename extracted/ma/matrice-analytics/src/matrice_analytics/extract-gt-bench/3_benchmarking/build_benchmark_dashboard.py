"""Build a dark-mode HTML dashboard from GT + prediction detection JSONs.

Aggregates multi-class benchmark metrics (same semantics as eval_without_volume)
and writes a standalone HTML file with Chart.js charts.

Usage::

    python build_benchmark_dashboard.py
    python build_benchmark_dashboard.py --gt path/to/gt.json --pred path/to/pred.json --out report.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_APPS_VC = _HERE.parent / "apps" / "vehicle-counting"
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from detection_loader import iter_frames, load_detection_json, match_frame_fp_fn  # noqa: E402
from eval_without_volume import (  # noqa: E402
    AGG_INTERVAL_SEC,
    _avg_accuracy,
    _frame_unique_ids,
    _pair_accuracy,
)

MAX_SERIES_POINTS = 500


def _f1_score(precision: float | None, recall: float | None) -> float | None:
    """Harmonic mean of precision and recall; ``None`` when undefined."""
    if precision is None or recall is None:
        return None
    if precision + recall <= 0:
        return 0.0 if (precision > 0 or recall > 0) else None
    return 2.0 * precision * recall / (precision + recall)


def _metric_note(
    cls: str,
    *,
    gt_vu: int,
    pred_vu: int,
    video_acc: float,
    minute_acc: float,
    tp: int,
    fp: int,
    fn: int,
    prec: float | None,
) -> str | None:
    """Short human-readable hint when a score is 0 or N/A (not missing data)."""
    parts: list[str] = []
    if video_acc == 0.0 and gt_vu != pred_vu:
        parts.append(f"video unique: GT {gt_vu} vs pred {pred_vu} track IDs")
    if minute_acc == 0.0 and video_acc == 0.0 and gt_vu != pred_vu:
        parts.append("minute windows penalized when pred unique >> GT")
    if prec is None and tp == 0 and fp == 0:
        parts.append("precision N/A (no TP/FP at IoU threshold)")
    if prec is not None and prec < 0.01 and fp > 0:
        parts.append(f"precision ~0% ({fp} FP, {tp} TP)")
    if cls == "bus" and fp > 100 and fn < 10:
        parts.append("many bus FPs vs almost no GT bus boxes")
    return "; ".join(parts) if parts else None


def _downsample(xs: list, ys: list[list], max_pts: int = MAX_SERIES_POINTS) -> tuple[list, list[list]]:
    n = len(xs)
    if n <= max_pts:
        return xs, ys
    stride = max(1, n // max_pts)
    idx = list(range(0, n, stride))
    if idx[-1] != n - 1:
        idx.append(n - 1)
    return [xs[i] for i in idx], [[row[i] for i in idx] for row in ys]


def _error_histogram(errors: list[int], bin_width: int = 1, cap: int = 10) -> dict[str, list]:
    """Bucket signed count errors (pred - gt) for histogram display."""
    bins: list[str] = []
    counts: list[int] = []
    for b in range(-cap, cap + 1):
        if b == cap:
            label = f">{cap}"
            c = sum(1 for e in errors if e > cap)
        elif b == -cap:
            label = f"<{-cap}"
            c = sum(1 for e in errors if e < -cap)
        else:
            label = str(b)
            c = sum(1 for e in errors if e == b)
        bins.append(label)
        counts.append(c)
    return {"labels": bins, "counts": counts}


def _class_names_ordered(gt_json: dict[str, Any]) -> list[str]:
    raw = gt_json.get("class_names") or {}
    if not raw:
        return []
    return [str(raw[k]) for k in sorted(raw.keys(), key=lambda x: int(x))]


def aggregate_all_classes(
    gt_path: Path,
    pred_path: Path,
    *,
    class_names: list[str],
    iou_threshold: float = 0.5,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Single-pass multi-class aggregation for dashboard series + summaries."""
    gt_json = load_detection_json(gt_path)
    pred_json = load_detection_json(pred_path)

    fps = float(gt_json.get("fps") or pred_json.get("fps") or 30.0)
    frames_per_window = max(1, int(round(AGG_INTERVAL_SEC * fps)))

    gt_all = dict(iter_frames(gt_json, target_classes=None))
    pred_all = dict(
        iter_frames(
            pred_json,
            target_classes=None,
            confidence_threshold=confidence_threshold,
        )
    )
    all_frame_ids = sorted(set(gt_all) | set(pred_all))

    summaries: dict[str, dict[str, Any]] = {}
    series: dict[str, dict[str, Any]] = {}
    table_rows: list[dict[str, Any]] = []

    for cls in class_names:
        per_frame_rows: list[dict[str, Any]] = []
        minute_rows: list[dict[str, Any]] = []
        window_gt_ids: set[Any] = set()
        window_pred_ids: set[Any] = set()
        video_gt_ids: set[Any] = set()
        video_pred_ids: set[Any] = set()
        total_tp = total_fp = total_fn = 0
        gt_total_boxes = pred_total_boxes = 0
        exact_match_frames = 0
        window_start_frame: int | None = None

        frame_ids: list[int] = []
        t_secs: list[float] = []
        gt_counts: list[int] = []
        pred_counts: list[int] = []
        errors: list[int] = []
        minute_t: list[float] = []
        minute_gt_u: list[int] = []
        minute_pred_u: list[int] = []

        for frame_id in all_frame_ids:
            gt_dets = [d for d in gt_all.get(frame_id, []) if d.get("category") == cls]
            pred_dets = [d for d in pred_all.get(frame_id, []) if d.get("category") == cls]

            gt_count = len(gt_dets)
            pred_count = len(pred_dets)
            gt_total_boxes += gt_count
            pred_total_boxes += pred_count

            tp, fp, fn = match_frame_fp_fn(gt_dets, pred_dets, iou_threshold=iou_threshold)
            total_tp += tp
            total_fp += fp
            total_fn += fn

            if gt_count == pred_count:
                exact_match_frames += 1

            per_frame_rows.append(
                {"gt_count": gt_count, "pred_count": pred_count}
            )
            frame_ids.append(frame_id)
            t_secs.append(frame_id / fps if fps > 0 else float(frame_id))
            gt_counts.append(gt_count)
            pred_counts.append(pred_count)
            errors.append(pred_count - gt_count)

            gt_ids = _frame_unique_ids(gt_dets)
            pred_ids = _frame_unique_ids(pred_dets)
            window_gt_ids |= gt_ids
            window_pred_ids |= pred_ids
            video_gt_ids |= gt_ids
            video_pred_ids |= pred_ids

            if window_start_frame is None:
                window_start_frame = frame_id
            if frame_id - window_start_frame + 1 >= frames_per_window:
                minute_rows.append((len(window_gt_ids), len(window_pred_ids)))
                minute_t.append(frame_id / fps if fps > 0 else float(frame_id))
                minute_gt_u.append(len(window_gt_ids))
                minute_pred_u.append(len(window_pred_ids))
                window_gt_ids = set()
                window_pred_ids = set()
                window_start_frame = None

        if window_gt_ids or window_pred_ids:
            minute_rows.append((len(window_gt_ids), len(window_pred_ids)))
            end_f = all_frame_ids[-1] if all_frame_ids else 0
            minute_t.append(end_f / fps if fps > 0 else float(end_f))
            minute_gt_u.append(len(window_gt_ids))
            minute_pred_u.append(len(window_pred_ids))

        n_frames = len(all_frame_ids) or 1
        per_frame_acc = _avg_accuracy(
            [(r["gt_count"], r["pred_count"]) for r in per_frame_rows]
        )
        minute_acc = _avg_accuracy(minute_rows) if minute_rows else 0.0
        video_acc = _pair_accuracy(len(video_gt_ids), len(video_pred_ids))

        prec = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else None
        rec = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else None
        f1 = _f1_score(prec, rec)

        gt_vu = len(video_gt_ids)
        pred_vu = len(video_pred_ids)
        summaries[cls] = {
            "per_frame_count_accuracy": per_frame_acc,
            "minute_unique_count_accuracy": minute_acc,
            "video_unique_count_accuracy": video_acc,
            "fp": total_fp,
            "fn": total_fn,
            "tp": total_tp,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "gt_total_detections": gt_total_boxes,
            "pred_total_detections": pred_total_boxes,
            "exact_match_fraction": exact_match_frames / n_frames,
            "gt_video_unique": gt_vu,
            "pred_video_unique": pred_vu,
            "note": _metric_note(
                cls,
                gt_vu=gt_vu,
                pred_vu=pred_vu,
                video_acc=video_acc,
                minute_acc=minute_acc,
                tp=total_tp,
                fp=total_fp,
                fn=total_fn,
                prec=prec,
            ),
        }

        ds_x, ds_ys = _downsample(t_secs, [gt_counts, pred_counts])
        scatter_x, scatter_ys = _downsample(gt_counts, [pred_counts])

        series[cls] = {
            "t_sec": ds_x,
            "gt_count": ds_ys[0],
            "pred_count": ds_ys[1],
            "scatter_gt": scatter_x,
            "scatter_pred": scatter_ys[0],
            "minute_t_sec": minute_t,
            "minute_gt_unique": minute_gt_u,
            "minute_pred_unique": minute_pred_u,
            "error_hist": _error_histogram(errors),
        }

        table_rows.append({"class": cls, **summaries[cls]})

    return {
        "fps": fps,
        "frame_count": len(all_frame_ids),
        "summaries": summaries,
        "series": series,
        "table_rows": table_rows,
    }


def _macro_averages(summaries: dict[str, dict[str, Any]]) -> dict[str, float]:
    if not summaries:
        return {}
    keys = (
        "per_frame_count_accuracy",
        "minute_unique_count_accuracy",
        "video_unique_count_accuracy",
    )
    out: dict[str, float] = {}
    for k in keys:
        out[f"macro_{k}"] = sum(s[k] for s in summaries.values()) / len(summaries)
    return out


def _weighted_averages(summaries: dict[str, dict[str, Any]]) -> dict[str, float]:
    total = sum(s.get("gt_total_detections", 0) for s in summaries.values())
    if total <= 0:
        return {}
    keys = (
        "per_frame_count_accuracy",
        "minute_unique_count_accuracy",
        "video_unique_count_accuracy",
    )
    out: dict[str, float] = {}
    for k in keys:
        out[f"weighted_{k}"] = (
            sum(s[k] * s.get("gt_total_detections", 0) for s in summaries.values()) / total
        )
    return out


def load_or_build_summaries(
    gt_path: Path,
    pred_path: Path,
    bench_path: Path | None,
    *,
    class_names: list[str],
    iou_threshold: float,
    confidence_threshold: float | None,
    agg: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Prefer freshly computed summaries; merge extended fields from bench.json when present."""
    merged = dict(agg["summaries"])
    if not (bench_path and bench_path.is_file()):
        return merged

    bench = json.loads(bench_path.read_text(encoding="utf-8"))
    if abs(float(bench.get("iou_threshold", -1)) - iou_threshold) > 1e-6:
        return merged
    if not bench.get("classes"):
        return merged

    metric_keys = (
        "per_frame_count_accuracy",
        "minute_unique_count_accuracy",
        "video_unique_count_accuracy",
        "fp",
        "fn",
        "tp",
        "precision",
        "recall",
        "f1",
        "gt_video_unique",
        "pred_video_unique",
        "gt_total_detections",
        "pred_total_detections",
        "exact_match_fraction",
    )
    for cls, row in bench["classes"].items():
        if cls not in merged:
            merged[cls] = dict(row)
            continue
        for k in metric_keys:
            if k in row and row[k] is not None:
                merged[cls][k] = row[k]
    return merged


def build_dashboard_data(
    gt_path: Path,
    pred_path: Path,
    bench_path: Path | None,
    *,
    iou_threshold: float = 0.5,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    gt_json = load_detection_json(gt_path)
    class_names = _class_names_ordered(gt_json)
    if not class_names:
        class_names = sorted(
            {d.get("category") for frames in gt_json.get("frames", {}).values() for d in frames if d}
        )

    agg = aggregate_all_classes(
        gt_path,
        pred_path,
        class_names=class_names,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold,
    )

    summaries = load_or_build_summaries(
        gt_path,
        pred_path,
        bench_path,
        class_names=class_names,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold,
        agg=agg,
    )

    fps = agg["fps"]
    n_frames = agg["frame_count"]
    default_class = "car" if "car" in class_names else (class_names[0] if class_names else "")

    return {
        "meta": {
            "evaluator": "eval_without_volume",
            "gt_json": str(gt_path.resolve()),
            "pred_json": str(pred_path.resolve()),
            "iou_threshold": iou_threshold,
            "confidence_threshold": confidence_threshold,
            "fps": fps,
            "frame_count": n_frames,
            "duration_sec": n_frames / fps if fps > 0 else 0,
            "width": int(gt_json.get("width", 0)),
            "height": int(gt_json.get("height", 0)),
        },
        "classes": class_names,
        "default_class": default_class,
        "summaries": summaries,
        "macro": _macro_averages(summaries),
        "weighted": _weighted_averages(summaries),
        "series": agg["series"],
        "table_rows": [
            {**row, **summaries.get(row["class"], {})} for row in agg["table_rows"]
        ],
    }


def _html_template() -> str:
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Benchmark Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg: #0f1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #8b949e;
      --accent-gt: #58a6ff;
      --accent-pred: #3fb950;
      --accent-warn: #d29922;
      --accent-bad: #f85149;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }
    header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid var(--border);
      background: var(--surface);
    }
    header h1 { margin: 0 0 0.25rem; font-size: 1.35rem; font-weight: 600; }
    header p { margin: 0; color: var(--muted); font-size: 0.85rem; }
    .kpis {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 0.75rem;
      padding: 1rem 1.5rem;
    }
    .kpi {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.75rem 1rem;
    }
    .kpi label { display: block; font-size: 0.7rem; text-transform: uppercase; color: var(--muted); letter-spacing: 0.04em; }
    .kpi span { font-size: 1.25rem; font-weight: 600; }
    main { padding: 0 1.5rem 2rem; }
    section { margin-top: 1.5rem; }
    section h2 {
      font-size: 1rem;
      font-weight: 600;
      margin: 0 0 0.75rem;
      color: var(--text);
    }
    .chart-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 1rem;
    }
    .chart-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem;
    }
    .chart-card.wide { grid-column: 1 / -1; }
    .chart-wrap { position: relative; height: 280px; }
    .chart-wrap.tall { height: 320px; }
    .controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
    }
    .controls label { color: var(--muted); font-size: 0.85rem; }
    select {
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.35rem 0.6rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
    }
    th, td {
      border: 1px solid var(--border);
      padding: 0.45rem 0.6rem;
      text-align: right;
    }
    th { background: #21262d; color: var(--muted); font-weight: 500; }
    th:first-child, td:first-child { text-align: left; }
    tr:hover td { background: #1c2128; }
    .heat-high { background: rgba(63, 185, 80, 0.15); }
    .heat-mid { background: rgba(210, 153, 34, 0.12); }
    .heat-low { background: rgba(248, 81, 73, 0.12); }
    caption { caption-side: bottom; text-align: left; color: var(--muted); font-size: 0.75rem; padding-top: 0.5rem; }
    .callout {
      margin: 0 1.5rem 1rem;
      padding: 0.75rem 1rem;
      background: #1c2128;
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent-warn);
      border-radius: 6px;
      font-size: 0.82rem;
      color: var(--muted);
    }
    .callout strong { color: var(--text); }
    .class-notes { font-size: 0.78rem; color: var(--muted); margin-top: 0.35rem; }
  </style>
</head>
<body>
  <header>
    <h1>Detection benchmark dashboard</h1>
    <p id="subtitle"></p>
  </header>
  <div class="callout" id="readout"></div>
  <div class="kpis" id="kpis"></div>
  <main>
    <section>
      <h2>Accuracy by class</h2>
      <p class="class-notes">Per-minute / video unique need track_id on both sides. A score of 0 means pred unique counts diverged from GT (not missing data). Tiny bars may be real values near 0%.</p>
      <div class="chart-grid">
        <div class="chart-card wide">
          <div class="chart-wrap tall"><canvas id="chartAccuracy"></canvas></div>
        </div>
      </div>
    </section>
    <section>
      <h2>Detection matching (FP / FN)</h2>
      <div class="chart-grid">
        <div class="chart-card"><div class="chart-wrap"><canvas id="chartFpFn"></canvas></div></div>
        <div class="chart-card"><div class="chart-wrap"><canvas id="chartPrecisionRecall"></canvas></div></div>
      </div>
    </section>
    <section>
      <h2>Detection volume</h2>
      <div class="chart-card wide">
        <div class="chart-wrap"><canvas id="chartTotals"></canvas></div>
      </div>
    </section>
    <section>
      <h2>Temporal (per class)</h2>
      <div class="controls">
        <label for="classSelect">Class</label>
        <select id="classSelect"></select>
      </div>
      <div class="chart-grid">
        <div class="chart-card wide">
          <div class="chart-wrap tall"><canvas id="chartTimeSeries"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-wrap"><canvas id="chartMinuteUnique"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-wrap"><canvas id="chartErrorHist"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-wrap"><canvas id="chartScatter"></canvas></div>
        </div>
      </div>
    </section>
    <section>
      <h2>Summary table</h2>
      <div class="chart-card">
        <table id="summaryTable"><thead></thead><tbody></tbody></table>
        <caption>Source: eval_without_volume semantics · IoU matching for FP/FN</caption>
      </div>
    </section>
  </main>
  <script>
    const DATA = __DASHBOARD_JSON__;
    const chartDefaults = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#8b949e' } }
      },
      scales: {
        x: { ticks: { color: '#8b949e' }, grid: { color: '#21262d' } },
        y: { ticks: { color: '#8b949e' }, grid: { color: '#21262d' } }
      }
    };

    function pct(v) { return v == null ? '—' : (v * 100).toFixed(1) + '%'; }
    function num(v, d=0) { return v == null ? '—' : Number(v).toFixed(d); }
    function prOrNull(v) { return v == null ? null : v; }

    const barValueLabels = {
      id: 'barValueLabels',
      afterDatasetsDraw(chart) {
        const { ctx } = chart;
        chart.data.datasets.forEach((ds, di) => {
          const meta = chart.getDatasetMeta(di);
          if (meta.hidden) return;
          meta.data.forEach((bar, i) => {
            const v = ds.data[i];
            if (v == null) return;
            const label = typeof v === 'number' && v < 1 && v > 0
              ? (v * 100).toFixed(1) + '%'
              : (typeof v === 'number' && v >= 1 ? String(Math.round(v)) : String(v));
            if (v === 0 && chart.options.scales?.y?.max === 1) return;
            ctx.save();
            ctx.fillStyle = '#c9d1d9';
            ctx.font = '10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(label, bar.x, bar.y - 4);
            ctx.restore();
          });
        });
      }
    };

    const meta = DATA.meta;
    document.getElementById('subtitle').textContent =
      `${meta.frame_count} frames · ${meta.fps} fps · ${num(meta.duration_sec, 1)}s · IoU ${meta.iou_threshold} · ${meta.width}×${meta.height}`;

    const kpiEl = document.getElementById('kpis');
    const kpiItems = [
      ['Macro per-frame acc', pct(DATA.macro.macro_per_frame_count_accuracy)],
      ['Macro minute unique', pct(DATA.macro.macro_minute_unique_count_accuracy)],
      ['Macro video unique', pct(DATA.macro.macro_video_unique_count_accuracy)],
      ['Weighted per-frame', pct(DATA.weighted.weighted_per_frame_count_accuracy)],
    ];
    kpiItems.forEach(([label, val]) => {
      const d = document.createElement('div');
      d.className = 'kpi';
      d.innerHTML = `<label>${label}</label><span>${val}</span>`;
      kpiEl.appendChild(d);
    });

    const classes = DATA.classes;
    const summaries = DATA.summaries;

    const notes = classes.filter(c => summaries[c].note).map(c => `<strong>${c}</strong>: ${summaries[c].note}`);
    document.getElementById('readout').innerHTML =
      '<strong>Reading the charts:</strong> Empty-looking bars are usually a score of 0 or N/A, not failed loading. ' +
      'Unique-count metrics compare distinct <code>track_id</code> values; GT and the model tracker often disagree, which drives scores to 0. ' +
      (notes.length ? '<br><br>' + notes.join('<br>') : '');

    function accBarChart() {
      const metrics = ['per_frame_count_accuracy', 'minute_unique_count_accuracy', 'video_unique_count_accuracy'];
      const labels = ['Per-frame count', 'Per-minute unique', 'Video unique'];
      return new Chart(document.getElementById('chartAccuracy'), {
        type: 'bar',
        data: {
          labels: classes,
          datasets: metrics.map((m, i) => ({
            label: labels[i],
            data: classes.map(c => summaries[c][m]),
            backgroundColor: ['#58a6ff', '#3fb950', '#d29922'][i] + 'cc'
          }))
        },
        options: {
          ...chartDefaults,
          plugins: {
            ...chartDefaults.plugins,
            barValueLabels,
            title: { display: true, text: 'Accuracy metrics by class (0–1)', color: '#e6edf3' },
            tooltip: {
              callbacks: {
                afterLabel(ctx) {
                  const c = classes[ctx.dataIndex];
                  const s = summaries[c];
                  return `GT unique IDs: ${s.gt_video_unique}, pred: ${s.pred_video_unique}`;
                }
              }
            }
          },
          scales: {
            ...chartDefaults.scales,
            y: { ...chartDefaults.scales.y, min: 0, max: 1, title: { display: true, text: 'Accuracy', color: '#8b949e' } }
          }
        }
      });
    }

    function fpFnChart() {
      return new Chart(document.getElementById('chartFpFn'), {
        type: 'bar',
        data: {
          labels: classes,
          datasets: [
            { label: 'False positives', data: classes.map(c => summaries[c].fp), backgroundColor: '#f85149aa' },
            { label: 'False negatives', data: classes.map(c => summaries[c].fn), backgroundColor: '#d29922aa' }
          ]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, barValueLabels, title: { display: true, text: 'FP / FN (summed over frames)', color: '#e6edf3' } },
          scales: {
            ...chartDefaults.scales,
            y: { ...chartDefaults.scales.y, type: 'logarithmic', title: { display: true, text: 'Count (log)', color: '#8b949e' } }
          }
        }
      });
    }

    function prChart() {
      return new Chart(document.getElementById('chartPrecisionRecall'), {
        type: 'bar',
        data: {
          labels: classes,
          datasets: [
            { label: 'Precision', data: classes.map(c => prOrNull(summaries[c].precision)), backgroundColor: '#58a6ffaa' },
            { label: 'Recall', data: classes.map(c => prOrNull(summaries[c].recall)), backgroundColor: '#3fb950aa' },
            { label: 'F1', data: classes.map(c => prOrNull(summaries[c].f1)), backgroundColor: '#d29922aa' }
          ]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, barValueLabels, title: { display: true, text: 'Precision / recall / F1 (IoU matching)', color: '#e6edf3' } },
          scales: { ...chartDefaults.scales, y: { ...chartDefaults.scales.y, min: 0, max: 1 } }
        }
      });
    }

    function totalsChart() {
      return new Chart(document.getElementById('chartTotals'), {
        type: 'bar',
        data: {
          labels: classes,
          datasets: [
            { label: 'GT detections', data: classes.map(c => summaries[c].gt_total_detections), backgroundColor: '#58a6ff99' },
            { label: 'Pred detections', data: classes.map(c => summaries[c].pred_total_detections), backgroundColor: '#3fb95099' }
          ]
        },
        options: {
          indexAxis: 'y',
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, title: { display: true, text: 'Total box detections by class', color: '#e6edf3' } }
        }
      });
    }

    let timeChart, minuteChart, histChart, scatterChart;

    function updateTemporal(cls) {
      const s = DATA.series[cls];
      if (!s) return;
      const t = s.t_sec;
      if (timeChart) timeChart.destroy();
      timeChart = new Chart(document.getElementById('chartTimeSeries'), {
        type: 'line',
        data: {
          labels: t,
          datasets: [
            { label: 'GT count', data: s.gt_count, borderColor: '#58a6ff', tension: 0.1, pointRadius: 0 },
            { label: 'Pred count', data: s.pred_count, borderColor: '#3fb950', tension: 0.1, pointRadius: 0 }
          ]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, title: { display: true, text: `Per-frame counts · ${cls}`, color: '#e6edf3' } },
          scales: {
            x: { ...chartDefaults.scales.x, title: { display: true, text: 'Time (s)', color: '#8b949e' } },
            y: { ...chartDefaults.scales.y, title: { display: true, text: 'Count', color: '#8b949e' } }
          }
        }
      });
      if (minuteChart) minuteChart.destroy();
      minuteChart = new Chart(document.getElementById('chartMinuteUnique'), {
        type: 'line',
        data: {
          labels: s.minute_t_sec,
          datasets: [
            { label: 'GT unique', data: s.minute_gt_unique, borderColor: '#58a6ff', tension: 0.1 },
            { label: 'Pred unique', data: s.minute_pred_unique, borderColor: '#3fb950', tension: 0.1 }
          ]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, title: { display: true, text: `Per-minute unique IDs · ${cls}`, color: '#e6edf3' } },
          scales: { x: { ...chartDefaults.scales.x, title: { display: true, text: 'Window end (s)', color: '#8b949e' } } }
        }
      });
      if (histChart) histChart.destroy();
      const h = s.error_hist;
      histChart = new Chart(document.getElementById('chartErrorHist'), {
        type: 'bar',
        data: {
          labels: h.labels,
          datasets: [{ label: 'Frames', data: h.counts, backgroundColor: '#8b949e99' }]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, title: { display: true, text: `Count error (pred − GT) · ${cls}`, color: '#e6edf3' } },
          scales: { x: { ...chartDefaults.scales.x, title: { display: true, text: 'Error', color: '#8b949e' } } }
        }
      });
      if (scatterChart) scatterChart.destroy();
      scatterChart = new Chart(document.getElementById('chartScatter'), {
        type: 'scatter',
        data: {
          datasets: [{
            label: 'GT vs pred count',
            data: s.scatter_gt.map((g, i) => ({ x: g, y: s.scatter_pred[i] })),
            backgroundColor: '#58a6ff88',
            pointRadius: 3
          }]
        },
        options: {
          ...chartDefaults,
          plugins: { ...chartDefaults.plugins, title: { display: true, text: `Count scatter · ${cls}`, color: '#e6edf3' } },
          scales: {
            x: { ...chartDefaults.scales.x, title: { display: true, text: 'GT count', color: '#8b949e' } },
            y: { ...chartDefaults.scales.y, title: { display: true, text: 'Pred count', color: '#8b949e' } }
          }
        }
      });
    }

    const sel = document.getElementById('classSelect');
    classes.forEach(c => {
      const o = document.createElement('option');
      o.value = c; o.textContent = c;
      sel.appendChild(o);
    });
    sel.value = DATA.default_class;
    sel.addEventListener('change', () => updateTemporal(sel.value));

    function heatClass(v, invert) {
      if (v == null) return '';
      const x = invert ? 1 - v : v;
      if (x >= 0.8) return 'heat-high';
      if (x >= 0.5) return 'heat-mid';
      return 'heat-low';
    }

    const cols = [
      ['class', r => r.class, () => ''],
      ['Per-frame acc', r => pct(r.per_frame_count_accuracy), r => heatClass(r.per_frame_count_accuracy, false)],
      ['Minute unique', r => pct(r.minute_unique_count_accuracy), r => heatClass(r.minute_unique_count_accuracy, false)],
      ['Video unique', r => pct(r.video_unique_count_accuracy), r => heatClass(r.video_unique_count_accuracy, false)],
      ['Exact match', r => pct(r.exact_match_fraction), r => heatClass(r.exact_match_fraction, false)],
      ['Precision', r => pct(r.precision), r => heatClass(r.precision, false)],
      ['Recall', r => pct(r.recall), r => heatClass(r.recall, false)],
      ['F1', r => pct(r.f1), r => heatClass(r.f1, false)],
      ['FP', r => r.fp, () => ''],
      ['FN', r => r.fn, () => ''],
      ['GT boxes', r => r.gt_total_detections, () => ''],
      ['Pred boxes', r => r.pred_total_detections, () => ''],
      ['GT unique IDs', r => r.gt_video_unique, () => ''],
      ['Pred unique IDs', r => r.pred_video_unique, () => ''],
    ];
    const thead = document.querySelector('#summaryTable thead');
    const tbody = document.querySelector('#summaryTable tbody');
    const hr = document.createElement('tr');
    cols.forEach(([h]) => { const th = document.createElement('th'); th.textContent = h; hr.appendChild(th); });
    thead.appendChild(hr);
    DATA.table_rows.forEach(row => {
      const tr = document.createElement('tr');
      cols.forEach(([, fn, heat]) => {
        const td = document.createElement('td');
        td.textContent = fn(row);
        const cl = heat(row);
        if (cl) td.className = cl;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    accBarChart();
    fpFnChart();
    prChart();
    totalsChart();
    updateTemporal(sel.value);
  </script>
</body>
</html>
"""


def render_html(data: dict[str, Any]) -> str:
    payload = json.dumps(data, separators=(",", ":"))
    # Prevent </script> breakout in embedded JSON
    payload = payload.replace("</", "<\\/")
    return _html_template().replace("__DASHBOARD_JSON__", payload)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--gt", type=Path, default=_APPS_VC / "gt-tracked.json")
    p.add_argument("--pred", type=Path, default=_APPS_VC / "pred-tracked.json")
    p.add_argument("--bench", type=Path, default=_APPS_VC / "bench.json")
    p.add_argument("--out", type=Path, default=_APPS_VC / "bench-dashboard.html")
    p.add_argument("--iou", type=float, default=0.5)
    p.add_argument("--conf-threshold", type=float, default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if not args.gt.is_file():
        sys.exit(f"GT JSON not found: {args.gt}")
    if not args.pred.is_file():
        sys.exit(f"Pred JSON not found: {args.pred}")

    bench_path = args.bench if args.bench.is_file() else None
    if bench_path is None and args.bench.parent == _APPS_VC:
        try:
            from build_bench_json import build_bench_report

            report = build_bench_report(
                args.gt,
                args.pred,
                iou_threshold=args.iou,
                confidence_threshold=args.conf_threshold,
            )
            args.bench.write_text(json.dumps(report, indent=2), encoding="utf-8")
            bench_path = args.bench
            print(f"Wrote {args.bench.resolve()} (metrics from eval_without_volume)")
        except ImportError:
            pass

    data = build_dashboard_data(
        args.gt,
        args.pred,
        bench_path,
        iou_threshold=args.iou,
        confidence_threshold=args.conf_threshold,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    html = render_html(data)
    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote {args.out.resolve()}")


if __name__ == "__main__":
    main()
