"""Size limits on Probe's own uploads (daemon pre-check, output capture)."""

from __future__ import annotations

#: Most an AUTOMATIC upload sends (daemon uploads, output capture at run close;
#: Richard 2026-10-12). Past the credential gate's 64 MiB inspection limit it goes
#: in parts. An explicit `log_artifact` is bounded by the server alone.
AUTO_UPLOAD_MAX_BYTES = 5 * 1024**3

#: Prefix of a big file scanned for credentials locally; equals the server's
#: `app/artifacts/multipart.py` INSPECT_PREFIX_BYTES (a test keeps them equal).
#: A 64 MiB scan took 35 s on the devbox, 16 MiB 9 s.
SCAN_PREFIX_BYTES = 16 * 1024 * 1024
