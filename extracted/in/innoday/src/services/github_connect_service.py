"""
GitHub Connection Service for Organization-Scoped Repository Management

Handles GitHub organization connections, repository discovery, and layer detection
for the organization-centric architecture.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from sqlmodel import Session, select

from src.api.github_api import GitHubAPI, GitHubAPIError
from src.domain.organization import Organization
from src.domain.project import (
    Project,
    ProjectRepository,
    RepositoryLayer,
)
from src.domain.project_timeline import TimelineEventType
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import (
    GitHubOrgRegistration,
    GitHubSyncHistory,
    Repository,
)
from src.services.org_credential_service import (
    GITHUB_INTEGRATION,
    get_github_credentials,
    mark_org_credential_validated,
    set_github_credentials,
)
from src.services.project_timeline_writer import add_timeline_entry
from src.services.release_planning import (
    ensure_pipeline,
    reconcile_statuses,
)
from src.services.workspace_onboard import WorkspaceOnboardService

logger = logging.getLogger(__name__)

# Mass-deactivation guard (see sync_project_repositories).
#
# Both thresholds have to be met, and each rules out a different false positive.
# The fraction alone would refuse a two-repo project that legitimately retired
# one; the floor alone would allow a 40-repo project to lose 39. Together they
# target the shape a misconfiguration actually makes: a project with several repos
# losing nearly all of them at once.
#
# 0.5 rather than something stricter because the failure being caught is total --
# a wrong GitHub org discovers *nothing*, so it retires 100% of what it can see.
# Anything at or above half is already far outside normal re-tagging.
_MASS_DEACTIVATION_MIN_ACTIVE = 3
_MASS_DEACTIVATION_THRESHOLD = 0.5

#: What the dashboard is told when the sync died of something nobody wrote a
#: message for. See `_reportable_sync_error`.
_UNEXPECTED_SYNC_ERROR = "The sync failed unexpectedly — check the server logs"


def _reportable_sync_error(exc: BaseException) -> str:
    """The message a failed sync may persist, which is not the same as `str(exc)`.

    Whatever lands in `Project.github_error_message` is rendered in the GitHub
    icon's tooltip to **every member of the org**, so it is a user-facing string,
    not a debugging aid. Escaping is already handled (`_integration_icon` puts the
    title through `esc()`), so the risk here is disclosure and misdirection rather
    than injection:

    - `IntegrityError` stringifies to the full SQL plus its bound parameters
    - `OperationalError` to psycopg2 connection detail -- host, port, user, and
      connection strings must never reach output
    - `TypeError` to "'NoneType' object has no attribute 'name'", which reads as
      "GitHub is broken" when the truth is that we are

    So only the exceptions raised *to be read* pass through verbatim: `ValueError`,
    which is what the credential, refusal and discovery paths deliberately raise
    with a written-for-humans message, and `GitHubAPIError`, which carries GitHub's
    own. Everything else is generic here and logged in full at the point of record,
    where the detail belongs.

    **`ValueError` exactly, not any subclass**, because "is a ValueError" is not
    "was written for a reader" once inheritance is involved. `pydantic`'s
    `ValidationError` subclasses `ValueError` and stringifies to the *input value*
    that failed validation -- so a model fed a credential reports it. `json`'s
    `JSONDecodeError` and `UnicodeDecodeError` are `ValueError`s too, and both
    describe a payload we were parsing rather than anything the reader can act on.
    Every one of those is the same disclosure as the `IntegrityError` above,
    wearing the type this function trusts.
    """
    if isinstance(exc, GitHubAPIError) or type(exc) is ValueError:
        return str(exc)
    return _UNEXPECTED_SYNC_ERROR


# ── Repository-layer detection tables ────────────────────────────────────────
#
# These replace a ~190-line if/elif chain. The precedence they encode is
# unchanged: an explicit `layer:` topic wins, then a name pattern (checked
# most-specific-layer first), then the primary language.

# `layer:<keyword>` GitHub **topic** → layer. Matched exactly, after stripping.
# Named for topics, not labels: a label in this platform is a *board* label on a
# ticket, and calling a repository topic one is how the two got confused.
#: Prefixes that mark a topic as an explicit layer declaration.
#:
#: **``layer-`` is the one that works.** The original marker was ``layer:``, and
#: a GitHub topic cannot contain a colon -- the API rejects it with "must start
#: with a lowercase letter or number, consist of 50 characters or less, and can
#: include hyphens". So that branch could never fire on a real repository, and
#: went unnoticed because nothing failed: a repo simply fell through to the
#: name and language rules, which usually produce something plausible.
#:
#: ``layer:`` is kept because it costs one comparison and a repository could
#: carry it from some other source (a description convention, an import), but
#: the hyphen form is the one to document and the one to set.
_LAYER_TOPIC_MARKERS = ("layer-", "layer:")

_TOPIC_KEYWORD_LAYERS: Dict[str, RepositoryLayer] = {
    "ui": RepositoryLayer.UI,
    "frontend": RepositoryLayer.UI,
    "front-end": RepositoryLayer.UI,
    "web": RepositoryLayer.UI,
    "api": RepositoryLayer.API,
    "backend": RepositoryLayer.API,
    "server": RepositoryLayer.API,
    "service": RepositoryLayer.API,
    "data": RepositoryLayer.DATA,
    "database": RepositoryLayer.DATA,
    "db": RepositoryLayer.DATA,
    "etl": RepositoryLayer.DATA,
    "pipeline": RepositoryLayer.DATA,
    "ai": RepositoryLayer.AI,
    "ml": RepositoryLayer.AI,
    "machine-learning": RepositoryLayer.AI,
    "model": RepositoryLayer.AI,
    "legacy": RepositoryLayer.LEGACY,
    "old": RepositoryLayer.LEGACY,
    "deprecated": RepositoryLayer.LEGACY,
    # DESIGN is reachable by an explicit `layer:design` topic and by nothing
    # else. There is deliberately no name pattern for it below: the obvious
    # candidates -- "demo", "design", "prototype" -- appear in the names of real
    # shipping repositories, and a heuristic that reclassified one of those
    # would move its work out of the release story silently. Saying so on the
    # repository is cheap; guessing wrong is not.
    "design": RepositoryLayer.DESIGN,
    "demo": RepositoryLayer.DESIGN,
    "prototype": RepositoryLayer.DESIGN,
}

# Name patterns, in precedence order: most specific layer first, so that
# "legacy-ml-api" resolves to LEGACY rather than AI or API. Regexes (word
# boundaries matter) -- unlike the language hints below, which are substrings.
_NAME_PATTERN_LAYERS: Tuple[Tuple[RepositoryLayer, "re.Pattern[str]"], ...] = tuple(
    (layer, re.compile("|".join(patterns)))
    for layer, patterns in (
        (
            RepositoryLayer.LEGACY,
            (
                r"-legacy\b",
                r"-old\b",
                r"-deprecated\b",
                r"-archive\b",
                r"^legacy-",
                r"^old-",
                r"^deprecated-",
                r"^archive-",
            ),
        ),
        (
            RepositoryLayer.AI,
            (
                r"-ai\b",
                r"-ml\b",
                r"-model\b",
                r"-analytics\b",
                r"-intelligence\b",
                r"^ai-",
                r"^ml-",
                r"^model-",
                r"^analytics-",
                r"-prediction",
                r"-recommender\b",
                r"-nlp\b",
                r"prediction-",
                r"recommender-",
            ),
        ),
        (
            RepositoryLayer.DATA,
            (
                r"-db\b",
                r"-database\b",
                r"-data\b",
                r"-etl\b",
                r"-pipeline\b",
                r"^db-",
                r"^database-",
                r"^data-",
                r"^etl-",
                r"-migrations?\b",
                r"-warehouse\b",
                r"-lake\b",
            ),
        ),
        (
            RepositoryLayer.UI,
            (
                r"-ui\b",
                r"-frontend\b",
                r"-web\b",
                r"-app\b",
                r"-client\b",
                r"^ui-",
                r"^frontend-",
                r"^web-",
                r"^client-",
                r"-portal\b",
                r"-dashboard\b",
                r"-console\b",
            ),
        ),
        (
            RepositoryLayer.API,
            (
                r"-api\b",
                r"-backend\b",
                r"-server\b",
                r"-service\b",
                r"-gateway\b",
                r"^api-",
                r"^backend-",
                r"^server-",
                r"^service-",
                r"-rest\b",
                r"-graphql\b",
                r"-grpc\b",
            ),
        ),
    )
)

# Primary language → layer, with optional name-substring overrides applied first.
# A Node backend is TypeScript but belongs in API, so the hints get a say before
# the language default. Substring matches (NOT word-boundary), preserving the
# original behaviour.
_LANGUAGE_LAYERS: Tuple[
    Tuple[
        Tuple[str, ...],
        RepositoryLayer,
        Tuple[Tuple[RepositoryLayer, Tuple[str, ...]], ...],
    ],
    ...,
] = (
    (
        ("javascript", "typescript", "jsx", "tsx", "vue", "svelte"),
        RepositoryLayer.UI,
        ((RepositoryLayer.API, ("api", "backend", "server", "service")),),
    ),
    (("html", "css", "scss", "sass", "less"), RepositoryLayer.UI, ()),
    (
        ("python", "java", "go", "rust", "c#", "ruby", "php"),
        RepositoryLayer.API,
        (
            (RepositoryLayer.UI, ("ui", "frontend", "web", "client")),
            (RepositoryLayer.DATA, ("data", "etl", "pipeline", "db")),
            (RepositoryLayer.AI, ("ai", "ml", "model", "analytics")),
        ),
    ),
    (("sql", "plpgsql", "tsql"), RepositoryLayer.DATA, ()),
    (("jupyter notebook", "r", "matlab"), RepositoryLayer.AI, ()),
)


def _parse_github_time(value):
    """GitHub's ISO-8601 `...Z` into an aware datetime, or None.

    `Z` is valid ISO-8601 but `fromisoformat` only learned it in 3.11, and this
    runs against 3.12+ -- the replace is belt and braces for a value that comes
    from someone else's API and is not worth an exception on a sync path.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _undetermined_result(
    result: Dict[str, Any],
    org_alias: str,
    question: str,
    cause: str,
) -> Dict[str, Any]:
    """Record "GitHub did not answer" on a validation result -- **not** a failure.

    ``valid`` becomes None rather than False: nothing was proved about the
    credential, and a diagnostic endpoint that answers "your token is bad"
    because GitHub returned 429 is worse than one that admits it does not know.

    ``cause`` must be a value *this module composed* -- an HTTP status, or an
    exception's class name. Never ``str(exception)`` and never a GitHub response
    body, on any path, which is the whole reason this helper exists rather than
    an f-string at each call site:

    * An outbound HTTP exception's message can quote the request. A stored token
      carrying a stray newline makes httpx/h11 raise ``LocalProtocolError:
      Illegal header value b'Bearer ghp_...'`` -- the credential, in the message,
      returned in a 200 body and written to the log.
    * Scrubbing the token out of that one string would only cover the exception
      we happened to find. Excluding exception text entirely covers every
      exception type, including ones added by a future httpx.

    A class name and a status code are enough to act on ("ConnectError, so check
    egress"; "HTTP 429, so retry") and cannot carry a secret.
    """
    logger.warning(
        "GitHub did not answer %s for org %s (%s)", question, org_alias, cause
    )
    result["valid"] = None
    result["error"] = (
        f"GitHub did not answer {question} ({cause}), so it is undetermined. "
        "This is not a verdict on the stored credential."
    )
    return result


class GitHubConnectService:
    """Service for managing GitHub connections at the organization level."""

    def __init__(self, session: Session):
        self.session = session

    def _get_github_credentials(self, org: Organization) -> Optional[Dict[str, str]]:
        """GitHub credentials for an org, from Supabase Vault. The only source.

        Deliberately has no local-config/OS-keyring fallback. The class that used
        to provide one, `CredentialProvider`, read ~/.innoday/config.json + the OS
        keyring, which exist only on a developer's machine: on the deployed server
        it returned None *silently*, so a "fallback" never yielded a credential in
        production — it only made local and deployed behaviour diverge and turned
        a misconfiguration into an empty result. Reading one store here and another
        elsewhere is exactly what let the same org look connected on one endpoint
        and unconnected on another. It was deleted in #525 phase 5; this docstring
        is why nothing like it should come back.

        Returns None when nothing is stored; callers surface "connect GitHub
        first" rather than guessing.
        """
        creds = get_github_credentials(self.session, org.id)
        if not creds:
            return None

        # github_org is public config, not a secret: prefer the org's explicit
        # setting so it stays editable without a Vault write.
        explicit_org = (org.settings or {}).get("github_org")
        if explicit_org:
            creds = {**creds, "github_org": explicit_org}
        elif not creds.get("github_org"):
            logger.warning(
                "Vault GitHub credential for org=%s has no github_org; "
                "set organizations.settings->>'github_org'",
                org.alias,
            )
        return creds

    async def connect_github_organization(
        self,
        organization_id: str,
        github_org: str,
        github_token: str,
        user_id: Optional[str] = None,
        force: bool = False,
    ) -> Dict:
        """
        Connect a GitHub organization to an InnoDay organization.

        One InnoDay organization may have at most one connected GitHub
        organization at a time (enforced here at the application level, not
        the DB level -- see the migration/plan notes for why). Reconnecting
        with the *same* github_org is always allowed (token refresh). Passing
        a *different* github_org requires force=True, since it silently
        changes which repos every project's topic-based discovery searches.

        Args:
            organization_id: InnoDay organization ID
            github_org: GitHub organization name
            github_token: GitHub personal access token
            force: allow switching to a different GitHub org than the one
                currently connected

        Returns:
            Connection details including discovered repository count
        """
        # Verify organization exists
        org = self.session.get(Organization, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        existing_creds = self._get_github_credentials(org)
        if (
            existing_creds
            and existing_creds.get("github_org")
            and existing_creds["github_org"] != github_org
            and not force
        ):
            raise ValueError(
                f"Organization '{org.alias}' is already connected to GitHub "
                f"org '{existing_creds['github_org']}'. Pass force=True to "
                f"switch to '{github_org}' instead."
            )

        # Validate GitHub token and org access
        github_api = GitHubAPI(github_token)

        try:
            # Validate token
            user_info = await github_api.validate_token()
            logger.info(f"GitHub token validated for user: {user_info.get('login')}")

            # Check organization access
            if not await github_api.validate_organization_access(github_org):
                raise ValueError(f"No access to GitHub organization: {github_org}")

        except Exception as e:
            logger.error(f"GitHub validation failed: {str(e)}")
            raise ValueError(f"GitHub validation failed: {str(e)}")

        # Generate connection ID for tracking
        connection_id = f"github_{organization_id}_{github_org}"

        # Store the token in Supabase Vault — the server-side source of truth,
        # readable by the deployed API (unlike the local keyring). The token
        # itself never lands on org_credentials or in a log; only the
        # vault_secret_id pointer is persisted.
        logger.info(f"Storing GitHub credentials in Vault for org alias: {org.alias}")
        set_github_credentials(
            self.session,
            org.id,
            token=github_token,
            github_org=github_org,
            rotated_by_user_id=user_id,
        )

        # Keep github_org discoverable as public config so topic discovery and
        # the access map can read it without touching Vault.
        settings = dict(org.settings or {})
        if settings.get("github_org") != github_org:
            settings["github_org"] = github_org
            org.settings = settings
            self.session.add(org)
            self.session.commit()

        test_creds = get_github_credentials(self.session, org.id)
        if test_creds and test_creds.get("token"):
            # This is the point at which all three things are true: the token
            # was checked against the live GitHub API above, it is stored, and
            # it reads back. Stamp the audit column here rather than inside
            # set_github_credentials -- see mark_org_credential_validated's
            # docstring for why storing must not imply validating.
            mark_org_credential_validated(self.session, org.id, GITHUB_INTEGRATION)
            logger.info(
                f"GitHub connection established for {github_org} "
                f"(org.alias={org.alias}, connection_id={connection_id})"
            )
        else:
            # A write that doesn't read back means Vault is misconfigured; fail
            # loudly rather than leaving a connection that silently can't auth.
            raise ValueError(
                "GitHub credentials were written but could not be read back from "
                "Vault — check the supabase_vault extension and the "
                "get_org_credential/set_org_credential functions."
            )

        # Get repository count for the organization
        try:
            repos = await github_api.get_all_organization_repositories(github_org)
            repo_count = len(repos)
        except Exception as e:
            logger.warning(f"Could not fetch repository count: {str(e)}")
            repo_count = 0

        # Upsert the DB-level registration record (BUG 1 fix: this used to be
        # skipped entirely, and the separate /integrations/github/connect
        # endpoint created a GitHubOrgRegistration row without ever storing a
        # usable token -- the two halves of "connect GitHub" never talked to
        # each other). One row per organization_id, since one org connects to
        # at most one GitHub org at a time.
        registration = self.session.exec(
            select(GitHubOrgRegistration).where(
                GitHubOrgRegistration.organization_id == organization_id
            )
        ).first()
        if registration:
            registration.organization = github_org
            registration.status = "active"
            registration.last_error = None
            registration.total_repos_count = repo_count
            self.session.add(registration)
            self.session.commit()
        elif user_id:
            # GitHubOrgRegistration.user_id is a required FK to users.id --
            # only create the row when we actually have a user to attribute
            # it to. Credentials are already stored above regardless, so a
            # missing user_id here just means discovery/sync still works,
            # it only skips the DB-level registration bookkeeping.
            registration = GitHubOrgRegistration(
                id=str(uuid4()),
                user_id=user_id,
                organization_id=organization_id,
                organization=github_org,
                status="active",
                total_repos_count=repo_count,
            )
            self.session.add(registration)
            self.session.commit()
        else:
            logger.warning(
                f"No user_id provided for GitHub connect on org {organization_id} -- "
                "credentials stored, but skipping GitHubOrgRegistration row "
                "(user_id is a required field)."
            )

        return {
            "connection_id": connection_id,
            "organization_id": organization_id,
            "github_org": github_org,
            "status": "connected",
            "total_repos_discovered": repo_count,
            "connected_at": datetime.now(timezone.utc).isoformat(),
        }

    async def validate_stored_github_credential(
        self, organization_id: str
    ) -> Dict[str, Any]:
        """Re-check the GitHub credential an organization has **already stored**.

        Runs the same two checks ``connect_github_organization`` runs --
        ``validate_token`` then ``validate_organization_access`` -- against the
        token in Vault, so the caller does not have to still possess it. The
        only way to revalidate before this existed was to re-submit the token
        through ``/integrations/github/connect``.

        Stamps ``last_validated_at`` on success, and only on success.

        A stored-but-rejected token is a **result, not an exception**: it comes
        back as ``valid: False`` with a reason. That is the case an expired dev
        token produced, where onboarding/resolve returned 500 and repository
        discovery returned ``[]`` -- neither of which said "the token expired".

        ``valid`` is deliberately **three-valued**, because there are three
        answers and only two of them are verdicts:

        ==========  ==========================================================
        ``True``    checked, and it works
        ``False``   GitHub answered *no* (401/403 on the token; 401/403/404 on
                    the org)
        ``None``    **not determined** -- GitHub was unreachable, throttled or
                    5xx-ing, so nothing was proved either way
        ==========  ==========================================================

        The third row is the point. Mapping an unanswered check to ``False``
        makes a diagnostic endpoint say "your token lost access" when GitHub
        merely rate-limited us, and an ADMIN will act on that. ``org_access``
        is likewise ``None`` for "not determined", which covers both "no
        GitHub org is configured" and "the access check did not complete" --
        ``error`` says which.

        Raises:
            ValueError: when the organization does not exist, or has no stored
                GitHub credential at all. Nothing was validated and nothing
                failed validation; there is simply nothing to check.
            VaultUnavailableError: propagated from the credential read on
                Postgres when the Vault wrapper cannot be called (the route
                turns it into a 503).

        The token itself is never returned or logged -- see
        ``_undetermined_result`` for why no exception message or GitHub
        response body is ever composed into the result either. ``github_login``
        is the *account* the token belongs to (GitHub's own answer to "whose
        token is this?"), which is what makes the result actionable, and is not
        a secret.
        """
        org = self.session.get(Organization, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        creds = self._get_github_credentials(org)
        token = (creds or {}).get("token")
        if not token:
            raise ValueError(
                f"Organization '{org.alias}' has no stored GitHub credential to "
                "validate. Connect GitHub first."
            )

        # _get_github_credentials has already resolved this, preferring the
        # public organizations.settings copy over the one in the Vault payload.
        github_org = creds.get("github_org")

        result: Dict[str, Any] = {
            "service": GITHUB_INTEGRATION,
            "valid": False,
            "github_org": github_org,
            "github_login": None,
            "org_access": None,
            "last_validated_at": None,
            "error": None,
        }

        github_api = GitHubAPI(token)
        token_question = "whether the stored token still works"

        # Both live checks are exception-handled, and that is the fix rather
        # than an accident of layout: the org check below used to sit outside
        # any try, so a ConnectError there escaped as a bare 500 -- no exception
        # handlers are registered on this app -- one line after an identical
        # failure that came back as a graceful 200. Two `try`s rather than one
        # so each can name the question it failed to answer.
        try:
            token_status, user_info = await github_api.probe_token()
        except Exception as e:
            return _undetermined_result(
                result, org.alias, token_question, type(e).__name__
            )

        if token_status in (401, 403):
            # GitHub answered, and the answer is no. This is a verdict.
            logger.warning(
                "stored GitHub token rejected for org %s (HTTP %s)",
                org.alias,
                token_status,
            )
            result["error"] = f"GitHub rejected the stored token (HTTP {token_status})."
            return result
        if token_status != 200:
            # 429, 5xx, anything else: GitHub did not answer the question.
            return _undetermined_result(
                result, org.alias, token_question, f"HTTP {token_status}"
            )

        result["github_login"] = (user_info or {}).get("login")

        if github_org:
            org_question = (
                f"whether the stored token can reach GitHub organization '{github_org}'"
            )
            try:
                org_status = await github_api.organization_access_status(github_org)
            except Exception as e:
                return _undetermined_result(
                    result, org.alias, org_question, type(e).__name__
                )

            if org_status in (401, 403, 404):
                result["org_access"] = False
                result["error"] = (
                    "The stored token is valid but has no access to GitHub "
                    f"organization '{github_org}' (HTTP {org_status})."
                )
                return result
            if org_status != 200:
                return _undetermined_result(
                    result, org.alias, org_question, f"HTTP {org_status}"
                )
            result["org_access"] = True

        result["valid"] = True
        result["last_validated_at"] = mark_org_credential_validated(
            self.session, org.id, GITHUB_INTEGRATION
        )
        return result

    def detect_repository_layer(
        self,
        repo_name: str,
        primary_language: Optional[str] = None,
        topics: List[str] = None,
    ) -> RepositoryLayer:
        """Detect a repository's architectural layer.

        ``topics`` was called ``github_labels`` and never held labels: both call
        sites pass a variable literally named ``topics``, and it looks for a
        ``layer:`` marker among a repository's GitHub **topics**. GitHub labels
        are a different thing entirely (they live on issues and pull requests),
        and the platform reserves "label" for a *board* label on a ticket -- one
        of which, being semver-shaped, becomes that ticket's release. Topics
        match repositories; labels annotate tickets.

        Precedence, highest first:
          1. an explicit ``layer-<keyword>`` GitHub topic
          2. a repository-name pattern (most specific layer first, so
             "legacy-ml-api" is LEGACY, not AI or API)
          3. the primary language, with name hints allowed to override it
             (a Node backend is TypeScript but belongs in API)
          4. UNASSIGNED

        The rules live in the three tables above rather than in a branch chain;
        adding a keyword or language is a one-line edit there.
        """
        name = repo_name.lower()

        for topic in topics or []:
            topic_lower = topic.lower()
            for marker in _LAYER_TOPIC_MARKERS:
                if not topic_lower.startswith(marker):
                    continue
                keyword = topic_lower[len(marker) :].strip()
                if keyword in _TOPIC_KEYWORD_LAYERS:
                    return _TOPIC_KEYWORD_LAYERS[keyword]

        for layer, pattern in _NAME_PATTERN_LAYERS:
            if pattern.search(name):
                return layer

        if primary_language:
            language = primary_language.lower()
            for languages, default_layer, hints in _LANGUAGE_LAYERS:
                if language not in languages:
                    continue
                for hint_layer, substrings in hints:
                    if any(s in name for s in substrings):
                        return hint_layer
                return default_layer

        return RepositoryLayer.UNASSIGNED

    async def discover_project_repositories(
        self,
        organization_id: str,
        project_id: str,
        github_label: str,
        connection_id: Optional[str] = None,
    ) -> Dict:
        """
        Discover GitHub repositories for a project based on labels/topics.

        Args:
            organization_id: InnoDay organization ID
            project_id: Project ID to discover repos for
            github_label: GitHub topic/label to search for (e.g., "acme")
            connection_id: Optional specific connection to use

        Returns:
            Dictionary with discovered repositories and their detected layers
        """
        # Get organization and credentials
        org = self.session.get(Organization, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        # Get project
        project = self.session.get(Project, project_id)
        if not project or project.organization_id != organization_id:
            raise ValueError(f"Project {project_id} not found in organization")

        # Get GitHub credentials
        logger.info(f"Looking for GitHub credentials for org alias: {org.alias}")
        creds = self._get_github_credentials(org)
        if not creds:
            logger.warning(
                f"No GitHub credentials found for organization alias: {org.alias}"
            )
            raise ValueError("No GitHub connection found for organization")

        github_token = creds["token"]

        # Resolve the GitHub org through the same shared, PROJECT-AWARE resolver
        # the topics go through below. `creds["github_org"]` is org-wide -- it
        # comes from `settings['github_org']`, which has no project context and so
        # cannot see a `settings['github_orgs']` per-project override.
        #
        # That asymmetry caused a real incident. BPAI moved to the `bp` org while
        # its repos stayed in `havilandsoftware`, recorded as
        # `github_orgs: {"BPAI": "havilandsoftware"}`. Discovery honoured the
        # override; THIS path did not, and searched `bp`'s org-wide
        # `BrightPowerSoftware` instead. Nine repos were not found there, so the
        # sync concluded they had lost their topic and deactivated all nine -- and
        # attached three BrightPowerSoftware repos that were not BPAI's.
        #
        # Note what that looked like: not an error, but "9 repositories lost the
        # topic label", which reads as a change someone made on GitHub. Resolving
        # the wrong org is indistinguishable from a legitimate re-tagging unless
        # the org is resolved the same way everywhere. Hence one resolver, not two.
        onboard = WorkspaceOnboardService(self.session)
        github_org = onboard.github_org(org, project)

        # Initialize GitHub API
        github_api = GitHubAPI(github_token)

        # Resolve the project's topics through the single shared resolver, which
        # reads organizations.settings->'github_topics' (a project's repos are
        # often tagged with something other than its alias -- PixelFuel's alias is
        # "PF" but its repos carry "pixelfuel"), lowercases (GitHub topics always
        # are, aliases are stored uppercase as the ticket prefix), and supports
        # several comma-separated topics per project. Deriving the topic from the
        # alias alone is what made discovery silently return zero repos.
        topics_to_search = (
            [t.strip().lower() for t in github_label.split(",") if t.strip()]
            if github_label
            else onboard.github_topics(org, project)
        )
        if topics_to_search:
            logger.info(f"Searching topics {topics_to_search} in {github_org}")

        # Search repositories with the specified topic(s)
        try:
            if topics_to_search:
                repos = await github_api.search_organization_repositories(
                    github_org, topic=topics_to_search
                )
                logger.info(
                    f"Found {len(repos)} repositories with topic(s) {topics_to_search}"
                )
            else:
                # Fall back to all repositories if no label
                repos = await github_api.get_all_organization_repositories(github_org)
                logger.info(
                    f"No filter specified, discovered all {len(repos)} repositories"
                )
        # Only GitHub's own errors are relabelled. This wrap used to be `except
        # Exception` and it laundered every failure into a `ValueError` carrying
        # `str(e)` -- which `_reportable_sync_error` passes through **verbatim**
        # into `Project.github_error_message`, rendered in the dashboard tooltip
        # to every member of the org.
        #
        # `github_api` uses httpx directly, so a proxy, DNS or TLS failure is not
        # a `GitHubAPIError`: it arrived here as an arbitrary exception, left as a
        # reportable one, and took its connection detail with it. A session-level
        # `OperationalError` raised anywhere in this call did the same. Narrowing
        # is the fix at the cause -- anything we did not author keeps its own type
        # and lands in the generic branch, and the full exception is still logged
        # by `sync_project_repositories` at the point of record.
        except GitHubAPIError as e:
            logger.error(f"Failed to fetch repositories: {str(e)}")
            raise ValueError(f"Failed to fetch repositories: {str(e)}")

        # Process discovered repositories
        discovered_repos = []
        for repo_data in repos:
            # Parse repository data
            parsed = github_api.parse_repository_data(repo_data)

            # Get topics from repository data
            topics = repo_data.get("topics", [])

            # Detect layer using topics as labels
            detected_layer = self.detect_repository_layer(
                repo_name=parsed["name"],
                primary_language=parsed.get("language"),
                topics=topics,
            )

            discovered_repos.append(
                {
                    "github_id": parsed["id"],
                    "name": parsed["name"],
                    "full_name": parsed["full_name"],
                    "url": parsed["url"],
                    "description": parsed.get("description"),
                    "primary_language": parsed.get("language"),
                    "detected_layer": detected_layer.value,
                    "stars": parsed.get("stars", 0),
                    "is_private": parsed.get("is_private", False),
                    "archived": parsed.get("archived", False),
                    "topics": topics,
                }
            )

        return {
            "project_id": project_id,
            "github_org": github_org,
            "github_label": github_label,
            # The RESOLVED topics, not the caller's filter. `github_label` is what
            # was passed in and is usually empty; these are what was actually
            # searched. Surfaced so a caller reporting "found nothing" can say
            # which org and which topics it looked for -- without that, a wrong-org
            # sync and a genuine re-tagging produce identical output.
            "topics_searched": topics_to_search,
            "discovered_repositories": discovered_repos,
            "total_discovered": len(discovered_repos),
        }

    async def import_repositories(
        self,
        organization_id: str,
        project_id: str,
        repositories: List[Dict],
        sync_issues: bool = True,
        sync_readme: bool = True,
    ) -> Dict:
        """
        Import selected repositories into a project with layer assignments.

        Args:
            organization_id: InnoDay organization ID
            project_id: Project ID to import repos into
            repositories: List of repos to import with layer assignments
            sync_issues: Whether to import GitHub issues
            sync_readme: Whether to import README content

        Returns:
            Import results with created/updated repositories
        """
        # Verify organization and project
        org = self.session.get(Organization, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        project = self.session.get(Project, project_id)
        if not project or project.organization_id != organization_id:
            raise ValueError(f"Project {project_id} not found in organization")

        # Get GitHub credentials
        logger.info(f"Looking for GitHub credentials for org alias: {org.alias}")
        creds = self._get_github_credentials(org)
        if not creds:
            logger.warning(
                f"No GitHub credentials found for organization alias: {org.alias}"
            )
            raise ValueError("No GitHub connection found for organization")

        github_token = creds["token"]
        github_api = GitHubAPI(github_token)

        # First, discover all repositories to get their details
        # This allows us to have the full repo data for import
        github_org = creds.get("github_org")
        all_repos = await github_api.get_all_organization_repositories(github_org)
        repos_by_id = {str(repo["id"]): repo for repo in all_repos}

        imported = []
        for repo_config in repositories:
            github_id = repo_config["github_id"]
            layer = RepositoryLayer[repo_config["layer"]]
            is_primary = repo_config.get("is_primary", False)
            purpose = repo_config.get("purpose")

            # Check if repository already exists
            existing_repo = self.session.exec(
                select(Repository).where(Repository.id == github_id)
            ).first()

            # Create or update repository record
            if not existing_repo:
                # Get the repository data from our discovery
                repo_data = repos_by_id.get(github_id)
                if not repo_data:
                    logger.warning(f"Repository {github_id} not found in GitHub org")
                    continue

                # Parse the repository data
                parsed = github_api.parse_repository_data(repo_data)

                # Create new repository
                repo = Repository(
                    id=github_id,
                    organization_id=organization_id,
                    name=parsed["name"],
                    full_name=parsed["full_name"],
                    url=parsed["url"],
                    description=parsed.get("description"),
                    language=parsed.get("language"),
                    stars=parsed.get("stars", 0),
                    forks=parsed.get("forks", 0),
                    open_issues_count=parsed.get("open_issues_count", 0),
                    is_private=parsed.get("is_private", False),
                    archived=parsed.get("archived", False),
                    github_created_at=parsed.get("github_created_at"),
                    github_updated_at=parsed.get("github_updated_at"),
                    # Optional fields - set to None if not needed
                    # client_id removed - using organization_id instead
                    github_org_registration_id=None,
                )
                self.session.add(repo)
                self.session.flush()  # Ensure repo is saved before linking
            else:
                repo = existing_repo

            # Link repository to project
            existing_link = self.session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.project_id == project_id,
                    ProjectRepository.repository_id == repo.id,
                )
            ).first()

            if not existing_link:
                project_repo = ProjectRepository(
                    id=str(uuid4()),
                    project_id=project_id,
                    repository_id=repo.id,
                    layer=layer,
                    is_primary=is_primary,
                    purpose=purpose,
                    added_at=datetime.now(timezone.utc),
                )
                self.session.add(project_repo)

                imported.append(
                    {
                        "repository_id": repo.id,
                        "name": repo.name,
                        "layer": layer.value,
                        "is_primary": is_primary,
                        "action": "imported",
                    }
                )
            else:
                # Update existing link
                existing_link.layer = layer
                existing_link.is_primary = is_primary
                existing_link.purpose = purpose
                self.session.add(existing_link)

                imported.append(
                    {
                        "repository_id": repo.id,
                        "name": repo.name,
                        "layer": layer.value,
                        "is_primary": is_primary,
                        "action": "updated",
                    }
                )

        self.session.commit()

        return {
            "project_id": project_id,
            "imported": imported,
            "total_imported": len(imported),
        }

    async def sync_project_repositories(
        self,
        organization_id: str,
        project_id: str,
        github_label: Optional[str] = None,
    ) -> Dict:
        """
        Sync repositories for a project, checking for new ones and updating existing.

        Args:
            organization_id: InnoDay organization ID
            project_id: Project ID to sync
            github_label: Optional GitHub label to filter by

        Returns:
            Sync results with changes
        """
        # Get project
        project = self.session.get(Project, project_id)
        if not project or project.organization_id != organization_id:
            raise ValueError(f"Project {project_id} not found in organization")

        # Everything from here on is the integration attempt, and its outcome is
        # what the project card's GitHub icon reports. The project lookup above
        # stays outside: a nonexistent project is a bad request, not a failed
        # integration, and there is no row to record it on.
        #
        # The try deliberately reaches all the way to the final commit rather than
        # wrapping discovery alone. A refusal guard, an IntegrityError from a flush,
        # or a failed release discovery all mean the same thing to a reader: the
        # sync did not complete, and the icon exists to say so (#640).
        #
        # `started_at` is taken before the try so that the failure path can report a
        # duration for an attempt that died inside discovery, which is where the
        # slowest failures (an expired token, a renamed org) happen.
        started_at = datetime.now(timezone.utc)
        # Counters the history row reports. Initialised here, outside the try, so
        # the failure path can write what had been achieved when the sync died --
        # they are local variables inside the try and a failure before their
        # assignment would otherwise leave the recorder reading an unbound name and
        # replacing the real exception with a NameError.
        repos_discovered = 0
        repos_created = 0
        repos_updated = 0
        repos_failed = 0
        try:
            # Discover repositories with the label (discover_project_repositories
            # applies the same project.alias-first default when github_label is
            # falsy, so pass it through as-is rather than duplicating the logic).
            discovery_result = await self.discover_project_repositories(
                organization_id=organization_id,
                project_id=project_id,
                github_label=github_label or "",
            )

            discovered_repos = discovery_result["discovered_repositories"]
            discovered_github_ids = {str(r["github_id"]) for r in discovered_repos}
            repos_discovered = len(discovered_repos)

            # Get existing project repositories (active and inactive -- an
            # inactive link whose repo regains the topic label reactivates the
            # same row rather than creating a duplicate, since
            # uq_project_repository is (project_id, repository_id))
            existing_links = self.session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.project_id == project_id
                )
            ).all()
            existing_links_by_repo_id = {
                link.repository_id: link for link in existing_links
            }

            # Refuse a sync that would retire most of the project's repos.
            #
            # Deactivating a repo is how this method records "GitHub no longer tags
            # this for the project", which is a normal, expected event for one or two
            # repos. But the same code path is what a *misconfiguration* produces, and
            # at volume the two are indistinguishable from the output: searching a
            # GitHub org that hosts none of the project's repos discovers nothing, so
            # every existing link looks retired. That is exactly what happened to BPAI
            # -- 9 of 12 deactivated, reported as "9 repositories lost the topic
            # label", which sent the reader to GitHub rather than to the resolver.
            #
            # A wrong org, a typo'd `github_orgs` override, a renamed GitHub org and a
            # token that lost org scope all present this way. None of them are worth
            # applying silently, and all of them are cheap to recover from if the sync
            # stops. Deliberately a hard refusal, not a warning: a warning in a log is
            # not read until someone is already investigating the damage.
            active_links = [link for link in existing_links if link.is_active]
            would_deactivate = [
                link
                for link in active_links
                if link.repository_id not in discovered_github_ids
            ]
            if (
                len(active_links) >= _MASS_DEACTIVATION_MIN_ACTIVE
                and len(would_deactivate)
                >= len(active_links) * _MASS_DEACTIVATION_THRESHOLD
            ):
                raise ValueError(
                    f"Refusing to sync: this would deactivate "
                    f"{len(would_deactivate)} of {len(active_links)} active "
                    f"repositories for project {project.alias}. Searched GitHub org "
                    f"'{discovery_result.get('github_org', '?')}' for topics "
                    f"{discovery_result.get('topics_searched', '?')} and found "
                    f"{len(discovered_repos)} repo(s). That is usually a resolution "
                    f"problem (wrong github_org / github_orgs override, renamed "
                    f"GitHub org, or a token that lost org scope) rather than a real "
                    f"re-tagging. Verify the org and topics above, then re-run."
                )

            # Track changes
            new_repositories = []
            reactivated_repositories = 0
            updated_repositories = 0
            deactivated_repositories = 0
            now = datetime.now(timezone.utc)

            # Confirm with GitHub before retiring anything.
            #
            # Up to here the only GitHub call has been a topic *search*, and its
            # answer is "what carries this topic in the org I searched". Treating
            # "absent from that answer" as "the tag was removed" conflates two
            # different statements: a wrong `github_orgs` override, a renamed org or
            # a token that lost scope all return HTTP 200 with zero repos, and then
            # every attached repo looks retired.
            #
            # So ask about each candidate specifically. `full_name` gives owner/repo
            # independently of whichever org was searched, which is the whole point --
            # the search may have looked in the wrong place, the repo's own identity
            # cannot.
            candidates = [
                link
                for link in existing_links
                if link.is_active and link.repository_id not in discovered_github_ids
            ]
            retained = await self._retain_still_tagged(
                candidates, discovery_result.get("topics_searched") or []
            )
            if retained:
                raise ValueError(
                    f"Refusing to sync: {len(retained)} repo(s) would be deactivated, "
                    f"but they still carry the project's topic on GitHub: "
                    f"{', '.join(sorted(retained.values()))}. Searched GitHub org "
                    f"'{discovery_result.get('github_org', '?')}' for topics "
                    f"{discovery_result.get('topics_searched', '?')} and found "
                    f"{len(discovered_repos)} repo(s). That is a resolution problem "
                    f"(wrong github_org / github_orgs override, renamed GitHub org, "
                    f"or a token that lost org scope), not a re-tagging. Nothing was "
                    f"changed."
                )

            # Deactivate first, before deciding is_primary below -- otherwise a
            # primary repo deactivated in this same call would leave
            # has_existing_primary stale (computed from pre-deactivation state),
            # so a newly-discovered repo could never be promoted to primary and
            # the project would be left with zero active primary repos.
            deactivated_repo_names = []
            for link in existing_links:
                if link.is_active and link.repository_id not in discovered_github_ids:
                    link.is_active = False
                    link.removed_at = now
                    # A deactivated repo can't remain the active primary --
                    # clear it now so has_existing_primary (below) reflects
                    # reality and a replacement can be elected this same call.
                    link.is_primary = False
                    self.session.add(link)
                    deactivated_repositories += 1
                    repo = self.session.get(Repository, link.repository_id)
                    deactivated_repo_names.append(
                        repo.name if repo else link.repository_id
                    )

            has_existing_primary = any(
                link.is_primary and link.is_active for link in existing_links
            )

            # Process discovered repositories
            for repo_data in discovered_repos:
                # Repository.id IS the GitHub repository id (see src/domain/repository.py)
                github_id = str(repo_data["github_id"])
                repo = self.session.get(Repository, github_id)

                if not repo:
                    # Create new repository
                    repo = Repository(
                        id=github_id,
                        organization_id=organization_id,
                        name=repo_data["name"],
                        full_name=repo_data["full_name"],
                        url=repo_data["url"],
                        description=repo_data.get("description"),
                        language=repo_data.get("primary_language"),
                        is_private=repo_data.get("is_private", False),
                        archived=repo_data.get("archived", False),
                        layer=repo_data["detected_layer"],
                        last_synced_at=now,
                    )
                    self.session.add(repo)
                    self.session.flush()  # Ensure repo is persisted before linking
                else:
                    # Update existing repository metadata.
                    #
                    # `updated_repositories` counts repositories whose metadata
                    # actually **changed**. It used to increment once per existing
                    # repository discovery returned, so a sync that changed nothing
                    # reported "40 existing repositories updated" -- the CLI prints
                    # that line verbatim, and it lands in `repositories_updated` on
                    # the sync-history row. A presence count labelled as a change
                    # count, in the record built to stop exactly that.
                    #
                    # `last_synced_at` is left out of the comparison deliberately: it
                    # changes on every sync by definition, so including it would make
                    # the count unconditional again.
                    incoming = (
                        repo_data.get("description"),
                        repo_data.get("primary_language"),
                        repo_data.get("archived", False),
                        repo_data["detected_layer"],
                    )
                    if (
                        repo.description,
                        repo.language,
                        repo.archived,
                        repo.layer,
                    ) != incoming:
                        updated_repositories += 1
                    (
                        repo.description,
                        repo.language,
                        repo.archived,
                        repo.layer,
                    ) = incoming
                    repo.last_synced_at = now
                    self.session.add(repo)

                existing_link = existing_links_by_repo_id.get(repo.id)

                if existing_link is None:
                    # Only the very first repo ever linked to a project (across
                    # all syncs, not just this call) becomes primary.
                    is_primary = not has_existing_primary and len(new_repositories) == 0
                    project_repo = ProjectRepository(
                        project_id=project_id,
                        repository_id=repo.id,
                        layer=RepositoryLayer(repo_data["detected_layer"]),
                        is_primary=is_primary,
                        # A repo arriving with no other project link adopts this
                        # project as its primary, matching the migration's backfill
                        # rule: one link is unambiguous. A repo that already belongs
                        # somewhere keeps whatever primary it has, so discovery can
                        # never move a repo's release path -- discovery only ever
                        # adds, and reassigning where a version lands is a decision.
                        is_primary_project=not self._repo_has_project_link(
                            repo.id, excluding_project_id=project_id
                        ),
                        added_at=now,
                    )
                    self.session.add(project_repo)
                    existing_links_by_repo_id[repo.id] = project_repo
                    if is_primary:
                        has_existing_primary = True
                    new_repositories.append(
                        {
                            "name": repo.name,
                            "url": repo.url,
                            "layer": repo_data["detected_layer"],
                        }
                    )
                elif not existing_link.is_active:
                    # Repo regained the topic label -- reactivate the same row.
                    # Layer is intentionally left untouched (matching `purpose`,
                    # which was already never touched here) -- an admin's manual
                    # reclassification via PUT .../repositories/{repo_id} must
                    # survive a deactivate/reactivate cycle, not get silently
                    # reverted to whatever GitHub's auto-detection says today.
                    existing_link.is_active = True
                    existing_link.removed_at = None
                    if not has_existing_primary:
                        existing_link.is_primary = True
                        has_existing_primary = True
                    self.session.add(existing_link)
                    reactivated_repositories += 1

            # If every active link's primary was cleared above (or none was ever
            # set) and at least one repo is still active, deterministically
            # promote one rather than leaving the project with zero primaries.
            if not has_existing_primary:
                for link in existing_links_by_repo_id.values():
                    if link.is_active:
                        link.is_primary = True
                        self.session.add(link)
                        break

            # One timeline entry per sync call, only if something changed --
            # a no-op sync (nothing added/reactivated/removed) isn't worth a row.
            repos_added = bool(new_repositories or reactivated_repositories)
            repos_removed = bool(deactivated_repositories)
            if repos_added or repos_removed:
                summary_parts = []
                if new_repositories:
                    summary_parts.append(
                        f"{len(new_repositories)} repo(s) attached: "
                        + ", ".join(r["name"] for r in new_repositories)
                    )
                if reactivated_repositories:
                    summary_parts.append(
                        f"{reactivated_repositories} repo(s) reactivated"
                    )
                if deactivated_repositories:
                    summary_parts.append(
                        f"{deactivated_repositories} repo(s) lost the topic label: "
                        + ", ".join(deactivated_repo_names)
                    )

                # REPO_ADDED if anything was added/reactivated this call (even
                # alongside removals); REPO_REMOVED only for a pure-removal sync.
                event_type = (
                    TimelineEventType.REPO_ADDED
                    if repos_added
                    else TimelineEventType.REPO_REMOVED
                )

                add_timeline_entry(
                    self.session,
                    organization_id=organization_id,
                    project_id=project_id,
                    event_type=event_type,
                    title="Project repositories synced",
                    summary="; ".join(summary_parts) + ".",
                    created_by="system",
                    metadata={
                        "new_repositories": new_repositories,
                        "reactivated_repositories": reactivated_repositories,
                        "deactivated_repositories": deactivated_repositories,
                        "deactivated_repository_names": deactivated_repo_names,
                    },
                )

            self.session.commit()

            repos_created = len(new_repositories)
            repos_updated = updated_repositories

            pr_counts, repos_failed = await self._refresh_open_pr_counts(
                organization_id, project_id
            )
            releases_found = await self._discover_releases(
                organization_id, project_id, project
            )
            # Cleared here, inside the try and against the same commit as the
            # sync's own writes -- so success is recorded atomically with what
            # succeeded. Clearing any earlier would have already gone green by
            # the time `_refresh_open_pr_counts` or `_discover_releases` failed.
            self._clear_project_sync_error(project)
            self.session.commit()
        except Exception as exc:  # noqa: BLE001 -- any failure means the sync did not complete, and the icon has to say so
            # Logged here, at the point of record, and before anything else runs.
            # Two reasons it is not left to the caller: a failure would otherwise
            # be durable in the database ("GitHub failed because X") with no
            # matching line in the logs, and the *stored* message is deliberately
            # lossy for unexpected types (see `_reportable_sync_error`), so this
            # is the only place the real exception survives in full.
            logger.exception(
                "GitHub repository sync failed for project %s in organization %s",
                project_id,
                organization_id,
            )
            # Record and re-raise, bare. The recorder writes state; it does not
            # change control flow, so the routers go on returning 400 and the
            # caller still learns the sync failed.
            #
            # It is wrapped because it issues statements of its own (rollback,
            # get, commit) and any of them can raise -- a connection that died
            # behind the session (pooler restart, failover) surfaces as
            # OperationalError/PendingRollbackError. Unwrapped, that would
            # *replace* `exc` on the way out: `routers/projects.py` matches
            # `except ValueError`, so the caller would get a 500 carrying a
            # database error instead of a 400, and the flag would go unwritten --
            # leaving the icon green for precisely the failure this exists to
            # surface. The recorder is best-effort *reporting*; it must never
            # replace the thing it is reporting on.
            try:
                self._record_project_sync_error(project_id, _reportable_sync_error(exc))
            except Exception:  # noqa: BLE001 -- a broken recorder must not become the error the caller sees
                logger.exception(
                    "Could not record the failed GitHub sync for project %s; "
                    "the original sync failure is re-raised unchanged",
                    project_id,
                )
            # After `_record_project_sync_error`, never before, and the ordering is
            # load-bearing twice over. That method rolls back first (an aborted
            # Postgres transaction silently downgrades COMMIT to ROLLBACK, so a row
            # written into one is lost while the code believes it persisted) and then
            # commits, which leaves a clean transaction for this insert to land in.
            # And the flag the dashboard reads is the more important of the two
            # writes, so it goes first: if only one of them survives, it should be
            # the one on screen.
            self._record_sync_history(
                organization_id=organization_id,
                project_id=project_id,
                started_at=started_at,
                status="failed",
                repositories_synced=repos_discovered,
                repositories_created=repos_created,
                repositories_updated=repos_updated,
                repositories_failed=repos_failed,
                exc=exc,
            )
            raise

        # Outside the `try`, deliberately. Inside it, a database failure while
        # writing this audit row would be caught by the handler above and reported
        # as a *failed sync* -- turning the record of a success into the destruction
        # of one. `_record_sync_history` also swallows its own errors, so this is
        # belt-and-braces; the placement is what makes it unarguable.
        self._record_sync_history(
            organization_id=organization_id,
            project_id=project_id,
            started_at=started_at,
            status="completed",
            repositories_synced=repos_discovered,
            repositories_created=repos_created,
            repositories_updated=repos_updated,
            repositories_failed=repos_failed,
        )

        return {
            "sync_id": str(uuid4()),
            "project_id": project_id,
            "status": "completed",
            "repositories_synced": len(discovered_repos),
            "issues_synced": 0,  # Issue sync not implemented yet
            "open_pr_repos_counted": pr_counts,
            "releases_discovered": releases_found,
            "changes": {
                "new_repositories": new_repositories,
                "reactivated_repositories": reactivated_repositories,
                "updated_repositories": updated_repositories,
                "deactivated_repositories": deactivated_repositories,
                "deactivated_repository_names": deactivated_repo_names,
                "new_issues": 0,
                "updated_issues": 0,
            },
            "timestamp": now.isoformat(),
        }

    def _client_for_org(self, organization_id: str) -> Optional[GitHubAPI]:
        """A GitHub client for this org, or None when it has no credential.

        The service builds one per call from org credentials rather than holding
        one on `self` -- the token is per-organization and resolved from Vault, so
        there is no single client the instance could own.
        """
        org = self.session.get(Organization, organization_id)
        if org is None:
            return None
        creds = self._get_github_credentials(org)
        if not creds or not creds.get("token"):
            return None
        return GitHubAPI(creds["token"])

    async def _refresh_open_pr_counts(
        self, organization_id: str, project_id: str
    ) -> Tuple[int, int]:
        """Count open PRs per active repo. Returns ``(counted, failed)``.

        One API call per repo, which is why it runs at sync time rather than on
        page render. A repo whose count cannot be read keeps its previous value
        rather than being zeroed -- a failed count is not evidence of no PRs.

        ``failed`` is the repos this method marked errored, and it is returned
        rather than recomputed because it is the only number here that is *known*:
        counting rows with `errored_at` afterwards would also pick up marks left
        by an earlier run. It feeds `repositories_failed` on the sync-history row.

        **This is the only writer of `open_pr_count`, so it is also the only writer
        of `open_pr_counted_at`** -- the count's own age, stamped beside the value
        it describes and only on a read that succeeded. Nothing else may stamp it:
        the badge that reads it is making a claim about *this* number, and the
        repository's other timestamps are written by metadata syncs that never look
        at a pull request. A repo that fails its read keeps both its previous count
        and the previous timestamp, which is what makes the pair honest -- the
        number is old, and the badge says how old.
        """
        api = self._client_for_org(organization_id)
        if api is None:
            return 0, 0

        links = self.session.exec(
            select(ProjectRepository, Repository)
            .join(Repository, Repository.id == ProjectRepository.repository_id)
            .where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active == True,  # noqa: E712
                Repository.archived == False,  # noqa: E712
                Repository.deleted == False,  # noqa: E712
            )
        ).all()

        # One instant for the whole pass, so two repos read seconds apart do not
        # render different ages. Naive UTC, the convention for datetime columns
        # here (CLAUDE.md).
        counted_at = datetime.now(timezone.utc).replace(tzinfo=None)

        counted = 0
        failed = 0
        for _link, repo in links:
            owner, _, name = (repo.full_name or "").partition("/")
            if not owner or not name:
                continue
            prs = await api.list_open_pull_requests(owner, name)
            if prs is None:
                # Unreadable, not empty. Leave both the stored rows and the
                # previous count alone -- deleting them here would report "no
                # open PRs" off a network blip, which is a claim about people's
                # work rather than about the fetch.
                self._record_repo_error(repo, "Could not read open pull requests")
                failed += 1
                continue
            if not prs:
                believable, why = await self._empty_pr_list_is_believable(
                    api, owner, name, repo
                )
                if not believable:
                    self._record_repo_error(repo, why)
                    failed += 1
                    continue
            await self._store_pull_requests(repo, prs, api, owner, name)
            # Derived, not stored twice: the count is len() of what was kept, so
            # the number on the card and the list on the project page cannot
            # drift apart (#500).
            repo.open_pr_count = len(prs)
            # Stamped here, next to the value, and nowhere else -- see the field's
            # comment for why borrowing `last_synced_at` produced a false claim.
            repo.open_pr_counted_at = counted_at
            self._clear_repo_error(repo)
            self.session.add(repo)
            counted += 1
        return counted, failed

    async def _empty_pr_list_is_believable(
        self, api: GitHubAPI, owner: str, name: str, repo
    ) -> Tuple[bool, str]:
        """Whether ``200 []`` for this repo may be acted on. ``(ok, why_not)``.

        `_store_pull_requests` marks every stored row GitHub did not return as
        closed, so an empty list is an instruction to close all of them. That is correct
        surprisingly often -- the last open pull request closing is an ordinary
        event -- and a blanket "never delete on empty" would leave merged work on
        the dashboard forever. So the empty list is not distrusted; it is
        *checked*, and only when there is something to lose.

        **A successful fetch can still be wrong.** A token that has lost access to
        a repository -- reinstalled app, revoked org grant, repo turned private,
        SSO re-authorisation lapsed -- receives HTTP 200 with `[]` on
        `/pulls`, byte-for-byte what a repository with nothing open returns.
        `list_open_pull_requests` distinguishes *unreadable* from *empty* only for
        transport failures; this case never fails, so nothing upstream can catch
        it. It did not cause #650 (no sync ran at all there) but it would delete
        real work silently the first time a grant lapsed.

        The check: ask GitHub about one pull request we already have on file. If it
        answers "closed", the empty list is consistent with what it claims and is
        acted on -- not proof that *every* stored row closed, but the cheapest
        evidence that the repository is genuinely being read, which is the thing in
        doubt. If it answers "open", the list contradicts GitHub's own answer about
        a single pull request and is not acted on. If it does not answer at all,
        the repository is not being read reliably and the list is not acted on
        either -- a probe that cannot reach the repo is exactly the state the
        lapsed-grant case produces.

        The highest stored number is probed rather than an arbitrary one: it is the
        most recently opened, so it is the one most likely to still be open, which
        is what gives the check its power to detect a lying list. Probing the
        oldest would find a legitimately-closed pull request most of the time and
        wave the empty list through.

        One extra request, only when the list is empty *and* rows are stored --
        never on the ordinary path, and never for a repository that has nothing to
        lose.
        """
        from src.domain.repository_pull_request import RepositoryPullRequest

        # **Only rows still marked open.** Closed rows are kept now rather than
        # deleted, so an unfiltered `max()` would soon pick a closed pull request
        # -- whose probe answers "closed", which this method reads as "the empty
        # list is believable". The guard would agree with every empty list it was
        # ever shown, and go on doing so silently.
        stored = self.session.exec(
            select(RepositoryPullRequest.number).where(
                RepositoryPullRequest.repository_id == repo.id,
                RepositoryPullRequest.state == "open",
            )
        ).all()
        if not stored:
            # Nothing open to close, so nothing to protect. Believe it, move on.
            return True, ""

        probe = max(stored)
        state = await api.get_pull_request_state(owner, name, probe)
        if state == "closed":
            return True, ""
        if state is None:
            return False, (
                f"GitHub reported no open pull requests, but would not answer for "
                f"#{probe}, which is stored as open. The {len(stored)} stored "
                f"pull request(s) were kept rather than deleted -- a token that "
                f"has lost access to a repository gets an empty list, not an "
                f"error. Check this organization's GitHub access, then sync again."
            )
        return False, (
            f"GitHub reported no open pull requests, but #{probe} is still open. "
            f"The {len(stored)} stored pull request(s) were kept rather than "
            f"deleted. Check this organization's GitHub access, then sync again."
        )

    async def _store_pull_requests(
        self, repo, prs: List[Dict[str, Any]], api=None, owner: str = "", name: str = ""
    ) -> None:
        """Upsert this repo's open PRs, and mark the ones that left the list.

        Upsert on ``(repository_id, number)`` rather than delete-then-insert: a
        PR keeps its row across syncs, so anything later hung off it survives.

        **Rows that are no longer open are marked, not deleted.** They used to be
        removed, which severed a ticket's link to the pull requests that shipped
        it at the exact moment the work shipped -- `head_ref` is the only field on
        a pull request that names a ticket. Every "open pull requests" view now
        filters on ``state`` instead of relying on absence, so what they show is
        unchanged.

        ``api``/``owner``/``name`` are optional so a caller that only wants the
        upsert can omit them; without them a departed pull request is recorded as
        closed with no merge verdict, which reads as "did not demonstrably ship".

        **A wrongly-empty list is still the caller's problem, not this method's.**
        An empty list is what a token that lost access to the repository receives,
        and marking everything closed off a network blip is a claim about people's
        work. `_empty_pr_list_is_believable` is the gate, and the caller runs it
        before an empty list reaches here.
        """
        from src.domain.repository_pull_request import RepositoryPullRequest

        existing = {
            row.number: row
            for row in self.session.exec(
                select(RepositoryPullRequest).where(
                    RepositoryPullRequest.repository_id == repo.id
                )
            ).all()
        }
        now = datetime.now(timezone.utc)
        seen = set()

        for pr in prs:
            number = pr.get("number")
            if number is None:
                continue
            seen.add(number)
            row = existing.get(number) or RepositoryPullRequest(
                repository_id=repo.id, number=number
            )
            row.title = (pr.get("title") or "")[:500]
            row.url = (pr.get("html_url") or pr.get("url") or "")[:500]
            row.author_login = (pr.get("user") or {}).get("login") or None
            # `head.ref` is the branch. It is on the payload already, so this
            # costs no extra request -- and it is the only field here that can tie
            # a pull request to a ticket.
            head_ref = (pr.get("head") or {}).get("ref")
            row.head_ref = (head_ref or None) and str(head_ref)[:255]
            row.assignee_logins = [
                a.get("login")
                for a in (pr.get("assignees") or [])
                if isinstance(a, dict) and a.get("login")
            ]
            row.is_draft = bool(pr.get("draft"))
            # It is in the open list, so it is open -- including a row that was
            # marked closed and has since been reopened.
            row.state = "open"
            row.merged_at = None
            row.closed_seen_at = None
            # GitHub's own timestamps. Stamping these with the sync instant would
            # make every PR look brand new after a re-sync -- the same bug #503
            # fixed for Linear tickets.
            row.github_created_at = _parse_github_time(pr.get("created_at"))
            row.github_updated_at = _parse_github_time(pr.get("updated_at"))
            row.last_synced_at = now
            self.session.add(row)

        # **Rows that left the open list are marked, not deleted.** `head_ref` is
        # the only field on a pull request that names a ticket, so deleting the
        # row severed that link at the exact moment the work shipped -- "which
        # pull requests shipped PF-1268?" was answerable right up until it was
        # worth asking.
        #
        # One request per departed pull request, and only for those: a repo where
        # nothing changed pays nothing, and a repo where five merged pays five.
        # Cheaper than re-listing closed pull requests on every sync, and it can
        # say *merged* rather than only *not open* -- an abandoned pull request
        # shipped nothing and must not read as though it had.
        for number, row in existing.items():
            if number in seen:
                continue
            if row.state != "open":
                continue  # already accounted for; do not re-ask every sync
            row.state = "closed"
            row.closed_seen_at = now
            outcome = await api.get_pull_request_outcome(owner, name, number)
            if outcome:
                merged = _parse_github_time(outcome.get("merged_at"))
                row.merged_at = merged
            # An unanswered probe leaves `merged_at` None, which reads as "did
            # not demonstrably ship" -- the safe direction. Claiming a merge we
            # could not confirm would put work in a release that never had it.
            self.session.add(row)

    def _record_repo_error(self, repo, message: str) -> None:
        """Mark this repository as having failed its last sync."""
        repo.errored_at = datetime.now(timezone.utc)
        repo.error_message = message[:500]
        self.session.add(repo)

    def _clear_repo_error(self, repo) -> None:
        """Clear a previous failure. **This half is what makes the flag mean
        anything** -- a mark that is only ever set becomes a permanent red for
        one bad afternoon, and people learn to ignore it (#499)."""
        if repo.errored_at is not None or repo.error_message is not None:
            repo.errored_at = None
            repo.error_message = None
            self.session.add(repo)

    def _record_project_sync_error(self, project_id: str, message: str) -> None:
        """Mark this project's last repository sync as failed.

        **The rollback comes first, and that ordering is load-bearing.** On
        Postgres a failed statement leaves the transaction aborted: every later
        statement is refused *and* `COMMIT` is silently downgraded to `ROLLBACK`
        while reporting success -- so a flag written into that transaction is lost
        while this code believes it persisted. SQLite has no such state, which is
        why the default fixtures cannot catch it; see
        `tests/test_postgres_only.py`. Rolling back is safe *because* everything
        pending belongs to a sync that just failed.

        The re-fetch after the rollback is not optional either: rollback expires
        identity-map state, and re-reading is what guarantees the UPDATE is issued
        in the fresh transaction rather than skipped as unchanged.

        The explicit `commit()` is load-bearing too -- `get_session` never commits
        on teardown, so an uncommitted flag here would simply be dropped.

        `message` is the *reportable* string, not `str(exc)`: this column is
        rendered to every org member, so the caller narrows it through
        `_reportable_sync_error` first. Those three statements are also why the
        caller wraps this call -- any of them can raise, and reporting a failure
        must never replace it.
        """
        self.session.rollback()
        project = self.session.get(Project, project_id)
        if project is None:
            return
        project.github_errored_at = datetime.now(timezone.utc)
        project.github_error_message = message[:500]
        self.session.add(project)
        self.session.commit()

    def _record_sync_history(
        self,
        *,
        organization_id: str,
        project_id: str,
        started_at: datetime,
        status: str,
        repositories_synced: int,
        repositories_created: int,
        repositories_updated: int,
        repositories_failed: int,
        exc: Optional[BaseException] = None,
    ) -> None:
        """Write the `github_sync_history` row for one finished sync attempt.

        **The table's only writer, since #658.** It briefly shared it with the
        org-wide registration sync (`routers/repositories.py`,
        `RepositorySyncService`), which wrote `"running"` and `"pending"` rows keyed
        on a `GitHubOrgRegistration` and counted every repository that registration
        reached. That import path is gone -- it had produced 0 of 36 repositories in
        dev -- and with it the second grain, so every row in this table is now one
        project's sync and any two rows' counts are comparable.

        Every row carries `organization_id` (the tenant, and what the RLS policy
        keys on) and `project_id` (what the reader filters by).

        **The rollback comes first, and that ordering is load-bearing** -- the same
        hazard `_record_project_sync_error` documents, and it applies with full force
        here because the common case for this method *is* the failure path. On
        Postgres a failed statement leaves the transaction aborted: every later
        statement is refused, and `COMMIT` is silently downgraded to `ROLLBACK`
        while reporting success. An audit row inserted into that transaction is
        therefore lost while this code believes it persisted -- an audit trail that
        is silently empty exactly when something went wrong, which is worse than no
        table at all and is indistinguishable from the bug this closes. SQLite has
        no aborted state, so the default fixtures cannot catch it; the Postgres test
        can.

        Rolling back is safe on both paths. On failure, everything pending belongs
        to a sync that just died. On success, the caller has already committed
        (twice), so there is nothing pending to discard.

        The explicit `commit()` is load-bearing too: `get_session` never commits on
        teardown, so an uncommitted row here would simply be dropped.

        **Two error fields, two different audiences.** `error_message` goes through
        `_reportable_sync_error`, because a stored, potentially-rendered field is a
        disclosure surface -- #641 found `IntegrityError` stringifying to SQL plus
        bound parameters and `OperationalError` to connection detail. Nothing renders
        this column today, and that is precisely why it must be narrowed now rather
        than when something starts to: the row outlives the decision not to show it.
        `error_details` gets the exception *type* and nothing more -- enough to
        correlate a row with the `logger.exception` line the caller has already
        written, which is where the unabridged traceback lives.

        `api_calls_made` is deliberately left NULL. Nothing counts requests: the
        GitHub client is constructed per call and keeps no tally, so any number put
        here would be arithmetic over assumptions -- which is the class of bug this
        issue is about. NULL says "not measured"; a plausible-looking integer would
        not.

        Never raises. A failure to record must not become the error the caller
        reports, in either direction -- see the two call sites.
        """
        try:
            self.session.rollback()
            completed_at = datetime.now(timezone.utc)

            # No registration is looked up, and there is no column left to put one
            # in. A project sync has none in scope -- `connect_github_organization`
            # creates the row only when a `user_id` is attributable, storing the
            # credential regardless -- so this used to resolve the *oldest*
            # registration for the org just to have something to key on, which
            # filed a project-scoped attempt under an org-wide sync record. #658
            # dropped the column instead.
            row = GitHubSyncHistory(
                id=str(uuid4()),
                organization_id=organization_id,
                project_id=project_id,
                started_at=started_at.replace(tzinfo=None),
                completed_at=completed_at.replace(tzinfo=None),
                status=status,
                repositories_synced=repositories_synced,
                repositories_created=repositories_created,
                repositories_updated=repositories_updated,
                repositories_failed=repositories_failed,
                # Project sync reads no READMEs. 0 is the true count, not a
                # placeholder for "did not look".
                readmes_synced=0,
                error_message=(
                    _reportable_sync_error(exc)[:500] if exc is not None else None
                ),
                error_details=(
                    f"{type(exc).__name__} — full detail in the server log"
                    if exc is not None
                    else None
                ),
                duration_seconds=(completed_at - started_at).total_seconds(),
                api_calls_made=None,
            )
            self.session.add(row)
            self.session.commit()
        except Exception:  # noqa: BLE001 -- an audit row must never replace the outcome it records
            logger.exception(
                "Could not record github_sync_history for project %s in "
                "organization %s (sync status was %s)",
                project_id,
                organization_id,
                status,
            )

    def _clear_project_sync_error(self, project) -> None:
        """Clear a previous failure. **This half is what makes the flag mean
        anything** -- a mark that is only ever set becomes a permanent red for one
        bad afternoon, and people learn to ignore it (#499, #640)."""
        if project.github_errored_at is not None or project.github_error_message:
            project.github_errored_at = None
            project.github_error_message = None
            self.session.add(project)

    def _repo_has_project_link(
        self, repository_id: str, excluding_project_id: str
    ) -> bool:
        """Whether this repo is already linked to some *other* project.

        ``is_active`` is deliberately ignored: an inactive link is a repo that
        lost a project's topic and can regain it (``uq_project_repository`` exists
        so reactivation reuses the row). Treating an inactive link as absent would
        hand this project the primary now and collide with
        ``uq_repo_primary_project`` when the other link came back.
        """
        return (
            self.session.exec(
                select(ProjectRepository.id).where(
                    ProjectRepository.repository_id == repository_id,
                    ProjectRepository.project_id != excluding_project_id,
                )
            ).first()
            is not None
        )

    async def _retain_still_tagged(self, candidates, topics) -> Dict[str, str]:
        """Which candidates must NOT be deactivated, keyed by repository id.

        A candidate is retained when GitHub says it still carries one of the
        project's topics, and *also* when the lookup fails: absence of evidence
        is not evidence of removal, and the cost of being wrong is asymmetric --
        a repo wrongly retired disappears from the project and, on the next
        refresh, from the developer's disk.

        Costs one call per candidate. Candidates are normally zero; when they are
        not, the run is about to make an irreversible-feeling change and the calls
        are the cheapest part of it.
        """
        if not candidates:
            return {}

        wanted = {t.strip().lower() for t in (topics or []) if t and t.strip()}
        api = self._client_for_org_id_of(candidates)
        retained: Dict[str, str] = {}

        for link in candidates:
            repo = self.session.get(Repository, link.repository_id)
            full_name = (repo.full_name or "") if repo else ""
            owner, _, name = full_name.partition("/")
            label = full_name or (repo.name if repo else link.repository_id)

            if not owner or not name or api is None:
                # Nothing to ask with -- retain, for the same reason as a failed
                # lookup below.
                retained[link.repository_id] = label
                continue

            try:
                live = {
                    t.strip().lower()
                    for t in await api.get_repository_topics(owner, name)
                }
            except Exception as exc:  # noqa: BLE001 -- see the docstring
                logger.warning(
                    "topic confirmation failed for %s (%s); not deactivating",
                    label,
                    exc,
                )
                retained[link.repository_id] = label
                continue

            if live & wanted:
                retained[link.repository_id] = label

        return retained

    def _client_for_org_id_of(self, candidates):
        """The GitHub client for these links' organization."""
        repo = self.session.get(Repository, candidates[0].repository_id)
        if repo is None or not repo.organization_id:
            return None
        return self._client_for_org(repo.organization_id)

    async def _discover_releases(
        self, organization_id: str, project_id: str, project
    ) -> int:
        """Create Release rows from the GitHub releases of the project's repos.

        Releases were previously only recorded two ways: by the release engine at
        cut time, and as a side effect of board sync seeing a version-shaped label
        on a ticket. Both are *registrations* -- if a release is cut without going
        through them, InnoDay never learns of it. That is exactly what happened to
        BPAI: its newest record is v1.8.0 while the repos are past it, and the only
        IN_PROGRESS row is a stale v1.4.0, which the dashboard then showed as the
        next launch. Reading GitHub makes the record self-healing instead.

        A published GitHub release means shipped, so rows are created (or moved) to
        RELEASED with the publication date. Drafts and prereleases are skipped:
        they are not shipped, and treating them as such is how a "next launch"
        starts lying in the other direction.

        **Only repos whose primary project is this one are read.** A repository's
        own package version and the cross-repo release it happens to be tagged
        into are independent, and this method used to conflate them: it read every
        repo linked to the project, so publishing ``innoday-blastoff`` v0.3.0 --
        unavoidable, since its PyPI publish triggers on a published GitHub
        Release -- created a PF *platform* release v0.3.0, which then became
        ``max(released)`` and collapsed the v1.0.0 changelog window from 171
        merged PRs to 5. See ``ProjectRepository.is_primary_project``.
        """
        api = self._client_for_org(organization_id)
        if api is None:
            return 0

        links = self.session.exec(
            select(Repository)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active == True,  # noqa: E712
                ProjectRepository.is_primary_project == True,  # noqa: E712
            )
        ).all()

        # A multi-project repo with no primary designated anywhere contributes no
        # releases, and that has to be *said* rather than silently true: it is
        # indistinguishable from "this repo has never released" at the row level,
        # and the whole failure mode being fixed here is a version appearing where
        # nobody chose to put it. Naming the repo turns the omission into a
        # decision somebody can make.
        undecided = self.session.exec(
            select(Repository.full_name)
            .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
            .where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.is_active == True,  # noqa: E712
                ProjectRepository.is_primary_project == False,  # noqa: E712
            )
        ).all()
        if undecided:
            logger.info(
                "release discovery skipping %d repo(s) whose primary project is "
                "not this one (or is undecided): %s -- set one with "
                "`innoday repos set-primary <name>` from that project's workspace",
                len(undecided),
                ", ".join(sorted(n for n in undecided if n)),
            )

        seen: Dict[str, datetime] = {}
        for repo in links:
            owner, _, name = (repo.full_name or "").partition("/")
            if not owner or not name:
                continue
            try:
                releases = await api.get_releases(owner, name)
            except (NameError, AttributeError, TypeError):
                # Programming errors, not "GitHub is unhappy about this repo".
                # Letting these through is the whole point: the first version of
                # this shipped with a NameError that the broad catch below turned
                # into an info log, so every sync reported success and discovered
                # nothing. A bug must be able to fail loudly.
                raise
            except Exception as exc:  # noqa: BLE001 - one bad repo must not fail a sync
                logger.warning(
                    "release discovery failed for %s: %s", repo.full_name, exc
                )
                continue

            for entry in releases:
                if entry.get("draft") or entry.get("prerelease"):
                    continue
                version = (entry.get("tag_name") or entry.get("name") or "").strip()
                if not version:
                    continue
                published = entry.get("published_at")
                when = now_utc = datetime.now(timezone.utc)
                if published:
                    try:
                        when = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    except ValueError:
                        when = now_utc
                # Several repos ship the same version in one cross-repo release;
                # keep the earliest publication as the release date.
                if version not in seen or when < seen[version]:
                    seen[version] = when

        created = 0
        promoted = 0
        for version, when in seen.items():
            existing = self.session.exec(
                select(Release).where(
                    Release.project_id == project_id,
                    Release.version == version,
                    Release.deleted_at.is_(None),
                )
            ).first()
            if existing is None:
                self.session.add(
                    Release(
                        organization_id=organization_id,
                        project_id=project_id,
                        version=version,
                        status=ReleaseStatus.RELEASED,
                        released_at=when,
                    )
                )
                created += 1
            elif existing.status != ReleaseStatus.RELEASED:
                # A row that board sync guessed as PLANNED, now known to have
                # shipped. This is what clears the stale IN_PROGRESS rows that
                # made "next launch" point backwards.
                existing.status = ReleaseStatus.RELEASED
                existing.released_at = existing.released_at or when
                self.session.add(existing)
                promoted += 1

        self.session.flush()

        # Straighten the statuses before deciding whether anything is missing:
        # a stale IN_PROGRESS from before the latest ship would otherwise look
        # like a plan and suppress the next version.
        all_releases = list(
            self.session.exec(
                select(Release).where(
                    Release.project_id == project_id,
                    Release.deleted_at.is_(None),
                )
            ).all()
        )
        reconciled = reconcile_statuses(all_releases)
        for release in all_releases:
            self.session.add(release)
        self.session.flush()

        created += self._ensure_release_pipeline(
            organization_id, project_id, all_releases
        )
        return created + promoted + reconciled

    def _ensure_release_pipeline(
        self, organization_id: str, project_id: str, releases: List[Release]
    ) -> int:
        """Keep the project's two forward release slots open.

        Slot 1 is IN_PROGRESS -- the version blastoff cuts next -- and slot 2 is
        PLANNED, the version tickets are being planned into. Shipping rotates
        them, and this is the repair path: a rotation that failed partway (the
        release was recorded, the API call that should have advanced the pipeline
        did not land) is put right on the next sync rather than leaving the
        project with nothing upcoming.

        Sync writes the intent; blastoff is still what cuts the tag and creates
        the GitHub release, and its own registration converges on these same
        (project, version) rows.

        This replaced ``_ensure_next_planned_release``, which opened a single
        PLANNED row and only when nothing at all was upcoming. One row was enough
        to stop the dashboard showing a dash, but not enough to plan against: the
        version being cut and the version being filled are different things, and a
        drop target that may or may not exist is not a planning surface.
        """
        opened = 0
        for version, status in ensure_pipeline(releases):
            self.session.add(
                Release(
                    organization_id=organization_id,
                    project_id=project_id,
                    version=version,
                    status=status,
                )
            )
            opened += 1
            logger.info(
                "opened %s as %s for project %s",
                version,
                status.value,
                project_id,
            )
        # `ensure_pipeline` reconciles in place as well as reporting what is
        # missing, so rows it promoted have to be persisted, not just new ones.
        for release in releases:
            self.session.add(release)
        return opened

    async def remove_project_repository(
        self,
        organization_id: str,
        project_id: str,
        repository_id: str,
        github_label: Optional[str] = None,
    ) -> Dict:
        """
        Remove a repository from a project: removes the project's GitHub
        topic label from the actual repo on GitHub, then soft-deletes the
        ProjectRepository link to match. GitHub is the source of truth --
        InnoDay's link state follows it, not the other way around.

        Args:
            organization_id: InnoDay organization ID
            project_id: Project to remove the repository from
            repository_id: Repository to remove
            github_label: Topic to remove. Defaults to the project's alias
                (lowercased) if omitted.

        Returns:
            Dict describing the removal
        """
        org = self.session.get(Organization, organization_id)
        if not org:
            raise ValueError(f"Organization {organization_id} not found")

        project = self.session.get(Project, project_id)
        if not project or project.organization_id != organization_id:
            raise ValueError(f"Project {project_id} not found in organization")

        link = self.session.exec(
            select(ProjectRepository).where(
                ProjectRepository.project_id == project_id,
                ProjectRepository.repository_id == repository_id,
                ProjectRepository.is_active == True,
            )
        ).first()
        if not link:
            raise ValueError("Repository not found in project")

        repo = self.session.get(Repository, repository_id)
        if not repo:
            raise ValueError(f"Repository {repository_id} not found")

        # Must use the same resolver as discovery: this call MUTATES GitHub
        # (strips the topic). Deriving it from the alias alone stripped
        # `pf` -- which no repo carries -- instead of `pixelfuel`, so the
        # link was deactivated while GitHub kept the tag.
        if github_label:
            topic = github_label
        else:
            resolved = WorkspaceOnboardService(self.session).github_topics(org, project)
            topic = resolved[0] if resolved else None
        owner, _, repo_name = repo.full_name.partition("/")

        creds = self._get_github_credentials(org)
        if not creds:
            raise ValueError(
                "No GitHub connection found for organization -- cannot remove "
                "the topic label from the repo on GitHub"
            )

        github_api = GitHubAPI(creds["token"])
        try:
            remaining_topics = await github_api.remove_repository_topic(
                owner, repo_name, topic
            )
        except Exception as e:
            logger.error(f"Failed to remove topic '{topic}' from {repo.full_name}: {e}")
            raise ValueError(f"Failed to remove topic from GitHub: {e}")

        now = datetime.now(timezone.utc)
        link.is_active = False
        link.removed_at = now
        self.session.add(link)

        add_timeline_entry(
            self.session,
            organization_id=organization_id,
            project_id=project_id,
            event_type=TimelineEventType.REPO_REMOVED,
            title="Repository removed from project",
            summary=f"{repo.name} was removed from the project ('{topic}' topic removed on GitHub).",
            created_by="system",
            metadata={"repository_id": repository_id, "removed_topic": topic},
        )

        self.session.commit()

        return {
            "project_id": project_id,
            "repository_id": repository_id,
            "removed_topic": topic,
            "remaining_topics": remaining_topics,
            "removed_at": now.isoformat(),
        }
