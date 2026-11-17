"""Product tag edits: set a product's owner, share it with a customer, take a share away.

Each operation is one rbac-service write made AS the caller, so the service decides
it on that person: an EdgeScale manager or admin can do all of them, any other
EdgeScale grant (read, developer) sees the page and is refused every edit, in the
service's own words. Nothing here
restates who may do what (rbac_service rule 3).

The order, in every operation:

1. `require_writes`: this stack edits tags, and the caller is EdgeScale staff. Before
   the input is looked at, so a refused caller learns nothing from a validation error.
2. The input's shape: a product the page lists (enumerated, AGENTS.md console rule 2),
   a company key, a share role. Whether the company exists is the service's question.
3. The write. A service refusal is an outcome (`ok: False` with its message), not an
   exception; only "could not ask" raises.
4. On success, every cached catalog in THIS ECS task is dropped, so the list returned
   and the next read this task serves show the change. Another task keeps its cached
   catalog for up to `rbac_service_cache_ttl_seconds`; the page reads with `fresh`
   after an edit for that reason (`access.require_staff`).

A success returns `{ok, message}` plus the refreshed product list, so a surface shows
the result without a second request. The list is left out when re-reading it fails
after the write, rather than reporting a write that happened as an error, and after a
refusal, which changed nothing the surface does not already show.

**An owner change is checked against the owner the person saw.** The service's PATCH
takes only the new owner, so on its own it would replace whatever owner the product has
by then, and a person confirming a tag on a page loaded before someone else's change
would silently undo it. `set_owner` therefore takes `expected`, reads the tag fresh
(uncached) just before writing, and refuses when it differs. That narrows the race to
the gap between that read and the write; closing it needs the service to take the
expected owner itself (an rbac-service change, not made yet).
"""

from __future__ import annotations

import re

from cube_common.apollo_client import ApolloError
from cube_cloud import rbac_service
from cube_cloud.config import settings
from cube_cloud.console import cache
from cube_cloud.manage.access import NotPermitted, is_offered, require_staff
from cube_cloud.manage.products import list_products

# The two owners that are not a customer. Neither can be shared with.
SHARED = "shared"
INTERNAL = "internal"

# The service's company keys: lower-case words joined by single hyphens (its `slug`).
# Anything else would be re-spelled by the service into a key the caller never typed.
_COMPANY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_COMPANY_MAX = 63

#: The roles a share can carry. `read` lets the customer see and install the product;
#: `developer` also lets them publish to it. A share never grants approve.
SHARE_ROLES = ("read", "developer")


class InvalidInput(ValueError):
    """The request's shape is wrong. Its message is safe to show the caller."""


def writes_offered(email: str | None) -> bool:
    """Whether to OFFER tag edits: the Manage section is offered and this stack edits
    tags. A hint for drawing the controls; each write still asks the service."""
    return is_offered(email) and bool(settings.rbac_service_writes_enabled)


async def require_writes(email: str | None) -> None:
    if not writes_offered(email):
        raise NotPermitted()
    await require_staff(email)


def _company(value: object, *, owner: bool) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidInput("A company is required.")
    company = value.strip().lower()
    if len(company) > _COMPANY_MAX or not _COMPANY.match(company):
        raise InvalidInput("A company is its key: lower-case letters, digits and single hyphens.")
    if not owner and company in (SHARED, INTERNAL):
        raise InvalidInput(f"A product cannot be shared with '{company}'.")
    return company


async def _listed(client, profile: str, email: str | None, product_id: object) -> str:
    """The product id, if the page lists it (Apollo's products and the service's tags)."""
    if not isinstance(product_id, str) or not product_id.strip():
        raise InvalidInput("A product is required.")
    pid = product_id.strip()
    listing = await list_products(client, profile, email)
    if not any(p["productId"] == pid for p in listing["products"]):
        raise InvalidInput("That product is not in the current product list. Read the list again and try again.")
    return pid


async def _outcome(client, profile: str, email: str | None, written: rbac_service.Written, done: str,
                   *, stale: bool = False) -> dict:
    """`stale`: the write was not made because the page's view is out of date, so the
    list goes back (re-read) even though nothing changed."""
    outcome = {"ok": written.ok, "message": done if written.ok else written.message}
    if not written.ok and not stale:
        # A refusal changed nothing: the surface keeps the list it has.
        return outcome
    # Every staff member's catalog in this task, not only the caller's: the change is
    # everyone's (and, when stale, every cached copy here is as old as the caller's).
    cache.invalidate("rbac-service")
    try:
        return {**outcome, **await list_products(client, profile, email)}
    except (rbac_service.RbacServiceError, ApolloError):
        # The write is done (or refused) whatever the re-read says, so this must not
        # turn into an error that reads as "nothing changed". No list: the surface
        # reads it again itself.
        return outcome


async def set_owner(client, profile: str, email: str | None, product_id: object, company: object,
                    expected: object) -> dict:
    """Make `company` (a customer key, `shared` or `internal`) the product's owner, as
    a declared tag, provided its owner is still `expected` (the one the page showed).

    A reassignment when the owner changes. When it does not (a derived or missing tag
    for the owner already shown), a declaration instead, so "set the owner to what it
    is" is how a person confirms a derived tag. Shares are kept either way; the service
    keeps them across a reassignment.
    """
    await require_writes(email)
    owner = _company(company, owner=True)
    if not isinstance(expected, str) or not expected.strip():
        raise InvalidInput("The owner last read is required, so a change made since is not overwritten. "
                           "Read the list again and try again.")
    expected = expected.strip().lower()
    pid = await _listed(client, profile, email, product_id)
    now = await rbac_service.tag(email, pid)
    current = str((now or {}).get("owner") or INTERNAL)
    if current != expected:
        changed = rbac_service.Written(
            False, 409, {}, f"The owner is {current} now, not {expected}: it changed since it was last "
                            "read. Nothing was changed; check the owner and try again.")
        return await _outcome(client, profile, email, changed, "", stale=True)
    written = await rbac_service.reassign(email, pid, owner)
    if written.ok and written.body.get("owner") == written.body.get("previous"):
        written = await rbac_service.declare(email, pid, owner)
        done = f"{owner} confirmed as the owner." if written.body.get("created") else f"{owner} is already the declared owner."
    else:
        done = f"{owner} is now the owner."
    return await _outcome(client, profile, email, written, done)


async def share(client, profile: str, email: str | None, product_id: object, company: object, role: object) -> dict:
    """Share the product with `company` at `role`. Sharing again changes the role."""
    await require_writes(email)
    target = _company(company, owner=False)
    if role not in SHARE_ROLES:
        raise InvalidInput("The role is read or developer.")
    pid = await _listed(client, profile, email, product_id)
    written = await rbac_service.grant_share(email, pid, target, role)
    return await _outcome(client, profile, email, written, f"Shared with {target} ({role}).")


async def unshare(client, profile: str, email: str | None, product_id: object, company: object) -> dict:
    """Take the product's share away from `company`."""
    await require_writes(email)
    target = _company(company, owner=False)
    pid = await _listed(client, profile, email, product_id)
    written = await rbac_service.revoke_share(email, pid, target)
    if not written.ok and written.status == 404:
        written = rbac_service.Written(False, 404, written.body, f"It is not shared with {target}.")
    return await _outcome(client, profile, email, written, f"No longer shared with {target}.")
