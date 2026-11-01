"""parse the op folder once, quarantine what does not parse, sweep stale temps, and requeue or list dead letters."""

from __future__ import annotations

#: Dead letters status.json remembers (plan 1.7), and how much of each error.
_RECENT_DEAD_LETTERS = 32
#: Op-file bytes whose parsed ops a journal keeps between drain passes (`Journal._scan_ops`):
#: about 4,300 one-point `log()` writes. Parsed, an op takes 4-7x its file size; uncapped,
#: 20k queued one-point ops held 58 MB in a long-lived exporter on the training node, with
#: this cap 12.4 MB (5,000 twenty-point ops: 8.2 MB). Ops past it are parsed again each pass.
SCAN_CACHE_MAX_BYTES = 2 * 1024 * 1024
