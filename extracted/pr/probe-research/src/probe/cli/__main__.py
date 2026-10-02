"""`python -m probe.cli`: the daemon's fallback when no `probe` sits beside its
interpreter (`probe.daemon.tools.probe_executable`)."""

from probe.cli import main

raise SystemExit(main())
