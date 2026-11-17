"""HTTP client for the RBAC service. Fails closed: any doubt is an exception, never an allow.

Modelled on `inventory/client.py` (Secrets Manager key cached per process, a local
override for a laptop, `httpx` with a short timeout) with one difference that matters:
inventory degrades to blank fields, while every caller of this module treats
`RbacServiceError` as a refusal. A reader that guessed at an authorization answer would
be worse than one that shows an error.

**Nothing from a response body is logged.** The catalog names every customer that owns
a product, which the service treats as tenancy data; a log line is a place it would
outlive the request. Status codes only, as `console/reads.py` does for `ApolloError`.

The contract is the service's own `docs/consumer-guide.md` and the `_catalog_route`
handler it describes (AGENTS.md rule 9): `GET /v1/products` with `x-api-key` and
`x-rbac-subject` answers 200 with `{allow, scope, items}` whether or not the person is
allowed, `scope == ["*"]` when they hold any EdgeScale grant, and items of
`{productId, owner, source, access, shares?}` (a share recipient's rows carry
`{productId, access: "share", role}` and no owner).

The four product writes (`reassign`, `declare`, `grant_share`, `revoke_share`) need a
key with `products:write`, and the service decides each one on the person named: an
EdgeScale read-only grant reads the catalog but is refused every write. A refusal is
an answer (`Written.ok` False, with the service's words), not an exception.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from urllib.parse import quote

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud.config import settings

logger = logging.getLogger(__name__)

#: The service's own spelling of "every company": what `scope` holds for a person
#: with any EdgeScale grant. Any grant, read-only included — so this means "EdgeScale
#: staff", never "admin"; the service decides each write separately.
STAR = "*"

#: The only domain whose people the console asks about. A pre-check, so nobody else's
#: page load ever reaches the service; the service's own answer is what decides.
EDGESCALE_DOMAIN = "edgescaleai.com"

_key: str | None = None


class RbacServiceError(Exception):
    """The service could not be asked, or its answer could not be read. A refusal."""


class KeyRefused(RbacServiceError):
    """The service answered 401 or 403: it refused this stack's key, or the key's scopes
    or domains do not cover the request. It acted on nothing, so a write it refused
    certainly did not happen, unlike a timeout."""


@dataclass(frozen=True)
class Catalog:
    """One person's `GET /v1/products` answer."""

    allow: bool
    scope: tuple[str, ...]
    items: list[dict] = field(default_factory=list)
    # The service's word for a refusal ("no grant in scope"), for the log only. It names
    # a rule, never a company or a product.
    reason: str = ""

    @property
    def internal(self) -> bool:
        """The person holds an EdgeScale grant, so `items` is the whole catalog."""
        return self.allow and STAR in self.scope


@dataclass(frozen=True)
class Written:
    """The outcome of one product write the service answered.

    `ok` is False when the service refused (no permission, `allow: false`) or turned the
    request down (an unknown customer, an owner already set, a share that is not
    there), and `message` then holds its reason or error, cut short. Those are rule
    names and validation errors; the one that names a company (409 "product already
    has an owner") is shown only to EdgeScale staff, the only callers.
    """

    ok: bool
    status: int
    body: dict = field(default_factory=dict)
    message: str = ""


def is_enabled() -> bool:
    """Read per call, never captured at import, as `inventory.is_enabled` is."""
    return bool(settings.rbac_service_enabled)


def is_edgescale(email: str | None) -> bool:
    return bool(email) and email.rsplit("@", 1)[-1] == EDGESCALE_DOMAIN


def _reset() -> None:
    """Forget the cached key. For tests; `catalog` does it itself on a 401 or 403."""
    global _key
    _key = None


def _load_key() -> str:
    """This stack's key, from Secrets Manager as {"api_key": "..."}. Cached for the process
    until the service rejects it."""
    global _key
    if _key:
        return _key
    if settings.rbac_service_key:
        logger.warning(
            "rbac-service key came from CUBE_CLOUD_RBAC_SERVICE_KEY, not Secrets "
            "Manager. That is intended for local development only."
        )
        _key = settings.rbac_service_key
        return _key
    ref = settings.rbac_service_key_secret
    if not ref:
        raise RbacServiceError(
            "rbac_service_key_secret is unset (Terraform sets "
            "CUBE_CLOUD_RBAC_SERVICE_KEY_SECRET on ECS)."
        )
    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = client.get_secret_value(SecretId=ref)
    except ClientError as e:
        raise RbacServiceError(
            f"Could not read the rbac-service key from {ref}: "
            f"{e.response.get('Error', {}).get('Code', 'ClientError')}"
        ) from e
    try:
        key = (json.loads(resp["SecretString"]) or {}).get("api_key", "")
    except (ValueError, KeyError, TypeError) as e:
        raise RbacServiceError(
            f'The rbac-service secret {ref} is not JSON of the form {{"api_key": "..."}}.'
        ) from e
    if not key:
        raise RbacServiceError(f"The rbac-service secret {ref} is missing 'api_key'.")
    _key = key
    return key


def _base() -> str:
    base = (settings.rbac_service_api_base or "").strip().rstrip("/")
    if not base.startswith("https://"):
        raise RbacServiceError("rbac_service_api_base is unset or not https.")
    return base


def _pid(product_id: str) -> str:
    # Product ids hold `:` and may hold `/`; the service wants them URL-encoded.
    return quote(product_id, safe="")


async def _send(method: str, path: str, subject: str, body: dict | None = None) -> httpx.Response:
    """One request as `subject`. Raises `RbacServiceError` for everything that is not an
    answer about the request: no subject, no key, unreachable, 401 or 403, or a 5xx."""
    if not subject or "@" not in subject:
        raise RbacServiceError("no verified subject to ask about")
    # Secrets Manager is a blocking call, and on a stack whose secret is still empty it
    # repeats on every read (a failure caches nothing), as inventory's does.
    headers = {"x-api-key": await asyncio.to_thread(_load_key), "x-rbac-subject": subject}
    try:
        async with httpx.AsyncClient(timeout=settings.rbac_service_timeout_seconds) as http:
            resp = await http.request(method, f"{_base()}{path}", headers=headers, json=body)
    except httpx.HTTPError as e:
        raise RbacServiceError(f"rbac-service unreachable ({type(e).__name__})") from e
    if resp.status_code in (401, 403):
        # A rotated, disabled or under-scoped key. Drop it, as inventory drops its
        # bearer, so a new value put in Secrets Manager is read on the next request
        # rather than after a redeploy. (403 is also a subject outside the key's
        # `subject_domains`, or a write with a read-only key; re-reading the key then
        # costs one Secrets Manager call.)
        _reset()
        raise KeyRefused(
            f"rbac-service refused the key or this request ({resp.status_code}: a bad "
            "or disabled key, a missing `products:read`, `products:write`, `decide` or "
            "`customers:read` scope, or a "
            "subject outside the key's domains); the key will be re-read from Secrets "
            "Manager next time"
        )
    if resp.status_code >= 500:
        raise RbacServiceError(f"rbac-service answered {resp.status_code}")
    return resp


async def _write(method: str, path: str, subject: str, body: dict | None = None) -> Written:
    """A product write. A 2xx is done unless its body says `allow: false`; 404, 409 and
    422 are the service turning the request down; anything else raises."""
    resp = await _send(method, path, subject, body)
    try:
        answer = resp.json() if resp.content else {}
    except ValueError as e:
        raise RbacServiceError("rbac-service answered with something other than JSON") from e
    if not isinstance(answer, dict):
        raise RbacServiceError("rbac-service answer is not an object")
    said = answer.get("reason") or answer.get("error")
    message = said[:160] if isinstance(said, str) else ""
    if 200 <= resp.status_code < 300:
        if answer.get("allow") is False:
            return Written(False, resp.status_code, answer, message or "not allowed")
        return Written(True, resp.status_code, answer)
    if resp.status_code in (404, 409, 422):
        return Written(False, resp.status_code, answer, message or f"rejected ({resp.status_code})")
    raise RbacServiceError(f"rbac-service answered {resp.status_code}")


async def may(subject: str, action: str, company: str) -> bool:
    """`POST /v1/decide` as `subject`: whether they may take `action` on `company`'s
    resources. The service resolves the person's role; nothing here infers one. Needs a
    key with the `decide` scope, and a 401/403 (a key without it) raises `KeyRefused`."""
    resp = await _send("POST", "/v1/decide", subject, {"action": action, "company": company})
    if resp.status_code != 200:
        raise RbacServiceError(f"rbac-service answered {resp.status_code}")
    try:
        answer = resp.json()
    except ValueError as e:
        raise RbacServiceError("rbac-service answered with something other than JSON") from e
    if not isinstance(answer, dict):
        raise RbacServiceError("rbac-service answer is not an object")
    return answer.get("allow") is True


async def tag(subject: str, product_id: str) -> dict | None:
    """`GET /v1/products/{id}` as `subject`: the product's tag as the service holds it
    NOW, uncached (`{productId, owner, source, shares?}`), or None when the service
    answers 404 (not visible to `subject`). A product with no row reads as owned by
    `internal`, as the service's rules have it.

    The catalog is cached for `rbac_service_cache_ttl_seconds`, per ECS task; this is
    the read for a check that cannot take a cached answer, such as the owner a change
    is about to replace."""
    resp = await _send("GET", f"/v1/products/{_pid(product_id)}", subject)
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        raise RbacServiceError(f"rbac-service answered {resp.status_code}")
    try:
        answer = resp.json()
    except ValueError as e:
        raise RbacServiceError("rbac-service answered with something other than JSON") from e
    if not isinstance(answer, dict):
        raise RbacServiceError("rbac-service answer is not an object")
    return answer


async def customers(subject: str) -> list[dict]:
    """`GET /v1/customers` as `subject`: the enabled companies their scope covers, as
    `[{company, display_name}]` sorted by key. Every enabled company for an EdgeScale
    person; never the internal tenant or `shared`, which are fixed names. Needs the
    key's `customers:read` scope (a key without it raises `KeyRefused`). It is the list
    a tag edit picks a company from: a company that is not in it has to be created on
    the service first, and the service refuses an owner or share naming one anyway."""
    resp = await _send("GET", "/v1/customers", subject)
    if resp.status_code != 200:
        raise RbacServiceError(f"rbac-service answered {resp.status_code}")
    try:
        body = resp.json()
    except ValueError as e:
        raise RbacServiceError("rbac-service answered with something other than JSON") from e
    if not isinstance(body, dict) or not isinstance(body.get("customers"), list):
        raise RbacServiceError("rbac-service answer is missing customers")
    out = []
    for c in body["customers"]:
        if isinstance(c, dict) and isinstance(c.get("company"), str) and c["company"]:
            name = c.get("display_name")
            out.append({"company": c["company"],
                        "display_name": name if isinstance(name, str) and name.strip() else c["company"]})
    return sorted(out, key=lambda c: c["company"])


async def reassign(subject: str, product_id: str, company: str) -> Written:
    """`PATCH /v1/products/{id}`: make `company` (a customer key, `shared` or `internal`)
    the owner. Needs approve on the CURRENT owner; only EdgeScale may set `shared` or
    `internal`. Writes nothing when `company` already owns it (`owner == previous`),
    so a derived tag stays derived: `declare` is what confirms one."""
    return await _write("PATCH", f"/v1/products/{_pid(product_id)}", subject, {"company": company})


async def declare(subject: str, product_id: str, company: str) -> Written:
    """`POST /v1/products`: tag the product with `company`, as declared. 409 when another
    company owns it; a derived or missing tag for the same owner becomes declared."""
    return await _write("POST", "/v1/products", subject, {"productId": product_id, "company": company})


async def grant_share(subject: str, product_id: str, company: str, role: str) -> Written:
    """`POST /v1/products/{id}/shares`: let `company` use the product at `role` (`read`
    or `developer`). Granting again changes the role. Needs approve on the owner."""
    return await _write("POST", f"/v1/products/{_pid(product_id)}/shares", subject,
                        {"company": company, "role": role})


async def revoke_share(subject: str, product_id: str, company: str) -> Written:
    """`DELETE /v1/products/{id}/shares/{company}`. 404 when it is not shared there."""
    return await _write("DELETE", f"/v1/products/{_pid(product_id)}/shares/{quote(company, safe='')}", subject)


async def catalog(subject: str) -> Catalog:
    """`GET /v1/products` as `subject`: their scope, and the products they may see.

    For an EdgeScale person that is every tagged product, each with its owner, its
    source (`declared` or `derived`) and, where it has any, its shares. A product the
    service has no row for is absent here, and is `internal` by the service's rules.
    """
    resp = await _send("GET", "/v1/products", subject)
    if resp.status_code != 200:
        # 5xx and the rest. None of them is an answer about the person.
        raise RbacServiceError(f"rbac-service answered {resp.status_code}")
    try:
        body = resp.json()
    except ValueError as e:
        raise RbacServiceError("rbac-service answered with something other than JSON") from e
    if not isinstance(body, dict) or not isinstance(body.get("items"), list) \
            or not isinstance(body.get("scope"), list):
        raise RbacServiceError("rbac-service answer is missing scope or items")
    items = [i for i in body["items"] if isinstance(i, dict) and isinstance(i.get("productId"), str)]
    reason = body.get("reason")
    return Catalog(allow=body.get("allow") is True,
                   scope=tuple(s for s in body["scope"] if isinstance(s, str)),
                   items=items,
                   reason=reason[:80] if isinstance(reason, str) else "")
