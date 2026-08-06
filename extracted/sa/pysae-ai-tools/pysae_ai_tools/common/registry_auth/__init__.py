"""GitLab registry credential: resolution targets, PAT lifecycle, per-ecosystem writers.

The socle every command group may import (see CLAUDE.md § Layering). It owns
three concerns and nothing else:

- :mod:`targets` — where the credential applies (GitLab host, owner/scope),
  derived from the repo identity rather than hardcoded.
- :mod:`pat` — the token's own lifecycle: expiry read from GitLab, rotation
  under a threshold, and the pre-filled creation URL shown on a miss.
- :mod:`npm`, :mod:`docker`, :mod:`uv` — one writer per ecosystem, each able to
  report its state, apply a token, and remove what it wrote.

Resolution of the token *value* (environment, on-disk cache, interactive
prompt) is deliberately absent: it belongs to the ``env`` group, which this
layer cannot import. The wiring lives in
:mod:`pysae_ai_tools.install.registry_credential`.
"""
