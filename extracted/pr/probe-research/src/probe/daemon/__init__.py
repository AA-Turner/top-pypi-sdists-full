"""The Probe daemon, version 2: one program that records a coding session in Probe.

Two processes per session. Capture (the stdlib `tap`, today's `tap watch`) ships
the transcript and supervises the AI process; this package is the AI process.
It reads the harness's chat log into a queue the moment lines land, thinks in
bites (your prompt, the agent's turn end, a size limit, anything ~2 minutes
old), and records with the same `probe` CLI the coding agent uses, each command
checked in plain code before it runs (`probe.shared.command_rules`).

    worker/     the loop: class Worker and its parts; bite/ is what one model call sees
    agent/      the model agents (writer, reader, audit, tasks), model/, tools/
    shell/      the daemon's shell: safe commands run, the rest ask the researcher
    lanes/      what runs beside the writer (lane.py: Lane): reader, audit, run alerts
    store/      the session's scrubbed event store, queue watermark, logbook
    host/       every session's worker in one process; session/ its folders and scope
    trace/      the agents' own trace files; prompts/ the job texts
    (chat log -> events per harness, and asking the researcher: `probe.shared`)

The core never branches on a harness name; it reads `Capabilities` (D23).
The third-party libraries (Pydantic AI) come from the `daemon` extra; nothing
here is imported by the CLI unless daemon mode runs.
"""
