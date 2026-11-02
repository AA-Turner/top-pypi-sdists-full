"""Support-request submission into Freshservice — the console's "problem or question".

The console's feedback form has two paths. A **feature request** still raises a
customer request on the Jira CF board (`tools/feedback.py`, unchanged). A **problem or
question** raises a ticket here instead, because that is a support interaction and
Freshservice is the helpdesk that has an agent queue, SLAs and a requester portal
behind it — none of which the CF board offers (see `feedback.py` item 6: the Jira
service account has no agent seat, so a Jira submitter gets no thread and no reply
notifications).

Five things about this integration are load-bearing.

1. **The domain is CONFIGURATION and must not be derived from the product name.** The
   product is "Edgeport"; the Freshservice tenant is `edgescaleai.freshservice.com`.
   `edgeport.freshservice.com` returns 404 — verified by probing both, rather than
   assuming the obvious one. `settings.freshservice_domain` carries it and has no
   default that names a tenant.

2. **The credential cannot introspect the field contract**, so the request shape is
   configuration rather than discovery. Verified live (2026-08-27): the key reads
   `GET /api/v2/tickets` (200) but `GET /api/v2/ticket_fields` returns
   `403 access_denied`. Exactly the same class of limitation as the Jira write-only
   credential, and it has the same consequence: **if Freshservice's required fields
   change, the only symptom is a 400 in production** and no test can catch it, because
   the credential cannot ask. `_explain_failure` therefore passes Freshservice's own
   error text through rather than collapsing it into "submission failed".

3. **The requester email is resolved server-side, and that is a PII boundary as much
   as an anti-spoof one.** It reuses `feedback._submitter_email`, so the address comes
   from the authenticated key's `"Browser login: <email>"` description and never from
   a request field. Reusing rather than reimplementing matters: a second copy of that
   resolution would be a second place for the boundary to drift. Freshservice
   *requires* a requester identifier, so unlike the Jira path there is no submitting
   without one — a bot/CLI key with no address on file is refused rather than
   silently attributed to someone.

4. **Every ticket is tagged `submitted-via-console`** (`CONSOLE_TAG`), the same literal
   the Jira integration uses as a label. Triage filters key on that exact string across
   both systems, so renaming it orphans saved views silently. It is a module constant
   rather than a caller argument for the same reason it is over there: "every request
   carries one" is the property being relied on, and an argument would let a submission
   opt out.

5. **No ticket URL is returned**, only the id. Freshservice *does* give a requester a
   portal thread, unlike Jira — but whether a given user can open it depends on how
   the tenant's portal access is configured, which this credential cannot check
   (item 2). Returning a link that 403s for the person who just filed the ticket is
   worse than returning none, so this follows the decision `feedback.py` item 8
   records: hand back a reference number and let the reply arrive by email.
"""

from __future__ import annotations

import base64
import html
import json
import logging

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud.config import settings
from cube_cloud.tools import feedback as feedback_tool

logger = logging.getLogger(__name__)

# Tags identifying which surface filed the ticket. Cross-system contracts with triage:
# the Jira integration applies the SAME two literals as labels, so one `tags`/`labels`
# clause separates agent-submitted from console-submitted traffic in either system.
#
# Like the Jira labels, neither is ever a function argument — which internal entry
# point was called selects it, not anything in the request body, so a submission cannot
# opt out of being attributed to its surface.
CONSOLE_TAG = "submitted-via-console"
MCP_TAG = "submitted-via-mcp"

# Freshservice enums, from the published API reference (the credential cannot read
# `ticket_fields` to confirm them — item 2).
_STATUS_OPEN = 2
_PRIORITY_MEDIUM = 2
# 2 = Portal. The submission comes from our own web form, not Freshservice's embedded
# feedback widget (5) — that distinction is what a support agent uses to know where a
# ticket came from, so it is worth getting right rather than defaulting.
_SOURCE_PORTAL = 2

_TIMEOUT_SECONDS = 20.0


class FreshserviceError(Exception):
    """A support request could not be filed. Message is safe to show the submitter."""


def is_enabled() -> bool:
    """Whether the Freshservice path is wired up on this stack.

    Read per call rather than captured at import, like every other flag here — an
    import-time value cannot be patched in a test and needs a restart to change.
    """
    return bool(settings.freshservice_enabled)


_key_cache: str | None = None


def _load_api_key() -> str:
    """The Freshservice API key, from Secrets Manager. Cached on success only.

    Secret value JSON: ``{"api_key": "..."}``.

    `CUBE_CLOUD_FRESHSERVICE_API_KEY` overrides it for local development, warned about
    on every resolve — Terraform must never set it, because an ECS task-definition
    environment variable is readable via `ecs:DescribeTaskDefinition` and is printed by
    `terraform plan`. Same rule and reason as the inventory bearer.

    Caching only on success is deliberate: a failed read caches nothing, so creating
    the secret takes effect on the next submission instead of needing a redeploy.
    """
    global _key_cache
    if _key_cache:
        return _key_cache

    if settings.freshservice_api_key:
        logger.warning(
            "Freshservice key came from CUBE_CLOUD_FRESHSERVICE_API_KEY, not Secrets "
            "Manager. That is for local development only — an ECS task-definition env "
            "var is readable via ecs:DescribeTaskDefinition."
        )
        _key_cache = settings.freshservice_api_key
        return _key_cache

    ref = settings.freshservice_api_key_secret
    if not ref:
        raise _misconfigured("no API key location is configured")
    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = client.get_secret_value(SecretId=ref)
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "ClientError")
        raise _misconfigured(f"the configured secret could not be read ({code})") from e
    try:
        key = (json.loads(resp["SecretString"]) or {}).get("api_key", "")
    except (ValueError, KeyError) as e:
        raise _misconfigured(
            'the configured secret is not JSON of the form {"api_key": "..."}'
        ) from e
    if not key:
        raise _misconfigured("the configured secret is missing 'api_key'")
    _key_cache = key
    return key


def _misconfigured(detail: str) -> FreshserviceError:
    """Log an operator-facing detail; return a submitter-facing error.

    **The pass-through rule in item 2 is about FRESHSERVICE's errors, not ours.** Its
    400s name the field it refused, which is the only diagnostic this credential can
    produce, so those go through verbatim. A credential-loading failure is different in
    both directions: the submitter cannot act on it, and the text names a Secrets
    Manager id — internal infrastructure detail that has no business reaching a
    customer's browser through `routes.py`'s 502 body.

    So the reason and the AWS error code go to CloudWatch, where the person who can fix
    it is looking, and the submitter is told what they need: this is not working, use
    the address instead.

    **The Secrets Manager id is deliberately NOT in either string.** It was, briefly,
    on the grounds that it helps an operator — and CodeQL flagged the log call
    `py/clear-text-logging-sensitive-data`, high severity. No secret VALUE was ever
    logged, only the id, so the alert is imprecise about what leaked. It is still the
    right call to defer to: the id buys an operator almost nothing (a stack has exactly
    one Freshservice secret, and its location is `settings.freshservice_api_key_secret`,
    readable from config), while keeping it means carrying a standing high-severity
    alert that every future reviewer has to re-triage. Log the reason and the AWS code,
    which is the part that is actually actionable.
    """
    logger.error("freshservice credential unavailable: %s", detail)
    return FreshserviceError(
        "Support requests are not available right now. Please email "
        "help@edgescaleai.com directly."
    )


def reset_key_cache() -> None:
    """Drop the cached key. For tests, and for a local credential swap."""
    global _key_cache
    _key_cache = None


def _base_url() -> str:
    domain = (settings.freshservice_domain or "").strip().rstrip("/")
    if not domain:
        raise FreshserviceError("Freshservice is enabled but no domain is configured.")
    # Accept a bare domain or a full origin, so a tfvar carrying either works.
    if domain.startswith("http://") or domain.startswith("https://"):
        return domain
    return f"https://{domain}"


def _auth_header(key: str) -> str:
    """HTTP Basic with the API key as the username and any password.

    Freshservice's documented scheme (`-u api_key:X`). The password is ignored, so "X"
    is the conventional placeholder rather than a secret in its own right.
    """
    return "Basic " + base64.b64encode(f"{key}:X".encode()).decode()


def _explain_failure(status: int, body: str) -> str:
    """A message the submitter can act on, keeping Freshservice's own words.

    The 400 case is the one that matters. Per item 2 this credential cannot introspect
    the field contract, so a required-field change surfaces *only* as a 400 whose body
    names the offending field — collapsing that into "submission failed" would discard
    the single diagnostic this integration can ever produce.
    """
    detail = (body or "").strip()[:400]
    if status == 400:
        return (
            "Freshservice rejected the request as invalid. This usually means its "
            "required fields have changed and the integration needs updating. "
            f"Freshservice said: {detail}"
        )
    if status in (401, 403):
        return (
            "Freshservice rejected our credentials. The API key may have been "
            "revoked or may lack permission to create tickets."
        )
    if status == 404:
        return (
            "Freshservice returned 404 — check the configured domain. The product "
            "name and the Freshservice subdomain are not the same thing."
        )
    if status == 429:
        return "Freshservice is rate-limiting us. Please try again in a minute."
    return f"Freshservice returned {status}. {detail}".strip()


def _tags(surface_tag: str) -> list[str]:
    """The ticket's tags: which surface filed it, and which stack it came from.

    The surface tag is the cross-system contract (item 4). The **stack** tag is what
    makes a shared queue workable: there is exactly one Freshservice tenant for both
    dev and prod, so without something filterable, dev test submissions and real
    customer incidents land in one undifferentiated list. The body carries the same
    fact, but a body line cannot be filtered on — a triager would have to open every
    ticket to sort them.

    `stack-<env>` is a small closed set (`stack-dev`, `stack-prod`) and, like the
    surface tag, is never a caller argument: it is read from `settings.env_name`, which
    Terraform sets on the task, so a submission cannot claim to be from another stack.
    Guarded the same way the body line is — a stack with no `CUBE_CLOUD_ENV_NAME` adds
    no tag rather than a literal `stack-unknown`.
    """
    tags = [surface_tag]
    if settings.env_name and settings.env_name != "unknown":
        tags.append(f"stack-{settings.env_name}")
    return tags


def _ticket_body(
    details: str,
    business_impact: str | None,
    cube: str | None,
    profile: str,
    submitted_via: str,
    submitter_role: str | None = None,
) -> str:
    """The ticket description, as **HTML** — every interpolated value escaped.

    **`description` is an HTML field, and that governs the caller's text as well as
    ours.** An earlier revision knew the first half and acted only on the second: it
    said "Freshservice renders HTML in `description`, so this is deliberately simple
    rather than marked up" and then `\\n`-joined raw `details`, `business_impact`,
    `cube` and `submitter_role` into it. Two things followed, and neither was
    cosmetic. Every newline was dropped, collapsing the provenance block into the
    submitter's prose. And an authenticated submitter could put markup into a
    helpdesk agent's browser — at minimum a link or an image, and more to the point
    they could forge or comment out the provenance block below, which is the only
    thing on the ticket saying who actually filed it.

    The Jira sibling never had this exposure: `servicedeskapi` takes plain strings and
    converts them server-side (`feedback.py` item 2). Nothing converts for us, so the
    escaping is ours to do.

    **Why not `description_text`.** Freshdesk accepts a plain-text field on create;
    Freshservice documents `description` as the HTML one and `description_text` as a
    read attribute. Sending an unproven field with a credential that **cannot
    introspect its own schema** (module docstring item 1) risks a silently-empty
    ticket body, and no test can catch that — a wrong-but-accepted field is a 201.
    Escaping the documented field is the option whose failure mode we can see.

    **Caller-supplied values in the provenance block are labelled as such.** `profile`
    is resolved server-side from the request context and can be trusted; `Role` and
    `Cube` are tool arguments the caller chose. The Jira builder already marks its one
    untrusted field `cube (caller-supplied, unvalidated)` — matching that here matters
    more, not less, because an agent reading a Freshservice ticket has no other way to
    tell the two kinds of line apart.

    `business_impact` is OPTIONAL here and required on the Jira feature form. That
    asymmetry is deliberate: "who is blocked and what does it cost" is a reasonable
    thing to demand of a roadmap request and pure friction in front of a question.
    """
    parts = [f"<p>{_html(details.strip())}</p>"]
    if (business_impact or "").strip():
        parts.append(
            f"<p><b>Impact:</b><br>{_html(business_impact.strip())}</p>"
        )

    # Server-resolved first, then the caller-supplied lines, each marked. Order is
    # deliberate: what we know precedes what we were told.
    context = [f"Profile: {_html(profile)}"]

    # WHICH STACK filed this. The Jira builder has always carried it
    # (`feedback.py::_context_block`) and this one did not, which was an oversight
    # rather than a decision — and it matters more here, not less: there is exactly
    # ONE Freshservice tenant, shared by dev and prod, so without this line a triager
    # cannot tell a dev test submission from a real customer's incident. Same
    # `!= "unknown"` guard as the Jira side, so a stack that never had CUBE_CLOUD_
    # ENV_NAME set prints nothing rather than the literal "unknown".
    if settings.env_name and settings.env_name != "unknown":
        context.append(f"Stack: {_html(settings.env_name)}")

    if submitter_role:
        context.append(f"Role (caller-supplied): {_html(submitter_role)}")
    if cube:
        context.append(f"Cube (caller-supplied, unvalidated): {_html(cube)}")
    context.append(_html(submitted_via))
    parts.append(f"<hr><p>{'<br>'.join(context)}</p>")
    return "".join(parts)


def _html(value: str) -> str:
    """Escape a value for the HTML ticket body, preserving its line breaks.

    `quote=True` so an attribute-shaped payload cannot break out even if this text is
    ever interpolated somewhere with attributes. Newlines become `<br>` AFTER escaping,
    so a literal `<br>` a submitter typed stays visible text rather than becoming
    markup.
    """
    return html.escape(value, quote=True).replace("\n", "<br>")


async def submit_support_request_from_console(
    profile: str,
    summary: str,
    details: str,
    business_impact: str | None = None,
    cube: str | None = None,
) -> str:
    """The CONSOLE entry point. Returns the ticket id as a string.

    No `contact_email` parameter, deliberately: the console form collects no address
    ever, so there is nothing to fall back to and nothing a caller could spoof.
    """
    return await _create(
        profile=profile,
        summary=summary,
        details=details,
        business_impact=business_impact,
        cube=cube,
        tag=CONSOLE_TAG,
        submitted_via="Submitted via the Edgeport Console.",
        contact_email=None,
        submitter_role=None,
    )


async def submit_support_request(
    profile: str,
    summary: str,
    details: str,
    business_impact: str | None = None,
    cube: str | None = None,
    submitter_role: str | None = None,
    contact_email: str | None = None,
) -> str:
    """The MCP entry point, for `send_feedback`'s support path.

    Differs from the console entry point in exactly the two ways the Jira pair differ:
    a different surface tag, and a `contact_email` fallback for a bot or CLI key with
    no address on file. That fallback is in `telemetry.redaction.SENSITIVE_ARG_KEYS`,
    so taking it does not widen what the telemetry archive stores.
    """
    return await _create(
        profile=profile,
        summary=summary,
        details=details,
        business_impact=business_impact,
        cube=cube,
        tag=MCP_TAG,
        submitted_via="Submitted via cube-mcp send_feedback.",
        contact_email=contact_email,
        submitter_role=submitter_role,
    )


async def _create(
    *,
    profile: str,
    summary: str,
    details: str,
    business_impact: str | None,
    cube: str | None,
    tag: str,
    submitted_via: str,
    contact_email: str | None,
    submitter_role: str | None,
) -> str:
    """File the ticket. Shared by both entry points so the payload has one builder."""
    if not is_enabled():
        raise FreshserviceError(
            "Support requests are not configured on this deployment."
        )

    # Reuses the Jira path's resolver so the identity boundary has ONE implementation.
    # `None` because there is no caller-supplied fallback on the console path at all.
    #
    # It RAISES rather than returning empty when the key has no address on file, and
    # its message is written for the MCP caller — it says to "pass contact_email
    # explicitly", which is a field the console form does not have and a concept a
    # browser user has no way to act on. So the failure is re-authored here rather than
    # forwarded, while the resolution itself stays shared.
    try:
        email = feedback_tool._submitter_email(contact_email)
    except feedback_tool.FeedbackError as e:
        # CLASS NAME ONLY, never `e`. One of that function's two failure messages
        # interpolates the rejected address verbatim ("contact_email '<addr>' doesn't
        # look like an email address"), so logging the text would put a cleartext user
        # address into CloudWatch — the exact thing issue #231 keeps out of the
        # telemetry archive, arriving by a side door. Same class-name-only rule as
        # `console/routes.py::_log_write_failure`.
        logger.info("freshservice: no submitter address on file (%s)", type(e).__name__)
        email = ""
    if not email or "@" not in email:
        # Freshservice requires a requester identifier, so there is no submitting
        # anonymously. Refusing beats attributing the ticket to a service account,
        # which would put a real person's problem behind an address nobody reads.
        raise FreshserviceError(
            "We could not determine your email address, so the request was not "
            "submitted. Please email help@edgescaleai.com directly."
        )

    payload = {
        "email": email,
        "subject": summary.strip(),
        "description": _ticket_body(
            details, business_impact, cube, profile, submitted_via, submitter_role,
        ),
        "status": _STATUS_OPEN,
        "priority": _PRIORITY_MEDIUM,
        "source": _SOURCE_PORTAL,
        "tags": _tags(tag),
    }

    key = _load_api_key()
    url = f"{_base_url()}/api/v2/tickets"
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT_SECONDS) as http:
            resp = await http.post(
                url,
                json=payload,
                headers={
                    "Authorization": _auth_header(key),
                    "Content-Type": "application/json",
                },
            )
    except httpx.HTTPError as e:
        raise FreshserviceError(
            f"Could not reach Freshservice ({type(e).__name__})."
        ) from e

    if resp.status_code in (401, 403):
        # Drop the cached key so a rotated secret takes effect on the next attempt
        # rather than needing a redeploy.
        reset_key_cache()

    if resp.status_code != 201:
        raise FreshserviceError(_explain_failure(resp.status_code, resp.text))

    try:
        ticket = (resp.json() or {}).get("ticket") or {}
    except ValueError as e:
        raise FreshserviceError("Freshservice returned a non-JSON response.") from e

    ticket_id = ticket.get("id")
    if not ticket_id:
        # A 201 with no id is not something to paper over: the caller is about to show
        # the user a reference number.
        raise FreshserviceError(
            "Freshservice accepted the request but returned no ticket id."
        )
    return str(ticket_id)
