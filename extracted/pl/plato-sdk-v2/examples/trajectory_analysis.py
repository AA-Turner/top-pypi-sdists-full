"""Fetch and display an ATIF trajectory from Chronos."""

from plato.chronos.sdk import Chronos

SESSION_ID = "12d4aae8-31f2-4d1d-b936-4e5093dafa03"

chronos = Chronos()
traj = chronos.get_trajectory(SESSION_ID)

# --- Session overview ---
print(f"Session  {traj.session_id}  [{traj.status}]")
print()

# --- World ---
w = traj.world
if w:
    print(f"World    {w.name} v{w.version}")
    if w.observation:
        print(f"  reset: {str(w.observation)[:200]}")
    steps = w.steps or []
    print(f"  {len(steps)} step(s)")
    print()

    for ws in steps:
        duration = ""
        if ws.start_time_unix_nano and ws.end_time_unix_nano:
            ms = (ws.end_time_unix_nano - ws.start_time_unix_nano) / 1_000_000
            duration = f"  ({ms:.0f}ms)"
        done_marker = " DONE" if ws.done else ""
        print(f"  step {ws.number}{done_marker}{duration}")
        if ws.observation:
            print(f"    obs: {str(ws.observation)[:200]}")
        for a in ws.agents or []:
            n = len(a.trajectory.steps) if a.trajectory.steps else 0
            print(f"    agent: {a.agent.name} ({n} steps)")
    print()

# --- Agents ---
for agent_trace in traj.agents or []:
    info = agent_trace.agent
    status = "ok" if info.success else (f"err: {info.error}" if info.error else "?")
    print(f"Agent    {info.name} v{info.version}  model={info.model_name}  [{status}]")

    if info.result:
        print(f"  result: {info.result[:200]}")

    steps = agent_trace.trajectory.steps or []
    for step in steps:
        msg = (step.message or "")[:120]
        print(f"  {step.step_id:>3}  [{step.source:<6}] {msg}")

        if step.tool_calls and isinstance(step.tool_calls, list):
            for tc in step.tool_calls:
                print(f"         -> {tc.function_name}({tc.arguments})")

        if step.observation and not isinstance(step.observation, str) and step.observation.results:
            for r in step.observation.results:
                print(f"         <- {r.content[:120]}")

        if step.screenshot:
            print(f"         [screenshot {step.screenshot_format}, {len(step.screenshot)} chars]")

        if step.metrics:
            m = step.metrics
            parts = []
            if m.prompt_tokens or m.completion_tokens:
                parts.append(f"{m.prompt_tokens or 0}/{m.completion_tokens or 0} tok")
            if m.cost_usd:
                parts.append(f"${m.cost_usd:.4f}")
            if parts:
                print(f"         {', '.join(parts)}")

    fm = agent_trace.trajectory.final_metrics
    if fm:
        total_tok = (fm.prompt_tokens or 0) + (fm.completion_tokens or 0)
        print(f"  total: {fm.total_steps} steps, {total_tok} tokens, ${fm.cost_usd:.4f}")
    print()

# --- Artifacts ---
artifacts = traj.artifacts or []
if artifacts:
    print(f"Artifacts ({len(artifacts)})")
    for art in artifacts:
        print(f"  {art.kind}: {art.url}")
    print()

chronos.close()
