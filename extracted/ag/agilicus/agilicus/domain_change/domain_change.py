"""Org-scoped domain-bound inventory report (IAF-2368).

Thin client over the users service ``/v1/orgs/{org_id}/domain_change``
endpoint. The server-side ``plan_domain_change`` is the single source of truth
(shared with the 7.1 executor); the CLI only calls it and renders the report,
so this module must never re-implement the enumeration.

The endpoint is newer than the pinned generated SDK, so the request goes
through the generated organisation client's raw ``call_api`` (the same client,
token and CA as every other call), following ``platform/smoke/smoke/sdk.py``.
"""

import json
from typing import Any, Dict, List, Optional

from agilicus import context
from agilicus.agilicus_api import ApiException
from agilicus.archive.archive import DOMAIN_BOUND_OBJECT_TYPES
from agilicus.input_helpers import get_org_from_input_or_ctx

DOMAIN_CHANGE_PATH = "/v1/orgs/{org_id}/domain_change"


class DomainChangeError(Exception):
    """A domain-change request the server refused or could not answer."""


class DomainChangePreflightError(DomainChangeError):
    """A 409 preflight refusal, carrying the failing components/hosts."""

    def __init__(self, message, components=None, body=None):
        super().__init__(message)
        self.components = list(components or [])
        self.body = body


def preflight_components(body) -> List[Dict[str, Any]]:
    """Parse a 409 response body into the failing component/host records."""
    if not body:
        return []
    try:
        parsed = json.loads(body) if isinstance(body, (str, bytes)) else body
    except (TypeError, ValueError):
        return []
    if isinstance(parsed, dict):
        parsed = parsed.get("components") or parsed.get("failures") or [parsed]
    if not isinstance(parsed, list):
        return []
    return [item for item in parsed if isinstance(item, dict)]


def get_domain_change(ctx, org_id: str, new_subdomain: str) -> Dict[str, Any]:
    """Fetch the read-only report/proposal for *new_subdomain* (GET)."""
    return _call_domain_change(
        ctx,
        "GET",
        org_id,
        query_params=[("new_subdomain", new_subdomain)],
    )


def create_domain_change(
    ctx,
    org_id: str,
    subdomain: str,
    issuer_url: Optional[str] = None,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """Run the domain change (POST). ``dry_run=True`` returns the same plan."""
    body: Dict[str, Any] = {"subdomain": subdomain, "dry_run": dry_run}
    if issuer_url:
        body["issuer_url"] = issuer_url
    return _call_domain_change(ctx, "POST", org_id, body=body)


def plan_domain_change(
    ctx,
    org_id: Optional[str],
    new_subdomain: str,
    issuer_url: Optional[str] = None,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """Return the server's domain-change plan.

    ``dry_run`` (the default) never writes: when no ``issuer_url`` is given it
    uses the read-only ``GET`` report; when an issuer is given (which the
    server's ``GET`` does not carry) it falls back to ``POST`` with
    ``dry_run=true``. ``dry_run=False`` delegates to the 7.1 executor.
    """
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    if not org_id:
        raise ValueError(
            "an organisation id is required (pass --org-id or set an org context)"
        )
    if not new_subdomain:
        raise ValueError("a new subdomain is required (pass --new-subdomain)")

    if dry_run and issuer_url is None:
        return get_domain_change(ctx, org_id, new_subdomain)
    return create_domain_change(
        ctx,
        org_id,
        new_subdomain,
        issuer_url=issuer_url,
        dry_run=dry_run,
    )


def _call_domain_change(
    ctx,
    method: str,
    org_id: str,
    query_params: Optional[List[Any]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Issue the raw request against the users service.

    The generated SDK predates the route, so it has no typed method; the
    organisation client's ``api_client`` carries the configured host, token
    and CA, so ``call_api`` reaches the same endpoint as every other call.
    """
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"

    apiclient = context.get_apiclient(ctx)
    try:
        result = apiclient.org_api.api_client.call_api(
            DOMAIN_CHANGE_PATH,
            method,
            path_params={"org_id": org_id},
            query_params=list(query_params or []),
            header_params=headers,
            body=body,
            response_type=(dict,),
            auth_settings=["token-valid"],
            _return_http_data_only=True,
            _check_type=False,
        )
    except ApiException as exc:
        if getattr(exc, "status", None) == 409:
            raise DomainChangePreflightError(
                _describe(exc),
                components=preflight_components(getattr(exc, "body", None)),
                body=getattr(exc, "body", None),
            ) from exc
        raise DomainChangeError(_describe(exc)) from exc
    return result if isinstance(result, dict) else {"result": result}


def _describe(exc: Exception) -> str:
    status = getattr(exc, "status", None)
    reason = getattr(exc, "reason", None) or getattr(exc, "body", None)
    parts = [str(part) for part in (status, reason) if part]
    text = " ".join(parts) if parts else str(exc)
    return " ".join(text.split())[:300]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def ordered_counts(report: Dict[str, Any]) -> List[Any]:
    """The report's per-type counts, in the shared planner vocabulary order."""
    counts = report.get("counts") or {}
    known = list(DOMAIN_BOUND_OBJECT_TYPES)
    ordered = [name for name in known if name in counts]
    ordered.extend(sorted(name for name in counts if name not in ordered))
    return [(name, counts[name]) for name in ordered]


def summary_line(report: Dict[str, Any]) -> str:
    """A one-line human summary of a report."""
    counts = report.get("counts") or {}
    totals = (report.get("summary") or {}).get("totals") or {}
    objects = totals.get("objects")
    if objects is None:
        objects = sum(counts.values())
    return "{} object(s), {} change(s), {} warning(s) on {} -> {}".format(
        objects,
        len(report.get("changes") or []),
        len(report.get("warnings") or []),
        report.get("old_domain") or "?",
        report.get("new_domain") or "?",
    )
