"""Pure manual-gate resolution for the CI job runner.

Given a resolved dependency chain and the pipeline's jobs, decide which manual
"gate" jobs (e.g. a ``start`` stage) must be played first because downstream
chain jobs depend on them through stage ordering. Entirely side-effect free —
no network, no sleep — and directly unit-testable.
"""

from .deps_resolver import _stage_order_from_jobs
from .gitlab_api import Job


def _is_manual_gate_job(job: Job) -> bool:
    """Whether a job acts as a manual gate.

    GitLab's REST API often returns ``when: null`` even for manual jobs, so
    relying on ``when`` alone misses real gates. ``status == "manual"`` is the
    reliable runtime signal: a job whose dependencies are satisfied and that
    is awaiting a play action will be reported in that state. We keep the
    ``when`` check as a complement for jobs that haven't transitioned yet.
    """
    return job.status == "manual" or job.when == "manual"


def add_manual_gates(
    target_name: str,
    chain: list[str],
    jobs: list[Job],
    needs_map: dict[str, list[str]] | None = None,
) -> list[str]:
    """Prepend manual-gate jobs that block the chain through stage ordering.

    A stage S is a "manual gate" for the target only if **some chain job**
    actually depends on S completing. With explicit ``needs:`` (DAG mode) a
    job only waits on its declared needs, not on prior stages — so most
    pipelines have no stage gates at all. The classic case the runner still
    has to cover is a ``start`` stage that downstream jobs depend on through
    stage ordering rather than an explicit ``needs:`` link.

    Rule used here: a stage S contributes gates iff at least one chain job J
    in a strictly later stage has **no explicit needs** (i.e. ``needs_map[J]``
    is empty or absent). Such a J is stage-ordered and would be blocked by
    every job in S. When every chain job has explicit needs, no stage is a
    gate and the chain is returned unchanged. The legacy "all stages before
    the target" behaviour is preserved when ``needs_map`` is ``None`` (e.g.
    YAML parsing failed entirely) so we don't deadlock the runner waiting on
    a manual gate we forgot to play.

    Within a candidate stage, only **blocking** jobs count: a job with
    ``allow_failure: true`` never gates the pipeline (GitLab lets later
    stages start without waiting for it), so advisory jobs such as the
    ``allow_failure`` AI-review / SAST jobs are ignored entirely — they are
    neither gates nor auto-played. The stage is treated as a gate when
    **every** blocking job in it is manual — either in ``status: manual`` or
    declared with ``when: manual``. Mixed stages (some auto, some manual) are
    skipped to avoid sweeping ordinary parallel manual jobs (e.g. a stage
    containing both ``deploy_review`` and ``deploy_prod``).
    """
    target_job = next((j for j in jobs if j.name == target_name), None)
    if not target_job:
        return chain

    stage_order = _stage_order_from_jobs(jobs)
    if target_job.stage not in stage_order:
        return chain
    target_idx = stage_order.index(target_job.stage)
    if target_idx == 0:
        return chain

    # Determine which stages can plausibly block the chain.
    gating_stages = _stages_that_gate_chain(chain, jobs, stage_order, target_idx, needs_map)
    if not gating_stages:
        return chain

    by_stage: dict[str, list[Job]] = {}
    for j in jobs:
        by_stage.setdefault(j.stage, []).append(j)

    chain_set = set(chain)
    extras: list[Job] = []
    for stage in stage_order[:target_idx]:
        if stage not in gating_stages:
            continue
        # ``allow_failure`` jobs don't block stage transitions, so they never
        # gate the chain — only blocking jobs decide whether this stage is a gate.
        blocking = [j for j in by_stage.get(stage, []) if not j.allow_failure]
        if not blocking or not all(_is_manual_gate_job(j) for j in blocking):
            continue
        for j in sorted(blocking, key=lambda x: x.id):
            if j.name not in chain_set:
                extras.append(j)

    return [j.name for j in extras] + chain


def _stages_that_gate_chain(
    chain: list[str],
    jobs: list[Job],
    stage_order: list[str],
    target_idx: int,
    needs_map: dict[str, list[str]] | None,
) -> set[str]:
    """Return the set of stages whose jobs can block the chain via stage ordering.

    Without a needs map we have no choice but to assume the worst (legacy
    behaviour): every stage before the target is a candidate gate. With a
    needs map, only stages strictly before a stage-ordered chain job count —
    a chain job is "stage-ordered" when it has no explicit ``needs:`` and
    therefore waits for every job in earlier stages.
    """
    if needs_map is None:
        return set(stage_order[:target_idx])

    jobs_by_name = {j.name: j for j in jobs}
    blocked: set[str] = set()
    for name in chain:
        job = jobs_by_name.get(name)
        if not job or job.stage not in stage_order:
            continue
        if needs_map.get(name):
            continue  # explicit needs → DAG mode, not gated by earlier stages
        idx = stage_order.index(job.stage)
        for stage in stage_order[:idx]:
            blocked.add(stage)
    return blocked
