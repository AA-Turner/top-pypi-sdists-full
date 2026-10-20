"""The Probe service: one on-demand process per user per machine.

Started by the first agent session that needs it (`client.ensure`), never at
login; exits a few seconds after the last live session and the last open app
window are gone. API v1 is pinned in `protocol.py`; the lifecycle and the
registry are `server.py` and `registry.py`; `client.py` is the stdlib-only
connector the tap and pi carry as byte-identical copies.

Nothing is imported here: `python -m probe.service` must start on the standard
library alone (plan S1).
"""
