"""
Middleware package for InnoDay platform.

Cross-cutting request/response concerns. The auth-related pieces live in
``token_auth`` (credential -> User) and ``rbac`` (User -> permission); the
deployment door key is ``src/api/middleware/team_secret``.

``license_middleware`` was removed: it was never registered on the app, it read
the retired ``X-User-ID`` header (so its user id would always have been None),
and it duplicated licence/usage accounting that the routers already do correctly
with the real authenticated user via ``src/utils/license_utils.track_usage``.
"""
