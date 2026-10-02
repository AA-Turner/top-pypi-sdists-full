"""The Probe daemon, version 2: one program that records a coding session in Probe.

Two processes per session. Capture (the stdlib `tap`, today's `tap watch`) ships
the transcript and supervises the AI process; this package is the AI process.
It reads the harness's chat log into a queue the moment lines land, thinks in
bites (your prompt, the agent's turn end, a size limit, anything ~2 minutes
old), and records with the same `probe` CLI the coding agent uses, each command
checked in plain code before it runs (`precheck`).

    adapters/   one per harness: chat log -> normalized events (`events.Event`)
    store       the session's scrubbed event store, queue watermark, logbook
    bite        what one model call sees, in cache order
    shell       the daemon's shell: safe commands run, the rest ask the researcher
    precheck    the checks before a `probe` command runs
    approvals   one shared way to ask the researcher (policies)
    worker      the loop

The core never branches on a harness name; it reads `Capabilities` (D23).
The third-party libraries (Pydantic AI) come from the `daemon` extra; nothing
here is imported by the CLI unless daemon mode runs.
"""
