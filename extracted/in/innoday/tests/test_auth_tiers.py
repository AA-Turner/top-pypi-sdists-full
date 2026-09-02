"""Every route sits in exactly one auth tier, and the tiers are enforced.

Tier A  public                       — no tokens
Tier B  user token                   — everything else
Tier C  user token + team secret     — org/user lifecycle only

The structural test below is the important one: it walks every route and fails if any
non-public endpoint lacks a user-auth dependency. 28 endpoints were in that state
(the shared team secret was their only gate), including
`POST /organizations/{id}/search`, which read `organization_id` straight from the path
with no membership check.
"""

import re
from pathlib import Path

import pytest

ROUTERS = Path(__file__).resolve().parents[1] / "src" / "routers"

# Names only. This list says a route *has* a gate; it cannot say the gate works --
# a `require_platform_admin` sat here for months while comparing a hardcoded literal
# to a query parameter, and this file certified every admin route as authenticated
# the whole time. It has since been deleted and the admin routes name
# `require_platform_access` directly. `test_every_auth_dep_resolves_a_real_user`
# below closes the gap by requiring each name here to reach `get_current_user`.
AUTH_DEPS = (
    "get_current_user",
    "get_authenticated_user",
    "require_platform_access",
    "get_admin_user",
    "require_org_role",
    # The /ui pages resolve identity from their session cookie rather than a
    # Depends, because a failed page auth must redirect to the sign-in page, not
    # raise a 401. It is the same credential either way -- a `cli_tokens` row,
    # looked up by the same hash -- so it is a real Tier B gate, not an exemption.
    "user_from_request",
)

# Tier A. Each either exposes no data (health/docs) or carries a stronger boundary of
# its own: the device flow's high-entropy device_code, the signed OAuth `state`, or an
# invite token whose follow-up call is Bearer-authed.
PUBLIC_ROUTES = {
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/api/v1/public/health",
    "/api/v1/public/ping",
    "/api/v1/public/status",
    "/api/v1/public/version",
    # Three integers for the product's public front page: how many projects are
    # tracked, how many releases went out, how many tickets rode them. Public of
    # necessity -- a number behind a sign-in wall is a number nobody reads -- and
    # safe because it is aggregate across every organization and carries no name,
    # alias, version or date. Anything identifying added to it makes it not
    # public, and it must move behind a token on the same commit.
    "/api/v1/public/impact",
    "/api/v1/ai/health",
    "/api/v1/platform/health",
    "/device",
    "/api/v1/device/code",
    "/api/v1/device/token",
    "/api/v1/device/approve",
    "/api/v1/boards/oauth/jira/callback",
    # Emailing an existing user a sign-in link. Unauthenticated of necessity --
    # the caller cannot sign in yet, which is the point. Its boundary is not a
    # token but the fact that it can only ever act on an address that already has
    # an InnoDay user: the address is matched against our own users table before
    # Supabase is called, so it cannot provision an identity. It is rate-limited
    # per address, answers identically for every outcome (so it is not an oracle
    # for who has an account), and returns nothing but a status. It is still
    # behind the team secret -- the Next.js UI calls it from its server.
    "/api/v1/auth/sign-in-link",
    "/invite/accept",
    "/api/v1/invite/accept",
    # Landing page for a Supabase invite / magic link. Serves HTML only; the
    # session arrives in the URL fragment, which never reaches the server. The
    # one call it makes, POST /api/v1/auth/confirm-email, is NOT public — it
    # requires a JWKS-verified Supabase JWT and is tier B. That route is exempt
    # from the *team secret* only, because a browser from an email can't send it.
    #
    # Listed under both spellings because the scanner below takes the prefix from
    # the first `APIRouter(...)` in a file, and invites.py declares two routers:
    # the /api/v1 one and an unprefixed `page_router` for browser pages. So a
    # page route gets reported with a spurious /api/v1. Same reason
    # /invite/accept appears twice above.
    "/auth/callback",
    "/api/v1/auth/callback",
    "/license-info",
    "/tiers",
    "/tiers/{tier_name}",
    # The three pre-auth steps of browser sign-in. Requiring a session to sign in
    # is a contradiction, so each carries its own boundary instead:
    #   /ui/login   sends a magic link and reveals nothing -- the response is
    #               identical for an address with an account and one without, and
    #               it is throttled per address (Supabase's mailer is capped at
    #               2/hour project-wide, so an unthrottled send is a real DoS).
    #   /ui/session accepts only a JWKS-verified Supabase JWT, the same check
    #               /api/v1/auth/confirm-email makes; an unverified one is a 401.
    #   /ui/logout  acts solely on the cookie the caller already presents, so it
    #               can end no session but the caller's own.
    # GET /ui/login is deliberately absent from this reasoning -- it resolves the
    # session to bounce an already-signed-in visitor, so it is caught as Tier B.
    "/ui/login",
    "/ui/session",
    "/ui/logout",
    # Request-for-access. Requiring a session to ask for one is circular. Its
    # boundary is the deployment's team secret, checked in the handler with
    # hmac.compare_digest -- and, crucially, treated as CLOSED when the secret is
    # unset, so a deployment without one does not silently open the page. The
    # POST creates no account: it either re-invites someone who already has one,
    # or queues a request for a platform member to decide.
    "/ui/join",
}


def _page_path_const(name: str) -> str:
    """Resolve a `src.page_paths` constant referenced in a decorator or prefix.

    `src/routers/webui/` writes both its router prefix and its route paths in
    terms of those constants rather than repeating the literals, so that a page's
    URL and the route serving it cannot drift apart (issue #414). A source
    scanner that only understands string literals would silently see none of
    those routes -- which is exactly how this file missed the whole package until
    the glob below was made recursive.
    """
    import src.page_paths as page_paths

    return str(getattr(page_paths, name, ""))


def _routes():
    """(path, method, handler-source) for every route under src/routers.

    `rglob`, not `glob`: routers may be packages (`src/routers/webui/`), and a
    top-level-only scan reports zero routes for them while still passing --
    an auth-gap test that cannot see a router is worse than no test at all.
    """
    for f in sorted(ROUTERS.rglob("*.py")):
        if f.name == "__init__.py" or "__pycache__" in f.parts:
            continue
        text = f.read_text()
        m = re.search(r"APIRouter\((.*?)\)", text, re.S)
        prefix = ""
        if m:
            pm = re.search(r'prefix\s*=\s*["\']([^"\']+)', m.group(1))
            if pm:
                prefix = pm.group(1)
            else:
                # e.g. `APIRouter(prefix=UI_PREFIX, ...)`
                pc = re.search(r"prefix\s*=\s*([A-Z_][A-Z0-9_]*)", m.group(1))
                if pc:
                    prefix = _page_path_const(pc.group(1))
        for chunk in re.split(r"(?=@(?:router|page_router)\.)", text):
            mm = re.match(
                r"@(?:router|page_router)\.(get|post|put|patch|delete)\("
                r'\s*\n?\s*["\']([^"\']*)["\']',
                chunk,
            )
            if mm:
                yield prefix + mm.group(2), mm.group(1).upper(), chunk[:2500], f.name
                continue
            # e.g. `@router.get(_route(LOGIN_PATH))` -- the constant already holds
            # the full path, so it replaces the prefix rather than appending.
            cm = re.match(
                r"@(?:router|page_router)\.(get|post|put|patch|delete)\("
                r"\s*\n?\s*_route\(([A-Z_][A-Z0-9_]*)\)",
                chunk,
            )
            if cm:
                yield (
                    _page_path_const(cm.group(2)),
                    cm.group(1).upper(),
                    chunk[:2500],
                    f.name,
                )


def test_no_route_relies_on_the_team_secret_alone():
    """Tier B/C: every non-public route must require a user token.

    The team secret is a shared deployment door key — it cannot identify a user or an
    org, so it must never be a route's only gate.
    """
    gaps = [
        f"{method} {path} ({fname})"
        for path, method, src, fname in _routes()
        if path not in PUBLIC_ROUTES and not any(d in src for d in AUTH_DEPS)
    ]
    assert gaps == [], "routes with no user-token dependency:\n  " + "\n  ".join(gaps)


def test_public_route_list_is_pinned():
    """Tier A is exemption-based, so growth must be deliberate.

    Adding a path here silently makes it reachable with no credential at all.
    """
    declared = {p for p, _, _, _ in _routes() if p in PUBLIC_ROUTES}
    # /health, /docs, /openapi.json, /redoc are served off the app, not a router.
    #
    # 16 as of #414's callback page: 15 + /auth/callback, the landing page for a
    # Supabase invite / magic link. It serves HTML only and holds no credential —
    # the session is in the URL fragment, which never reaches the server.
    #
    # 19 with browser sign-in: + /ui/login, /ui/session, /ui/logout. See the
    # justification beside each in PUBLIC_ROUTES — all three are pre-auth by
    # necessity and none of them can act on another person's session.
    #
    # 20 with /ui/join (GET and POST share the path). Gated by the deployment's
    # team secret rather than a session, because requiring a session to ask for
    # one is circular — and closed outright when no secret is configured.
    #
    # 21 with /api/v1/auth/sign-in-link, which does for the Next.js UI what
    # POST /ui/login does for the Python one: the new UI holds no database
    # connection, so it cannot check the address against our users table itself,
    # and that check is the thing standing between this route and a stranger
    # provisioning an identity. Pre-auth by necessity — the caller cannot sign in
    # yet. Same team-secret gate as /ui/join.
    #
    # 22 with /api/v1/public/impact: three aggregate integers for the product's
    # public front page. It carries no name, alias, version or date, and holds
    # nothing that could identify an organization -- which is the whole of why it
    # is allowed to be here. A field added to it that identifies anybody makes it
    # no longer a Tier A route.
    assert len(declared) == 22, sorted(declared)


def test_no_optional_user_auth_remains():
    """`get_optional_user` on a data route means "anonymous is fine" — it wasn't.

    All nine uses were `integrations/{service}/*`, which manage an org's board and
    GitHub connections.
    """
    offenders = [
        f"{method} {path} ({fname})"
        for path, method, src, fname in _routes()
        if "get_optional_user" in src
    ]
    assert offenders == [], "optional-user auth on data routes:\n  " + "\n  ".join(
        offenders
    )


TIER_C = {
    ("POST", "/api/v1/users"),
    ("DELETE", "/api/v1/users/{user_id}"),
    ("POST", "/api/v1/organizations"),
    ("DELETE", "/api/v1/organizations/{organization_id}"),
    ("DELETE", "/api/v1/admin/organizations/{organization_id}"),
    ("POST", "/api/v1/platform/setup"),
    ("POST", "/api/v1/platform/init"),
    ("POST", "/api/v1/admin/platform/setup"),
}


def test_team_secret_only_on_org_user_lifecycle():
    """Tier C is scoped by ENTITY TYPE, not by risk.

    Creating or deleting an organization or a user — never anything scoped to a
    project, repo, board or ticket, however destructive.
    """
    found = {
        (method, path)
        for path, method, src, _ in _routes()
        if "Depends(require_team_secret)" in src
    }
    assert found == TIER_C, (
        f"unexpected: {sorted(found - TIER_C)}\nmissing: {sorted(TIER_C - found)}"
    )

    for _method, path in found:
        for scoped in ("project", "repositor", "board", "ticket"):
            assert scoped not in path.lower(), (
                f"{path} is tenant-scoped; the team secret must not gate it"
            )


@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", "/api/v1/organizations/org-1/search?q=x"),
        ("POST", "/api/v1/organizations/org-1/containers/execute"),
        ("GET", "/api/v1/organizations/org-1/projects/p1/scope"),
        ("GET", "/api/v1/organizations/org-1/integrations/github/config"),
        ("GET", "/api/v1/users/some-user"),
        ("GET", "/api/v1/platform/status"),
    ],
)
def test_previously_open_routes_now_reject_anonymous(client, method, path):
    """Behavioural counterpart to the structural test above."""
    resp = client.request(method, path, json={} if method == "POST" else None)
    assert resp.status_code in (401, 403), f"{method} {path} -> {resp.status_code}"


def test_public_route_still_open(client):
    assert client.get("/api/v1/public/health").status_code == 200


def test_every_auth_dep_resolves_a_real_user():
    """A name in ``AUTH_DEPS`` must actually reach ``get_current_user``.

    The structural test above matches dependency names, so a gate that *looks*
    like auth satisfies it regardless of what it does. That is not hypothetical:
    a ``require_platform_admin`` compared a hardcoded literal against a **query
    parameter** and, on a match, returned a fabricated ``User(id="admin")`` that
    was never persisted -- and because its name was on that list, every admin
    route (including ``DELETE /admin/organizations/{id}``) was certified as
    authenticated for as long as it stood.

    Following each guard to ``get_current_user`` is the cheap structural check
    that would have caught it. A new guard that resolves identity some other
    legitimate way should be added here deliberately, not by renaming.

    The walk is transitive, because real guards delegate -- ``require_org_role``
    is a factory whose *inner* function holds the dependency, so one-level matching
    would reject that correct design while still accepting a stub that names itself
    well.
    """
    resolvers = {"get_current_user", "get_authenticated_user", "user_from_request"}
    # Guards live in both places -- rbac.py is middleware, platform.py is a router.
    search_roots = [ROUTERS, ROUTERS.parent / "middleware"]
    combined = "\n".join(
        p.read_text()
        for root in search_roots
        for p in sorted(root.rglob("*.py"))
        if "__pycache__" not in p.parts
    )

    def body_of(name):
        """Source of ``name``, from its ``def`` to the next top-level definition.

        Terminating on a `def`/`class`/decorator specifically, not on any
        column-0 character: a multi-line signature closes with `) -> X:` at
        column 0, so a looser terminator truncates the body to the signature and
        makes every guard look like it resolves nothing. End-of-file is in the
        alternation because the last function in a file has nothing after it to
        terminate on, and would otherwise read as having no body at all.
        """
        m = re.search(
            rf"^(?:async )?def {name}\(.*?(?=^(?:@|class |def |async def )|\Z)",
            combined,
            re.S | re.M,
        )
        return m.group(0) if m else None

    def reaches_a_user(name, seen):
        if name in resolvers:
            return True
        if name in seen:
            return False
        seen.add(name)
        body = body_of(name)
        if body is None:
            return False
        # Match `Depends(x)`, not a bare mention of `x`. Prose counts as source to
        # a substring search, and these guards are heavily documented -- an earlier
        # draft of this test passed a deliberately re-broken platform guard
        # purely because the docstring explaining the break named `get_current_user`.
        wired = set(re.findall(r"Depends\(\s*([A-Za-z_][A-Za-z0-9_]*)", body))
        return any(reaches_a_user(called, seen) for called in wired if called != name)

    for dep in AUTH_DEPS:
        assert body_of(dep) or dep in resolvers, (
            f"{dep} is in AUTH_DEPS but no definition was found -- a name that "
            f"matches nothing silently gates nothing."
        )
        assert reaches_a_user(dep, set()), (
            f"{dep} claims to authenticate but no chain from it reaches "
            f"{' / '.join(sorted(resolvers))}. A gate that does not identify the "
            f"caller is not a gate."
        )


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/admin/platform/info",
        "/api/v1/admin/platform/statistics",
        "/api/v1/admin/organizations",
    ],
)
def test_admin_routes_reject_the_old_hardcoded_key(client, path):
    """The stub accepted a literal from this repo's own source, passed in the URL.

    It shipped inside the PyPI wheel (``include = ["src*"]`` packages all of
    ``src/``), so "the repo is private" was never the boundary. Anonymous, wrong
    value, and the literal itself must now be equally rejected -- if the literal
    ever answers differently from the others, it is a credential again.
    """
    anonymous = client.get(path).status_code
    assert anonymous in (401, 403)
    assert client.get(f"{path}?x_api_key=admin-secret-key").status_code == anonymous
    assert client.get(f"{path}?x_api_key=whatever-else").status_code == anonymous
