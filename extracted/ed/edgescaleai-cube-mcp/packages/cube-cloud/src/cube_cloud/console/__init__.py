"""The cube-cloud console: a browser UI for cube access.

See `docs/console-spec.md`. Everything the console serves — the SPA shell and its
JSON API — lives under the single reserved apex prefix
`auth/session_cookie.CONSOLE_PREFIX` (`/console`), which is also the one entry in
`auth/middleware.APIKeyMiddleware.COOKIE_ALLOWED_APEX_PREFIXES`.

Two rules govern this package and are load-bearing, not stylistic:

1. **No generic tool proxy** (spec §4.3). There must never be an endpoint that
   accepts a tool name and forwards it. That would recreate the `/mcp` surface —
   generic and mutating — under cookie auth, which is exactly what the CSRF rule
   in `browser-app-proxy-spec.md` §4.2 exists to prevent. Every capability is its
   own route with its own enumerated, validated arguments.

2. **Secrets are excluded structurally, not redacted** (spec §4.4). `reads.py`
   must never select Apollo's `declaredState` and must never emit a config field;
   entity config overrides carry cleartext deployment secrets. The response
   serializer is an explicit field allowlist so a future Apollo field that starts
   carrying a secret cannot leak through it.
"""
