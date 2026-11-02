"""Customer-feedback submission into the Jira Service Management CF board.

`submit_feedback` raises a customer request on the **Customer Feedback** JSM
project (key `CF`) via `POST /rest/servicedeskapi/request`, authenticating as a
dedicated Atlassian **service account** through an OAuth 2.0 client-credentials
grant (2LO) — the same auth shape `cube_common/apollo_client.py` already uses for
Apollo, so the credential lives in Secrets Manager and never leaves the cloud.

**The credential is deliberately write-only** — one scope, `write:servicedesk-
request` — and this module is built around that constraint rather than in spite
of it:

* It cannot read a service desk, a request type, or a field schema. A `GET` on
  `/rest/servicedeskapi/servicedesk` with this token returns 401 (verified live,
  2026-08-19). Every id in `_FORMS` is therefore **configuration, not discovery**.
* Consequence before you edit: **if the CF request forms change in Jira, the ids
  below go stale and the only symptom is a 400 from Atlassian.** Nothing here can
  self-heal and no test can catch it, because a write-only credential cannot
  introspect the form. Atlassian's 400 body does name the missing field by its
  human label ("Please provide a value for required field 'Role'"), so that text
  is surfaced verbatim rather than collapsed into a generic failure — it is the
  only diagnostic this credential can ever produce. Re-derive ids with
  `getJiraIssueTypeMetaWithFields` (or any read-scoped token) against project CF.

Two behaviors that look like details and are not:

1. **Text fields take plain strings here.** The same values sent to the core
   `POST /rest/api/3/issue` endpoint are rejected unless wrapped in Atlassian
   Document Format. `servicedeskapi` converts them for us, so there is no ADF
   serializer in this module and adding one would break it.
2. **The submitter's address is resolved server-side, not taken from the caller.**
   See `_submitter_email`.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import NamedTuple

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud._request_context import current_request
from cube_cloud.auth import api_keys
from cube_cloud.config import settings

logger = logging.getLogger(__name__)

TOKEN_URL = "https://auth.atlassian.com/oauth/token"

# Stamped on every ticket this tool creates, so triage can separate
# agent-submitted feedback from portal/email traffic with a `labels =` JQL clause.
# Deliberately a constant rather than config or a caller argument: "every request
# carries it" is the property being relied on, and either of those would let a
# submission opt out of the filter.
MCP_LABEL = "submitted-via-mcp"

# Stamped instead of MCP_LABEL when the submission came from the Edgeport Console
# rather than an MCP tool call, so triage can tell the two surfaces apart with the
# same kind of `labels =` JQL clause. Like MCP_LABEL, this is never a function
# argument — which internal entry point a caller used (`submit_feedback` vs
# `submit_feedback_from_console`) is what selects it, not anything in the request
# body, so it stays just as uncontrollable as the label it sits beside.
CONSOLE_LABEL = "submitted-via-console"


class _Origin(NamedTuple):
    """The three things that vary by which surface called in, bundled so a new
    surface can't update the label without also updating the other two.

    `default_role`/`submitted_via` are user-visible ticket content, not just
    triage metadata like `label` — a console submission previously inherited the
    MCP-facing wording for both ("Cube MCP user", "Submitted via cube-mcp
    submit_feedback.") even though nothing about that request went through MCP.
    """

    label: str
    default_role: str
    submitted_via: str


_MCP_ORIGIN = _Origin(MCP_LABEL, "Cube MCP user", "Submitted via cube-mcp send_feedback.")
_CONSOLE_ORIGIN = _Origin(
    CONSOLE_LABEL, "Edgeport Console user", "Submitted via the Edgeport Console.",
)

# Reporter-identity fields. Shared by all three CF forms.
_F_NAME = "customfield_10321"
_F_ROLE = "customfield_10322"
_F_EMAIL = "customfield_10323"


class _RequestForm(NamedTuple):
    """One CF request type and where its prose lands.

    The two forms do NOT share a body field: `bug` and `feature` each own a
    distinct pair of textareas. A single "description" mapping would validate
    for one type and 400 for the other.
    """

    request_type_id: str
    details_field: str
    impact_field: str


# Verified against createmeta for project CF, 2026-08-19.
_FORMS: dict[str, _RequestForm] = {
    "bug": _RequestForm("10294", "customfield_10324", "customfield_10325"),
    "feature": _RequestForm("10292", "customfield_10326", "customfield_10327"),
}

# CF's "Email request" type (10288) is intentionally absent: it is the type JSM
# stamps on tickets arriving through the inbound mail channel, not something a
# person should be able to raise from an agent.

FEEDBACK_TYPES = tuple(_FORMS)


class FeedbackError(Exception):
    """Raised when a feedback submission cannot be completed."""


# --------------------------------------------------------------------------
# Credential + token
# --------------------------------------------------------------------------


def _misconfigured(detail: str) -> FeedbackError:
    """Log an operator-facing detail; return a submitter-facing error.

    **The pass-through rule is about JIRA's errors, not ours.** Its 400s name the field
    it refused, which is the only diagnostic a write-only credential can produce, so
    those go through verbatim (`_explain_failure`). A credential-loading failure is
    different in both directions: the submitter cannot act on it, and the text named a
    Secrets Manager id — internal infrastructure detail that reached a customer's
    browser through `console/routes.py`, which returns `str(e)` in a 502 body and logs
    it as well.

    Exactly the treatment `freshservice.py::_misconfigured` already gives the sibling
    path, including keeping the secret id out of BOTH strings: it buys an operator
    almost nothing (a stack has one Jira secret, and its location is
    `settings.jira_oauth_secret`, readable from config) while logging it draws a
    high-severity CodeQL `py/clear-text-logging-sensitive-data` that every future
    reviewer has to re-triage.
    """
    logger.error("jira credential unavailable: %s", detail)
    return FeedbackError(
        "Feedback submission is not available right now. Please email "
        "help@edgescaleai.com directly."
    )


def _load_credentials() -> tuple[str, str]:
    """Read the service-account client id/secret from Secrets Manager.

    Secret value JSON: {"client_id": "...", "client_secret": "..."}.

    Every failure here goes through `_misconfigured`: the reason reaches CloudWatch,
    and the submitter is told what they can actually do about it.
    """
    if not settings.jira_oauth_secret:
        raise _misconfigured("no credential location is configured")

    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = client.get_secret_value(SecretId=settings.jira_oauth_secret)
    except ClientError as e:
        # AWS error CODE only, never the exception text: a Secrets Manager error can
        # echo request context, and this path runs on every submission.
        code = e.response.get("Error", {}).get("Code", "ClientError")
        raise _misconfigured(f"the configured secret could not be read ({code})") from e

    try:
        secret = json.loads(resp["SecretString"]) or {}
    except (ValueError, KeyError) as e:
        raise _misconfigured(
            'the configured secret is not JSON of the form '
            '{"client_id": "...", "client_secret": "..."}'
        ) from e
    client_id = secret.get("client_id", "")
    client_secret = secret.get("client_secret", "")
    if not client_id or not client_secret:
        raise _misconfigured(
            "the configured secret is missing 'client_id' or 'client_secret'"
        )
    return client_id, client_secret


class _TokenCache:
    """Process-lifetime cache for the 60-minute service-account access token.

    Single-flighted: feedback volume is low, but without the lock a burst would
    mint one token per concurrent call. Refreshes a minute early so a token can't
    expire mid-request.
    """

    def __init__(self) -> None:
        self._token: str | None = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    def clear(self) -> None:
        self._token = None
        self._expires_at = 0.0

    async def get(self, http: httpx.AsyncClient) -> str:
        async with self._lock:
            if self._token and time.monotonic() < self._expires_at:
                return self._token

            client_id, client_secret = _load_credentials()
            resp = await http.post(
                TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                headers={"content-type": "application/x-www-form-urlencoded"},
            )
            if resp.status_code != 200:
                # Body can echo the client_secret back on some error shapes.
                raise FeedbackError(
                    f"Jira token request failed ({resp.status_code})."
                )

            body = resp.json()
            token = body.get("access_token")
            if not token:
                raise FeedbackError("Jira token response carried no access_token.")

            expires_in = int(body.get("expires_in", 3600))
            self._token = token
            self._expires_at = time.monotonic() + max(expires_in - 60, 60)
            return token


_tokens = _TokenCache()


# --------------------------------------------------------------------------
# Submitter identity
# --------------------------------------------------------------------------


def _submitter_email(contact_email: str | None) -> str:
    """Resolve the reporter address, preferring the authenticated key over args.

    The browser-login key's description is the only place cube-cloud holds a
    cleartext address (`auth/api_keys.classify_actor` documents why it is never
    logged). Preferring it does two things worth keeping:

    * Attribution can't be spoofed by a tool argument.
    * On the common path there is **no cleartext email in the tool args at all**,
      so the telemetry archive keeps storing `user_domain` + `user_email_hash`
      rather than the address itself — the PII boundary issue #231 drew.

    `contact_email` is the fallback for a bot or CLI key with no address on file,
    and it is masked in telemetry (`telemetry/redaction.SENSITIVE_ARG_KEYS`) so
    taking the fallback does not quietly widen what the archive holds.
    """
    try:
        req = current_request.get()
    except LookupError:
        req = None

    if req is not None:
        derived = api_keys.email_from_description(
            getattr(req.state, "key_description", "") or ""
        )
        # "@" guards against a browser-login key whose description carries
        # the literal fallback `login_flow.py` writes when the Cognito token
        # had no email claim (`"Browser login: unknown"`) — `derived` is
        # truthy there, but "unknown" is not an address.
        if derived and "@" in derived:
            return derived

    if contact_email and "@" in contact_email:
        return contact_email.strip()

    if contact_email:
        raise FeedbackError(
            f"contact_email '{contact_email}' doesn't look like an email address."
        )
    raise FeedbackError(
        "No submitter email available. This key has no address on file "
        "(it is a bot or CLI key), so pass contact_email explicitly."
    )


def _context_block(cube: str | None, origin: _Origin) -> str:
    """Server-stamped provenance appended to the body.

    Everything here is read from the request, never from the caller — except
    `cube`, which is labelled as caller-supplied because nothing validates it.
    `origin.submitted_via` is also not caller-supplied: it is selected by which
    internal entry point was called, the same way `origin.label` is.
    """
    try:
        req = current_request.get()
    except LookupError:
        req = None

    lines = ["", "---", origin.submitted_via]
    if req is not None:
        profile = getattr(req.state, "profile", None)
        actor = getattr(req.state, "actor_type", None)
        if profile:
            lines.append(f"profile: {profile}")
        if actor:
            lines.append(f"actor: {actor}")
    if settings.env_name and settings.env_name != "unknown":
        lines.append(f"stack: {settings.env_name}")
    if cube:
        lines.append(f"cube (caller-supplied, unvalidated): {cube}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Tool
# --------------------------------------------------------------------------


# The MCP `send_feedback` tool's types, and where each one goes.
#
# ONE tool with a routing question, rather than two tools or one tool and one
# destination. The reason is that a person reporting something does not know or care
# which of our systems should hold it — but the answer matters a lot, because a
# helpdesk and a product backlog have different triage, different SLAs and different
# people reading them. So the agent asks a question the user CAN answer ("is this a
# problem, or an idea?") and the routing follows from it.
#
# `support` covers a problem, an observed bug, or a question — all three are support
# interactions and all three go to Freshservice, where there is an agent queue and a
# reply path. `feature` is a roadmap request and goes to the Jira CF board.
#
# Note this retires the Jira `bug` form for every caller: `_FORMS["bug"]` is still
# valid configuration and `_submit` still honours it, but no surface routes there any
# more. Left in place rather than deleted so restoring a Jira bug path is a routing
# change rather than a re-derivation of field ids the credential cannot introspect.
SEND_FEEDBACK_TYPES = ("support", "feature")

# The tool this replaced, kept as an accepted name rather than removed.
#
# **The local agent and cube-cloud deploy on different schedules, and only one of them
# is ours to move.** cube-cloud redeploys on every merge to `main`; the agent is a
# PyPI/npm package a developer upgrades whenever they choose, and it advertises its
# OWN bundled `REMOTE_TOOLS`, so an agent installed before this rename keeps offering
# `submit_feedback` and forwarding that name. Matching only the new name would answer
# those callers `"Unknown tool: submit_feedback"` — which is a 200 string, not an
# error, so the model relays it as prose and the user sees a confusing non-answer
# rather than a version problem. `telemetry/events.py` already keeps the old name for
# the same reason; the dispatcher has to agree.
#
# There is no deprecation window to wait out, because we cannot observe when the last
# old agent is gone. This stays until the analytics archive shows no `submit_feedback`
# calls for a long stretch — see `docs/tool-call-analytics-queries.md`.
LEGACY_TOOL_NAME = "submit_feedback"
TOOL_NAMES = ("send_feedback", LEGACY_TOOL_NAME)

# The old tool's `feedback_type` enum was `bug`/`feature`. `feature` is unchanged;
# `bug` has no direct successor because the routing question changed underneath it —
# "is this broken" and "do you have a problem or a question" are the same destination
# now. So `bug` maps to `support`, which sends it to the helpdesk that can reply to it
# rather than to a product backlog that cannot.
#
# Note what this does NOT do: it does not resurrect the Jira `bug` form. An old
# agent's bug report now goes where a new agent's would, so the two clients agree on
# destination and triage sees one queue instead of two. The alias is a compatibility
# shim for the NAME, not a second routing policy.
LEGACY_FEEDBACK_TYPES = {"bug": "support"}


def normalize_feedback_type(feedback_type: str) -> str:
    """Map a retired `feedback_type` onto its current one, or pass it through.

    Unknown values pass through untouched so `send_feedback` still produces its own
    "must be one of…" error rather than this silently absorbing a typo.
    """
    return LEGACY_FEEDBACK_TYPES.get(feedback_type, feedback_type)


async def send_feedback(
    feedback_type: str,
    summary: str,
    details: str,
    business_impact: str | None = None,
    cube: str | None = None,
    submitter_name: str | None = None,
    submitter_role: str | None = None,
    contact_email: str | None = None,
) -> str:
    """The single MCP feedback entry point. Routes by what the user actually has.

    `support` -> Freshservice (a problem, a bug, or a question).
    `feature` -> the Jira CF board (a roadmap request).

    Returns a human-readable string, like every other MCP tool handler — including on
    failure, since a tool that raises gives the agent nothing to relay.
    """
    if feedback_type not in SEND_FEEDBACK_TYPES:
        return (
            f"Error: feedback_type must be one of {', '.join(SEND_FEEDBACK_TYPES)}. "
            "Ask the user whether they have a problem, a bug or a question "
            "(support), or an idea for something new (feature)."
        )

    if feedback_type == "feature":
        # Unchanged Jira path, including its own business_impact requirement.
        return await submit_feedback(
            feedback_type,
            summary,
            details,
            business_impact,
            cube,
            submitter_name,
            submitter_role,
            contact_email,
        )

    # Imported at call time, not at module scope: `freshservice` imports THIS module
    # for `_submitter_email`, so a top-level import here would be circular.
    from cube_cloud.tools import freshservice as freshservice_tool

    try:
        ticket = await freshservice_tool.submit_support_request(
            profile=_profile_for_context(),
            summary=summary,
            details=details,
            business_impact=business_impact,
            cube=cube,
            submitter_role=submitter_role,
            contact_email=contact_email,
        )
    except freshservice_tool.FreshserviceError as e:
        return f"Error: {e}"

    # No ticket URL, for the same reason the Jira path returns none — see the
    # freshservice module docstring item 5.
    #
    # "Bug report", not "Support request", and no reply promise: this string is what
    # the agent relays to the user, so it is a customer-facing commitment in the same
    # way the console's copy is. See docs/console-spec.md 4.4e "Deferred: support
    # framing" — the destination is unchanged and working; the word is what there is
    # no on-call rotation to honour yet.
    return f"Bug report recorded: reference {ticket}"


def _profile_for_context() -> str:
    """The caller's profile for the ticket's provenance block, or "unknown".

    Read off the request context rather than taken as an argument, so it cannot be
    misreported — the same reason the reporter's email is resolved rather than passed.
    """
    try:
        req = current_request.get()
    except LookupError:
        return "unknown"
    if req is None:
        return "unknown"
    return str(getattr(req.state, "profile", "") or "unknown")


async def submit_feedback(
    feedback_type: str,
    summary: str,
    details: str,
    business_impact: str | None = None,
    cube: str | None = None,
    submitter_name: str | None = None,
    submitter_role: str | None = None,
    contact_email: str | None = None,
) -> str:
    """Raise a bug / feature request on the CF board."""
    try:
        key = await _submit(
            feedback_type,
            summary,
            details,
            business_impact,
            cube,
            submitter_name,
            submitter_role,
            contact_email,
        )
    except FeedbackError as e:
        return f"Error: {e}"

    # No browse link: the submitter has no JSM agent seat (see the module
    # docstring's identity note), so a `/browse/<key>` URL is a dead link for
    # every caller, not just an external one — it only ever resolves for
    # someone who already has their own Jira login. The key is still useful as
    # a reference number for an out-of-band follow-up.
    return f"Feedback submitted: {key} ({feedback_type})"


async def submit_feedback_from_console(
    feedback_type: str,
    summary: str,
    details: str,
    business_impact: str | None = None,
    cube: str | None = None,
    submitter_name: str | None = None,
    submitter_role: str | None = None,
) -> str:
    """The Edgeport Console's entry point into this module. Returns the ticket key.

    Two differences from `submit_feedback`, both deliberate:

    1. **No `contact_email` parameter.** The console form never collects an email
       address at all — the submitter is always resolved server-side from the
       cookie-authenticated request's key (`_submitter_email`, same as the MCP
       path), and there is no fallback here for a key with no address on file
       (the console is browser-login only, so that case cannot arise). Omitting
       the parameter rather than accepting-and-ignoring it means a caller cannot
       even try to pass one through.
    2. **Raises `FeedbackError` rather than formatting it into an `"Error: ..."`
       string** — the console's HTTP route needs a plain value for its JSON
       response, not text meant for an agent transcript.

    Stamps `_CONSOLE_ORIGIN` instead of `_MCP_ORIGIN` — hardcoded here, not
    threaded from a caller, so triage (and the ticket body's own provenance line)
    can trust it the same way they trust the MCP path's.
    """
    return await _submit(
        feedback_type,
        summary,
        details,
        business_impact,
        cube,
        submitter_name,
        submitter_role,
        None,
        origin=_CONSOLE_ORIGIN,
    )


async def _submit(
    feedback_type: str,
    summary: str,
    details: str,
    business_impact: str | None,
    cube: str | None,
    submitter_name: str | None,
    submitter_role: str | None,
    contact_email: str | None,
    *,
    origin: _Origin = _MCP_ORIGIN,
) -> str:
    if not settings.jira_enabled:
        raise FeedbackError(
            "Feedback submission is disabled on this stack "
            "(CUBE_CLOUD_JIRA_ENABLED is false)."
        )
    if not settings.jira_cloud_id or not settings.jira_service_desk_id:
        raise FeedbackError(
            "Jira is not configured: CUBE_CLOUD_JIRA_CLOUD_ID and "
            "CUBE_CLOUD_JIRA_SERVICE_DESK_ID must both be set."
        )

    form = _FORMS.get(feedback_type)
    if form is None:
        raise FeedbackError(
            f"Unknown feedback_type '{feedback_type}'. "
            f"Expected one of: {', '.join(FEEDBACK_TYPES)}."
        )

    summary = (summary or "").strip()
    details = (details or "").strip()
    if not summary:
        raise FeedbackError("summary is required.")
    if not details:
        raise FeedbackError("details is required.")

    impact = (business_impact or "").strip()
    if not impact:
        raise FeedbackError(
            f"business_impact is required for feedback_type '{feedback_type}'."
        )

    email = _submitter_email(contact_email)
    name = (submitter_name or "").strip() or email.split("@", 1)[0]
    role = (submitter_role or "").strip() or origin.default_role

    body = details + _context_block(cube, origin)

    fields: dict[str, object] = {
        "summary": summary,
        _F_NAME: name,
        _F_ROLE: role,
        _F_EMAIL: email,
        form.details_field: body,
        form.impact_field: impact,
        "labels": [origin.label],
    }

    payload = {
        "serviceDeskId": settings.jira_service_desk_id,
        "requestTypeId": form.request_type_id,
        "requestFieldValues": fields,
    }

    url = (
        f"https://api.atlassian.com/ex/jira/{settings.jira_cloud_id}"
        f"/rest/servicedeskapi/request"
    )

    async with httpx.AsyncClient(timeout=30) as http:
        token = await _tokens.get(http)
        resp = await http.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        if resp.status_code == 401:
            # Either the token aged out mid-flight or the credential's scope
            # changed. Drop the cache so the next call re-mints rather than
            # replaying a dead token for the rest of the process's life.
            _tokens.clear()
            raise FeedbackError(
                "Jira rejected the credential (401). The service account's scope "
                "must include write:servicedesk-request."
            )
        if resp.status_code >= 400:
            raise FeedbackError(_explain_failure(resp))

        created = resp.json()

    key = created.get("issueKey", "")
    if not key:
        raise FeedbackError("Jira accepted the request but returned no issue key.")

    return key


def _explain_failure(resp: httpx.Response) -> str:
    """Turn Atlassian's error body into the most actionable message available.

    Atlassian names missing fields by their human label, which is the ONLY
    diagnostic a write-only credential can produce — it cannot read the form to
    say more. Pass that text through verbatim and name the stale-id failure mode,
    since that is what a 400 here usually means.
    """
    detail = ""
    try:
        detail = (resp.json() or {}).get("errorMessage", "") or ""
    except ValueError:
        detail = ""
    detail = detail.strip() or resp.text[:300].strip()

    hint = ""
    if resp.status_code == 400:
        hint = (
            " If this names a field, the CF request form changed in Jira and the "
            "ids in tools/feedback.py are stale."
        )
    return f"Jira rejected the submission ({resp.status_code}): {detail}{hint}"
