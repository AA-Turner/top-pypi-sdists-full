"""MolmoSpaces batches use one shared Dreamscale session and existing sim metrics."""

from __future__ import annotations

import json
from pathlib import Path
from time import monotonic

from dreamscale_transport.cosmos3 import MODEL_ID

from dreamscale import errors
from dreamscale.config import load_config
from dreamscale.model_names import public_model
from dreamscale.policy.lifecycle import _validate_keep_warm

from .artifacts import SimArtifactRecorder
from .molmospaces_catalog import BENCHMARKS, episode_selection, selected_suites
from .molmospaces_runtime import MolmoSpacesSimEnv, benchmark_counts, ensure_molmospaces_runtime
from .sim_arm import connect_libero

# The qualified Cosmos worker has a one-hour provider lifetime. Renew between
# episodes with ample time for cold startup and scene preparation.
_SESSION_RENEW_AFTER_S = 30 * 60


def aggregate_results(episodes):
    suites = {}
    for item in episodes:
        record = suites.setdefault(item["task_suite"], {"episodes": 0, "successes": 0})
        record["episodes"] += 1
        record["successes"] += int(item["done"])
    for record in suites.values():
        record["oracle_success_rate"] = record["successes"] / record["episodes"]
    return {
        "suites": suites,
        "episodes": len(episodes),
        "successes": sum(item["done"] for item in episodes),
        "mean_suite_oracle_success_rate": (
            sum(item["oracle_success_rate"] for item in suites.values()) / len(suites)
            if suites
            else 0
        ),
    }


def run_molmospaces(
    *,
    model=MODEL_ID,
    task_suite="all",
    task_id=0,
    task_seed=0,
    max_steps=None,
    max_duration=None,
    view=True,
    tui=True,
    real_time=True,
    json_output=False,
    output_root=None,
    keep_warm=0,
    region=None,
    transport="auto",
    verbose=False,
    on_line=print,
    steady_send=None,
):
    from .benchmarks import validate_selection

    task_id = validate_selection("molmospaces", model, task_suite, task_id)
    suites = selected_suites(task_suite)
    selection = episode_selection(task_id)
    keep_warm = _validate_keep_warm(keep_warm)
    if not load_config().api_key:
        raise errors.catalog("not_configured")
    root = Path(output_root).expanduser().resolve() if output_root is not None else None
    if root is not None:
        if root.exists() and any(root.iterdir()):
            raise FileExistsError(f"artifact directory is not empty: {root}")
        root.mkdir(parents=True, exist_ok=True)
    # Bootstrap both native renderer variants before requesting cloud compute.
    executables = {
        renderer: ensure_molmospaces_runtime(renderer=renderer, on_line=on_line)
        for renderer in dict.fromkeys(BENCHMARKS[name].renderer for name in suites)
    }
    counts = benchmark_counts(suites, next(iter(executables.values())))
    if selection != "all":
        for name, count in counts.items():
            if selection >= count:
                raise ValueError(f"{name} --task-id must be 0–{count - 1}")
    rows = []
    sim = None
    session_started = None
    env = None
    summary = {
        "benchmark": "molmospaces",
        "model": public_model(model),
        "task_suite": task_suite,
        "task_id": selection,
        "task_seed": task_seed,
        "success_condition": "upstream_judge_success_oracle",
        "results": rows,
        "previous_sessions": [],
    }
    try:
        for name in suites:
            index = 0 if selection == "all" else selection
            count = counts[name]
            while index < count:
                on_line(f"Preparing MolmoSpaces {name}, episode {index}…")
                env = MolmoSpacesSimEnv(
                    suite=name,
                    task_id=index,
                    seed=task_seed,
                    python=executables[BENCHMARKS[name].renderer],
                )
                count = env.episode_count
                if sim is not None and monotonic() - session_started >= _SESSION_RENEW_AFTER_S:
                    on_line("Renewing compute before the next episode…")
                    # A parked worker retains its original hard lifetime.
                    sim._keep_warm = 0
                    sim.close()
                    summary["previous_sessions"].append({
                        "session_id": sim._session.session_id,
                        "status": sim.release_status or "unknown",
                    })
                    if sim.release_status != "closed":
                        raise RuntimeError("Compute release unconfirmed; cannot renew the session")
                    sim = None
                if sim is None:
                    session_started = monotonic()
                    sim = connect_libero(
                        model=model,
                        benchmark="molmospaces",
                        task_suite=name,
                        task_id=index,
                        task_seed=task_seed,
                        env_factory=lambda prepared=env: prepared,
                        keep_warm=keep_warm,
                        region=region,
                        transport=transport,
                        view=view,
                        verbose=verbose,
                        on_line=on_line,
                        steady_send=steady_send,
                    )
                    summary["session_id"] = sim._session.session_id
                else:
                    sim._env.close()
                    sim._env = env
                    if view:
                        sim._render_frame = env.render_frame
                on_line(f"[local] task: {env.task_description}")
                recorder = None
                if root is not None:
                    recorder = SimArtifactRecorder(
                        root / name / f"episode-{index:05d}", fps=15, video_writer=env.write_video
                    )
                    recorder.start()
                horizon = (
                    max_steps or max(1, int(max_duration * 15 + 0.999999))
                    if max_duration
                    else max_steps or env.horizon_steps
                )
                try:
                    result = sim.do(
                        max_steps=horizon,
                        tui=tui and not json_output,
                        real_time=real_time,
                        on_frame=None if recorder is None else recorder.frame,
                        on_buffer=None if recorder is None else recorder.buffer,
                        on_policy_timing=None if recorder is None else recorder.policy_timing,
                    )
                    row = {
                        "task_suite": name,
                        "task_id": index,
                        "instruction": env.task_description,
                        "done": result.done,
                        "steps": result.steps,
                        "policy_calls": result.policy_calls,
                        "metrics": result.metrics,
                        "benchmark_info": env.benchmark_info,
                        "episode_count": count,
                        "max_steps": horizon,
                    }
                    rows.append(row)
                    if recorder:
                        recorder.finish(summary=row)
                    on_line(
                        f"{name} episode {index}: {'success' if result.done else 'not complete'}"
                    )
                    if root:
                        (root / "summary.json").write_text(json.dumps(summary, indent=2))
                except BaseException as exc:
                    if recorder:
                        recorder.fail(exc)
                    raise
                index += 1
                if selection != "all":
                    break
        summary.update(aggregate_results(rows))
        summary["full_benchmark"] = (
            selection == "all" and not max_steps and not max_duration and task_seed == 0
        )
    except BaseException as exc:
        summary.update(aggregate_results(rows))
        summary["error"] = str(exc)
        raise
    finally:
        try:
            if sim is not None:
                sim.close()
                summary["session"] = sim.release_status or "unknown"
                summary["keep_warm_s"] = keep_warm
                summary["worker"] = {
                    "parked": "warm_reserved", "parking": "warm_reservation_pending",
                    "closed": "reservation_released",
                }.get(summary["session"], "release_unconfirmed")
            if env is not None and (sim is None or sim._env is not env):
                env.close()
        finally:
            if root:
                (root / "summary.json").write_text(json.dumps(summary, indent=2))
    on_line(f"MolmoSpaces: {summary['successes']}/{summary['episodes']} episodes succeeded")
    if json_output:
        on_line(json.dumps(summary, sort_keys=True))
    return summary
