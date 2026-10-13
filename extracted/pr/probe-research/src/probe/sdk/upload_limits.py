"""Size limits on uploads Probe makes on its own, shared by the daemon's
pre-check and output capture."""

from __future__ import annotations

#: The most an AUTOMATIC upload sends: a file the Probe daemon uploads, and a
#: file output capture keeps at a run's close (Richard, 2026-10-12: "more like
#: 5 gb"). Past the credential gate's inspection limit (64 MiB) the bytes go in
#: parts. An explicit `log_artifact` is bounded by the server alone.
AUTO_UPLOAD_MAX_BYTES = 5 * 1024**3

#: How much of a big file is scanned for credentials on this machine before it
#: is sent: the prefix the server's multipart verifier inspects too
#: (`app/artifacts/multipart.py` INSPECT_PREFIX_BYTES; a test keeps them equal).
#: A 64 MiB text scan took 35 s on the devbox, 16 MiB 9 s.
SCAN_PREFIX_BYTES = 16 * 1024 * 1024
