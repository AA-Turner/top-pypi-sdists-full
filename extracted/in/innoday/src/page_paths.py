"""Canonical paths for the hosted browser pages -- the ``/ui`` half of the app.

The API half lives under ``/api/v1``; the server-rendered pages live under
``/ui``. Both are served by the same app, on the same host, on the same port --
the path prefix is the only thing that distinguishes them. That was the whole
point of the split: ``inno.day``'s DNS is at GoDaddy, which cannot point an apex
domain at Railway (no ``CNAME @``, no ALIAS, no CNAME flattening), so everything
consolidated onto ``www.inno.day`` and the two halves segment by path instead of
by hostname.

These are constants rather than literals because each path is constructed in
several places -- the invite email link, the device-flow ``verification_uri``,
and the Supabase ``redirect_to`` built by ``users.py``, ``bootstrap.py``, and
``scripts/backfill_supabase_identities.py`` -- and named again in
``TeamSecretMiddleware.EXEMPT_PATHS``. Literals in each would guarantee drift the
next time the prefix moves, and a drifted ``/auth/callback`` is not a visible
failure: it is an invite email that silently lands on a 404 (issue #414).

``LEGACY_REDIRECTS`` maps the pre-``/ui`` paths to their new homes. Those paths
were baked into invite emails already delivered and into Supabase's redirect
allowlist, so they must keep working; ``src/api/app.py`` serves them as 301s.
"""

UI_PREFIX = "/ui"

AUTH_CALLBACK_PATH = f"{UI_PREFIX}/auth/callback"
INVITE_ACCEPT_PATH = f"{UI_PREFIX}/invite/accept"
DEVICE_PATH = f"{UI_PREFIX}/device"

# The signed-in web surface (src/routers/webui/).
LOGIN_PATH = f"{UI_PREFIX}/login"
LOGOUT_PATH = f"{UI_PREFIX}/logout"
SESSION_PATH = f"{UI_PREFIX}/session"
# Team-secret-gated request-for-access page. Deliberately not linked from
# the sign-in card: it is for people who cannot sign in yet, and advertising
# it to everyone else only invites guesses at the secret.
JOIN_PATH = f"{UI_PREFIX}/join"

# The dashboard is ``/ui/{org_ref}`` -- a bare org alias (lowercased) or, when the
# org has no alias, its UUID. Because that segment sits directly under ``/ui``
# with no collection noun, every literal page name is also a *reserved alias*: an
# org aliased "login" would otherwise shadow the sign-in page. Two guards, both
# required -- ``src/api/app.py`` registers the literal routes before the
# parameterized one, and ``webui.routes`` refuses these segments with a 404.
RESERVED_UI_SEGMENTS = frozenset(
    {
        "login",
        "logout",
        "session",
        "join",
        "auth",
        "invite",
        "device",
        "static",
        "health",
        # "profile" is reserved even though the page itself lives one level
        # deeper, at ``/ui/{org_ref}/profile``. An org aliased "profile" would
        # not shadow that route, but it would produce ``/ui/profile/profile``
        # and an org whose every URL reads as a page name -- and the moment
        # anyone adds the obvious ``/ui/profile`` shortcut, the collision is
        # real and silent. Reserving costs one alias nobody wants.
        "profile",
        # Same argument as "profile", one level up: the project pages live at
        # ``/ui/{org}/projects/...``, so an org aliased "projects" would not
        # shadow them today -- it would produce ``/ui/projects/projects/pf``,
        # and it makes the day someone adds a ``/ui/projects`` shortcut a silent
        # collision instead of a loud one.
        "projects",
        "team",
        # Same argument again, and with the sharpest edge of the three: the
        # workflow launcher lives at ``/ui/{org}/workflow``, so an org aliased
        # "workflow" would produce ``/ui/workflow/workflow`` -- and this is the
        # page the post-sign-in redirect points at, so the day anyone adds the
        # obvious ``/ui/workflow`` shortcut the collision lands on the first
        # page every member sees rather than on a corner of the app.
        "workflow",
    }
)


def dashboard_path(org_ref: str) -> str:
    """The dashboard URL for one org, keyed by lowercased alias or UUID."""
    return f"{UI_PREFIX}/{org_ref.lower()}"


def profile_path(org_ref: str) -> str:
    """Where a person maps their board handles, for one org.

    Named here rather than built inline for the reason the module exists: the
    CLI's ``summary`` command already prints this path in two different
    messages ("map it at /ui/{org}/profile"), and a drifted page path is not a
    visible failure -- it is a printed instruction that 404s.
    """
    return f"{UI_PREFIX}/{org_ref.lower()}/profile"


def team_path(org_ref: str) -> str:
    """The org's team page: who is here, what they may do, and who is unmapped.

    Org-scoped, so it sits beside ``profile_path`` rather than under a project.
    ``OrganizationMembership`` has no project column -- a per-project team page
    would be the same list at every URL.
    """
    return f"{UI_PREFIX}/{org_ref.lower()}/team"


def workflow_path(org_ref: str) -> str:
    """The workflow launcher for one org -- pick a project, pick a workflow, go.

    Org-scoped rather than project-scoped, and that is the whole point of the
    page: the project rail *is* the picker, so a per-project URL would mean
    navigating to change the very thing the page exists to let you switch
    without navigating.

    Named here for the reason the module exists, with one call site that makes
    it acute: this is where signing in is meant to land, so the literal is
    wanted by the sign-in redirect, by the dashboard's own link back, and by
    ``RESERVED_UI_SEGMENTS`` above -- and a drifted landing path is not a
    visible failure, it is everyone's first page after sign-in 404ing.
    """
    return f"{UI_PREFIX}/{org_ref.lower()}/workflow"


def project_path(org_ref: str, project_alias: str) -> str:
    """One project's own page, keyed by its alias rather than its UUID.

    The alias, because it is what people say out loud and what the ticket prefix
    already uses -- and it is unambiguous here: ``Project.alias`` is unique
    *per organization* (``uq_project_org_alias``), and the org is the segment
    above it. ``Organization.alias`` is the globally-unique one.

    Lowercased for the same reason ``dashboard_path`` lowercases the org: aliases
    are stored uppercase because they are ticket prefixes, and a URL that changes
    case depending on which side built it is a URL that fails to match.
    """
    return f"{UI_PREFIX}/{org_ref.lower()}/projects/{project_alias.lower()}"


def new_project_path(org_ref: str) -> str:
    """The create-a-project form for one org.

    ``new`` sits where a project alias would, so it is a **reserved project
    alias** in the same way the literals above are reserved org aliases -- a
    project aliased "new" would shadow this form. Enforced by the create route,
    which refuses it, rather than by another module-level frozenset: the
    collision is one word and one call site, and a set of one is a set that
    drifts out of use.
    """
    return f"{UI_PREFIX}/{org_ref.lower()}/projects/new"


# Where the pages lived before the /ui prefix. Still routed, as 301s.
LEGACY_AUTH_CALLBACK_PATH = "/auth/callback"
LEGACY_INVITE_ACCEPT_PATH = "/invite/accept"
LEGACY_DEVICE_PATH = "/device"

LEGACY_REDIRECTS = {
    LEGACY_AUTH_CALLBACK_PATH: AUTH_CALLBACK_PATH,
    LEGACY_INVITE_ACCEPT_PATH: INVITE_ACCEPT_PATH,
    LEGACY_DEVICE_PATH: DEVICE_PATH,
}

# Exempt from the team-secret gate: a browser cannot send that header, and the 301
# would otherwise 401 before routing. ``UI_PREFIX`` is exempted as a *prefix*
# rather than a path list because ``/ui/{org_ref}`` cannot be enumerated -- the
# segment is an org alias. The pages' real boundary is the session cookie
# (``webui.session``), exactly as the device page's is its high-entropy code.
#
# Note the consequence: ``POST /ui/login`` is publicly reachable on a gated
# deployment, and it sends email. Supabase's built-in sender is capped at 2/hour
# project-wide, so ``webui.routes`` throttles per address to keep a stranger from
# burning the org's entire quota. That throttle is in-process, so it is per worker.
UI_PAGE_PATHS = frozenset(LEGACY_REDIRECTS.values())
LEGACY_PAGE_PATHS = frozenset(LEGACY_REDIRECTS)
