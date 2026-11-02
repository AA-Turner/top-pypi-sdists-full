"""Browser app proxy (spec: docs/browser-app-proxy-spec.md).

Phase 2a: a real HTTP reverse proxy from an app-subdomain host to the
matching Teleport app, dialed server-side via tbot. Phase 2b adds scoped
authorization on top. WebSocket support is Phase 3 (not here).
"""
