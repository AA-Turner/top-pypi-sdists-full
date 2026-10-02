"""Canonical home of the tap's transcript data contract.

The probe-research-tap plugin ships sanitized per-session transcripts to the
Research OS knowledgebase. The backfill CLI ships *historical* transcripts
through the same ingest door, and the two paths must produce identical wire
shapes — same sanitizer, same batch chunking, same byte-cursor discipline —
or the same session recorded twice tells two different stories.

The tap is a separate distribution living in the agent's plugin cache: the CLI
cannot import it, and the plugin cannot import probe. So the shared modules
live here canonically and are VENDORED into the plugin, byte-identical, by
`make sync-tap-core`:

    sanitize.py        Claude Code event sanitizer
    codex_sanitize.py  Codex rollout -> CC-shape translator
    pi_sanitize.py     pi session JSONL -> CC-shape translator
    transcript.py      JSONL tail/split/validate + batch chunking + byte cursor

tests/test_tap_core_sync.py fails when the copies drift. Edit the canonical
files here, never the plugin copies. Cross-module imports inside these files
must stay RELATIVE (`from .sanitize import ...`) so the same bytes resolve in
both packages. Same contract as sync-plugin-policy / sync-telemetry-core /
sync-session-marker, with the canonical direction unchanged: canonical in
src/probe, copy in the plugin.
"""
