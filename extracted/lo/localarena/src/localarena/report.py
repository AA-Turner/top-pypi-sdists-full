"""Self-contained HTML visualization for evaluation runs."""

from __future__ import annotations

import html
from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path

from .evaluation import EvaluationRun


def _escape(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _format_number(value: object, digits: int = 3) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def render_html_report(
    run: EvaluationRun,
    *,
    title: str | None = None,
) -> str:
    """Render one portable report with no external assets or network calls."""

    report_title = title or run.name
    summary = run.summary()
    task_ids = [str(task["id"]) for task in run.tasks]
    errors = sum(record.error is not None for record in run.records)
    scored = sum(record.score is not None for record in run.records)
    total_seconds = sum(record.duration_seconds for record in run.records)
    judge_rows: list[str] = []
    for task in run.tasks:
        evaluator = task.get("evaluator")
        if (
            not isinstance(evaluator, Mapping)
            or evaluator.get("type") != "model_judge"
        ):
            continue
        target = evaluator.get("target")
        if not isinstance(target, Mapping):
            continue
        parameters = target.get("parameters")
        if not isinstance(parameters, Mapping):
            parameters = {}
        judge_rows.append(
            f"""
            <tr>
              <td>{_escape(task.get("id"))}</td>
              <td><strong>{_escape(target.get("name"))}</strong></td>
              <td>{_escape(target.get("provider"))}</td>
              <td>{_escape(target.get("model"))}</td>
              <td class="metric">{_escape(parameters.get("max_tokens"))}</td>
              <td class="metric">{_format_number(parameters.get("temperature"))}</td>
            </tr>
            """
        )
    judge_section = (
        f"""
    <section>
      <h2>Live judges</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Task</th><th>Target</th><th>Provider</th><th>Model</th><th>Max tokens</th><th>Temperature</th></tr></thead>
          <tbody>{''.join(judge_rows)}</tbody>
        </table>
      </div>
    </section>
        """
        if judge_rows
        else ""
    )

    score_rows = []
    for row in summary:
        score = row["reliability_adjusted_score"]
        width = 0 if score is None else max(0, min(100, float(score) * 100))
        evidence = (
            "inconclusive"
            if row["arena_inconclusive"]
            else "separated"
        )
        confidence = (
            f"{_format_number(row['arena_confidence_lower'], 1)}–"
            f"{_format_number(row['arena_confidence_upper'], 1)}"
        )
        score_rows.append(
            f"""
            <tr>
              <td><strong>{_escape(row["name"])}</strong><br>
                <span class="muted">{_escape(row["provider"])} · {_escape(row["model"])}</span>
              </td>
              <td class="metric">{_format_number(score)}</td>
              <td class="chart-cell"><div class="bar-track"><div class="bar" style="width:{width:.2f}%"></div></div></td>
              <td class="metric">{_format_number(row["average_score"])}</td>
              <td class="metric">{_format_number(row["score_coverage"])}</td>
              <td class="metric"><strong>{_format_number(row["arena_rating"], 1)}</strong><br><span class="muted">{confidence}</span></td>
              <td>{_escape(evidence)}</td>
              <td class="metric">{_format_number(row["pass_rate"])}</td>
              <td class="metric">{_format_number(row["average_latency_seconds"])}</td>
              <td class="metric">{_escape(row["input_tokens"])} / {_escape(row["output_tokens"])}</td>
              <td class="metric">{_format_number(row["judge_latency_seconds"])}</td>
              <td class="metric">{_escape(row["judge_input_tokens"])} / {_escape(row["judge_output_tokens"])}</td>
              <td class="metric">{_escape(row["successful"])} / {_escape(row["runs"])}</td>
              <td class="metric error-count">{_escape(row["errors"])}</td>
            </tr>
            """
        )

    grouped: dict[tuple[str, str], list[float]] = defaultdict(list)
    failures: set[tuple[str, str]] = set()
    for record in run.records:
        key = (record.target, record.task_id)
        if record.score is not None:
            grouped[key].append(record.score.value)
        if record.error is not None:
            failures.add(key)

    matrix_header = "".join(f"<th>{_escape(task_id)}</th>" for task_id in task_ids)
    matrix_rows = []
    for model in run.models:
        name = str(model["name"])
        cells = []
        for task_id in task_ids:
            values = grouped.get((name, task_id), [])
            if values:
                value = sum(values) / len(values)
                hue = value * 120
                cells.append(
                    f'<td class="heat" style="--heat:{hue:.1f}">{_format_number(value)}</td>'
                )
            elif (name, task_id) in failures:
                cells.append('<td class="heat failed">error</td>')
            else:
                cells.append('<td class="heat missing">—</td>')
        matrix_rows.append(
            f"<tr><th>{_escape(name)}</th>{''.join(cells)}</tr>"
        )

    detail_rows = []
    for record in run.records:
        score_text = (
            _format_number(record.score.value)
            if record.score is not None
            else "—"
        )
        answer = ""
        if run.include_content and record.generation is not None:
            answer = record.generation.text
        score_reason = (
            record.score.reason
            if run.include_content and record.score is not None
            else "Not retained"
        )
        error_detail = (
            record.error
            if run.include_content and record.error is not None
            else (
                "Error details not retained"
                if record.error is not None
                else None
            )
        )
        detail_rows.append(
            f"""
            <details class="record {'record-error' if record.error else ''}">
              <summary>
                <span class="status status-{_escape(record.status)}">{_escape(record.status)}</span>
                <strong>{_escape(record.target)}</strong>
                <span>× {_escape(record.task_id)}</span>
                <span class="grow"></span>
                <span>score {score_text}</span>
                <span>{_format_number(record.duration_seconds)}s</span>
              </summary>
              <div class="record-grid">
                <div><h4>Answer</h4><pre>{_escape(answer) if answer else "Not retained"}</pre></div>
                <div>
                  <h4>Evaluation</h4>
                  <p>{_escape(score_reason) if record.score is not None else "No score"}</p>
                  <h4>Provider result</h4>
                  <dl>
                    <dt>Provider</dt><dd>{_escape(record.provider)}</dd>
                    <dt>Model</dt><dd>{_escape(record.model)}</dd>
                    <dt>Repetition</dt><dd>{record.repetition}</dd>
                    <dt>Finish reason</dt><dd>{_escape(record.generation.finish_reason) if record.generation else "—"}</dd>
                  </dl>
                  {'<h4>Error</h4><pre>' + _escape(error_detail) + '</pre>' if error_detail else ''}
                </div>
              </div>
            </details>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark light">
  <link rel="icon" href="data:,">
  <title>{_escape(report_title)} · LocalArena</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #121a2d;
      --panel-2: #18233a;
      --text: #e8edf7;
      --muted: #9aa8bf;
      --line: #2a3853;
      --accent: #5eead4;
      --accent-2: #60a5fa;
      --danger: #fb7185;
      --shadow: 0 18px 50px rgba(0,0,0,.22);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at 12% 0%, #172554 0, transparent 30rem), var(--bg);
      color: var(--text);
      font: 15px/1.5 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{ width: min(1380px, calc(100% - 32px)); margin: 42px auto 80px; }}
    h1 {{ font-size: clamp(30px, 5vw, 54px); line-height: 1.05; margin: 0 0 10px; letter-spacing: -.04em; }}
    h2 {{ margin: 0 0 20px; font-size: 22px; }}
    h4 {{ margin: 0 0 8px; }}
    .eyebrow {{ color: var(--accent); font-size: 12px; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }}
    .subtitle {{ color: var(--muted); margin: 0; }}
    .cards {{ display: grid; grid-template-columns: repeat(5, minmax(120px, 1fr)); gap: 12px; margin: 28px 0; }}
    .card, section {{
      border: 1px solid var(--line);
      border-radius: 16px;
      background: color-mix(in srgb, var(--panel) 94%, transparent);
      box-shadow: var(--shadow);
    }}
    .card {{ padding: 18px; }}
    .card .value {{ display: block; font-size: 27px; font-weight: 800; }}
    .card .label, .muted {{ color: var(--muted); }}
    section {{ padding: 22px; margin-top: 18px; overflow: hidden; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 12px 10px; text-align: left; vertical-align: middle; }}
    th {{ color: var(--muted); font-size: 12px; letter-spacing: .05em; text-transform: uppercase; }}
    tbody tr:last-child td, tbody tr:last-child th {{ border-bottom: 0; }}
    .metric {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
    .chart-cell {{ min-width: 180px; width: 28%; }}
    .bar-track {{ width: 100%; height: 11px; border-radius: 999px; background: var(--panel-2); overflow: hidden; }}
    .bar {{ height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--accent-2), var(--accent)); }}
    .error-count {{ color: var(--danger); }}
    .matrix th:first-child {{ position: sticky; left: 0; background: var(--panel); z-index: 1; }}
    .heat {{ text-align: center; font-weight: 800; color: white; background: hsl(var(--heat) 48% 33%); min-width: 90px; }}
    .heat.failed {{ background: #7f1d1d; }}
    .heat.missing {{ background: var(--panel-2); color: var(--muted); }}
    details.record {{ border-top: 1px solid var(--line); }}
    details.record:first-of-type {{ border-top: 0; }}
    summary {{ cursor: pointer; display: flex; align-items: center; gap: 13px; padding: 14px 4px; list-style: none; }}
    summary::-webkit-details-marker {{ display: none; }}
    summary::before {{ content: "›"; color: var(--muted); font-size: 22px; transition: transform .15s ease; }}
    details[open] summary::before {{ transform: rotate(90deg); }}
    .grow {{ flex: 1; }}
    .status {{ padding: 3px 8px; border-radius: 999px; font-size: 11px; font-weight: 800; text-transform: uppercase; background: #164e63; }}
    .status-generation_error, .status-score_error {{ background: #881337; }}
    .record-grid {{ display: grid; grid-template-columns: 1.5fr 1fr; gap: 18px; padding: 4px 4px 20px 42px; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; margin: 0; padding: 13px; border-radius: 10px; background: #070b15; color: #dbeafe; max-height: 420px; overflow: auto; }}
    dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 5px 12px; margin: 0; }}
    dt {{ color: var(--muted); }} dd {{ margin: 0; overflow-wrap: anywhere; }}
    footer {{ color: var(--muted); text-align: center; margin-top: 26px; font-size: 13px; }}
    @media (max-width: 820px) {{
      .cards {{ grid-template-columns: repeat(2, 1fr); }}
      .record-grid {{ grid-template-columns: 1fr; padding-left: 4px; }}
      summary span:not(.status):not(.grow) {{ display: none; }}
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f5f7fb; --panel: #ffffff; --panel-2: #edf2f7; --text: #172033;
        --muted: #60708a; --line: #d8e0eb; --shadow: 0 16px 45px rgba(35,50,80,.09);
      }}
      body {{ background: radial-gradient(circle at 12% 0%, #dbeafe 0, transparent 30rem), var(--bg); }}
      pre {{ background: #111827; color: #e5edff; }}
      .matrix th:first-child {{ background: var(--panel); }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">LocalArena live evaluation</div>
      <h1>{_escape(report_title)}</h1>
      <p class="subtitle">Run {_escape(run.id)} · {_escape(run.started_at)} → {_escape(run.finished_at)}</p>
    </header>

    <div class="cards">
      <div class="card"><span class="value">{len(run.models)}</span><span class="label">models</span></div>
      <div class="card"><span class="value">{len(run.tasks)}</span><span class="label">tasks</span></div>
      <div class="card"><span class="value">{len(run.records)}</span><span class="label">evaluation rows</span></div>
      <div class="card"><span class="value">{scored}</span><span class="label">scored</span></div>
      <div class="card"><span class="value">{errors}</span><span class="label">errors · {_format_number(total_seconds, 1)}s total</span></div>
    </div>

    <section>
      <h2>Leaderboard</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Model</th><th>Decision score</th><th>Relative decision score</th><th>Raw mean</th><th>Score coverage</th><th>Arena rating · 95% CI</th><th>Evidence</th><th>Pass rate</th><th>Candidate latency (s)</th><th>Candidate tokens in / out</th><th>Judge latency (s)</th><th>Judge tokens in / out</th><th>Successful / runs</th><th>Errors</th></tr></thead>
          <tbody>{''.join(score_rows)}</tbody>
        </table>
      </div>
    </section>

    {judge_section}

    <section>
      <h2>Task matrix</h2>
      <div class="table-wrap">
        <table class="matrix">
          <thead><tr><th>Model</th>{matrix_header}</tr></thead>
          <tbody>{''.join(matrix_rows)}</tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>Outputs and diagnostics</h2>
      {''.join(detail_rows)}
    </section>

    <footer>Generated locally by LocalArena. Provider credentials and endpoint URLs are not included.</footer>
  </main>
</body>
</html>
"""


def write_html_report(
    run: EvaluationRun,
    path: str | Path,
    *,
    title: str | None = None,
) -> Path:
    """Write a self-contained HTML report and return its path."""

    destination = Path(path)
    destination.write_text(
        render_html_report(run, title=title),
        encoding="utf-8",
    )
    return destination
