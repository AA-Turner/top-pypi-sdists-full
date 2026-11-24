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

import asyncio
import re
import time

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
    written, done, stale = await _write_owner(email, pid, owner, expected)
    return await _outcome(client, profile, email, written, done, stale=stale)


class _OutOfTime(Exception):
    """A bulk edit's deadline passed between two of one product's calls; nothing that
    product needed was written."""


async def _write_owner(email: str, pid: str, owner: str, expected: str,
                       in_time=None) -> tuple[rbac_service.Written, str, bool]:
    """The owner write for one product the caller has already been checked against:
    `(written, the success message, whether it was refused as stale)`.

    Up to three calls in a row (read, reassign, declare). `in_time`, from a bulk edit,
    is asked before each call after the first, and raises `_OutOfTime` rather than start
    one past the deadline; a single edit passes nothing."""
    now = await rbac_service.tag(email, pid)
    current = str((now or {}).get("owner") or INTERNAL)
    if current != expected:
        changed = rbac_service.Written(
            False, 409, {}, f"The owner is {current} now, not {expected}: it changed since it was last "
                            "read. Nothing was changed; check the owner and try again.")
        return changed, "", True
    if in_time is not None and not in_time():
        raise _OutOfTime()
    written = await rbac_service.reassign(email, pid, owner)
    if written.ok and written.body.get("owner") == written.body.get("previous"):
        # The reassignment changed nothing (same owner), so stopping here leaves the
        # product as it was.
        if in_time is not None and not in_time():
            raise _OutOfTime()
        written = await rbac_service.declare(email, pid, owner)
        done = f"{owner} confirmed as the owner." if written.body.get("created") else f"{owner} is already the declared owner."
    else:
        done = f"{owner} is now the owner."
    return written, done, False


async def share(client, profile: str, email: str | None, product_id: object, company: object, role: object) -> dict:
    """Share the product with `company` at `role`. Sharing again changes the role."""
    await require_writes(email)
    target = _company(company, owner=False)
    if role not in SHARE_ROLES:
        raise InvalidInput("The role is read or developer.")
    pid = await _listed(client, profile, email, product_id)
    written, done = await _write_share(email, pid, target, role)
    return await _outcome(client, profile, email, written, done)


async def _write_share(email: str, pid: str, target: str, role: str) -> tuple[rbac_service.Written, str]:
    written = await rbac_service.grant_share(email, pid, target, role)
    return written, f"Shared with {target} ({role})."


async def unshare(client, profile: str, email: str | None, product_id: object, company: object) -> dict:
    """Take the product's share away from `company`."""
    await require_writes(email)
    target = _company(company, owner=False)
    pid = await _listed(client, profile, email, product_id)
    written, done = await _write_unshare(email, pid, target)
    return await _outcome(client, profile, email, written, done)


async def _write_unshare(email: str, pid: str, target: str) -> tuple[rbac_service.Written, str]:
    written = await rbac_service.revoke_share(email, pid, target)
    if not written.ok and written.status == 404:
        written = rbac_service.Written(False, 404, written.body, f"It is not shared with {target}.")
    return written, f"No longer shared with {target}."



# --- Bulk edits: one change, several products (spec §4.30 "Bulk edits") ------------
#
# The rbac-service has no bulk form of these writes (its `POST /v1/products` batch only
# declares an owner, and refuses a product another customer owns), so a bulk edit is the
# single edit above, product by product, each made AS the caller and decided by the
# service on its own. It is NOT all-or-nothing: every product gets its own outcome, and
# a run cut short says exactly which products it did not reach.
#
# What a bulk edit does once instead of per product: `require_writes`, the input checks,
# the "is it on the page" check (one catalog read), the cache drop and the re-read.

#: The edits a bulk request may make, by the name the single routes use.
BULK_ACTIONS = ("owner", "share", "unshare")
#: Products in one request. Bounds the request's work and time, not a policy.
BULK_MAX_PRODUCTS = 100
#: Writes in flight at once. The service is one Lambda; this keeps a bulk edit from
#: being a burst against it while still finishing 100 products well inside the budget.
BULK_CONCURRENCY = 4
#: The request must answer inside the load balancer's 60 s idle timeout. From the
#: request's start: no product is STARTED after BULK_BUDGET_SECONDS; no further call for
#: a product already started (an owner change is up to three) after
#: BULK_CALL_DEADLINE_SECONDS; and the catalog is not re-read after
#: BULK_REREAD_DEADLINE_SECONDS (the page reads it itself). The client's
#: `rbac_service_timeout_seconds` (5 s) is httpx's PER-PHASE timeout, not a total, so one
#: call can run longer: hard stops cancel a product's calls at BULK_WRITE_STOP_SECONDS
#: (its outcome is then `unknown`, since the write may have landed) and the re-read at
#: BULK_REREAD_STOP_SECONDS, so the answer always leaves by about 56 s.
BULK_BUDGET_SECONDS = 40.0
BULK_CALL_DEADLINE_SECONDS = 45.0
BULK_WRITE_STOP_SECONDS = 50.0
BULK_REREAD_DEADLINE_SECONDS = 50.0
BULK_REREAD_STOP_SECONDS = 56.0

#: One product's outcome. `done`: changed. `refused`: the service turned it down, in its
#: own words. `stale`: the owner changed since the page read it, so nothing was written.
#: `unknown`: the service did not answer, so the write may or may not have happened.
#: `not_attempted`: the run stopped first (the time budget, or the key was refused).
BULK_STATUSES = ("done", "refused", "stale", "unknown", "not_attempted")
BULK_RESULT_FIELDS = frozenset({"productId", "status", "message"})


def _bulk_products(value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        raise InvalidInput("Pick at least one product.")
    if len(value) > BULK_MAX_PRODUCTS:
        raise InvalidInput(f"At most {BULK_MAX_PRODUCTS} products at a time.")
    pids: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise InvalidInput("Each product is its id.")
        if item.strip() not in pids:
            pids.append(item.strip())
    return pids


def _bulk_expected(value: object, pids: list[str]) -> dict[str, str]:
    """The owner the page showed for each product, which an owner change must still find."""
    if not isinstance(value, dict) or any(not isinstance(value.get(p), str) or not value[p].strip() for p in pids):
        raise InvalidInput("The owner last read is required for every product, so a change made since "
                           "is not overwritten. Read the list again and try again.")
    return {p: value[p].strip().lower() for p in pids}


def _listed_ids(listing: dict) -> set[str]:
    """The product ids the page lists (Apollo's products and the service's tags)."""
    return {p["productId"] for p in listing["products"]}


async def bulk_edit(client, profile: str, email: str | None, action: object, product_ids: object,
                    company: object, *, role: object = None, expected: object = None) -> dict:
    """Make one tag edit (`owner`, `share` or `unshare`) on several products.

    Gated and checked exactly as the single edits are, in the same order, once for the
    whole request; every product must be on the page. Then each product is written as
    the caller, `BULK_CONCURRENCY` at a time, none started after `BULK_BUDGET_SECONDS`.

    Returns `{ok, message, results, summary}` and, when anything may have changed, the
    re-read product list as the single edits do. `ok` is True only when every product is
    `done`. Raises `KeyRefused` only when the service refused this stack's key before
    anything was written, so a surface reports it as it does for a single edit.
    """
    started = time.monotonic()
    await require_writes(email)
    if action not in BULK_ACTIONS:
        raise InvalidInput("The edit is owner, share or unshare.")
    target = _company(company, owner=(action == "owner"))
    if action == "share" and role not in SHARE_ROLES:
        raise InvalidInput("The role is read or developer.")
    pids = _bulk_products(product_ids)
    expect = _bulk_expected(expected, pids) if action == "owner" else {}

    listing = await list_products(client, profile, email)
    listed = _listed_ids(listing)
    missing = [p for p in pids if p not in listed]
    if missing:
        raise InvalidInput(f"{len(missing)} of the products are not in the current product list. "
                           "Read the list again and try again.")

    gate = asyncio.Semaphore(BULK_CONCURRENCY)
    stop = asyncio.Event()  # set when the key is refused: nothing after it can succeed

    async def one(pid: str) -> tuple[dict, bool]:
        """`(result, whether the catalog may have changed)`."""
        async with gate:
            if stop.is_set() or time.monotonic() - started > BULK_BUDGET_SECONDS:
                return {"productId": pid, "status": "not_attempted",
                        "message": "Not attempted: the edit stopped before this product."}, False
            async def write() -> tuple[rbac_service.Written, str, bool]:
                if action == "owner":
                    return await _write_owner(
                        email, pid, target, expect[pid],
                        in_time=lambda: time.monotonic() - started <= BULK_CALL_DEADLINE_SECONDS)
                if action == "share":
                    return (*await _write_share(email, pid, target, role), False)
                return (*await _write_unshare(email, pid, target), False)

            try:
                written, done, stale = await asyncio.wait_for(
                    write(), timeout=max(0.0, BULK_WRITE_STOP_SECONDS - (time.monotonic() - started)))
            except asyncio.TimeoutError:
                # Cancelled mid-call: the service may have acted on it.
                return {"productId": pid, "status": "unknown",
                        "message": "The RBAC service did not answer in time. Reload to see whether this one changed."}, True
            except _OutOfTime:
                return {"productId": pid, "status": "not_attempted",
                        "message": "Not attempted: the edit stopped before this product."}, False
            except rbac_service.KeyRefused:
                stop.set()
                return {"productId": pid, "status": "not_attempted",
                        "message": "Not changed: the RBAC service refused this site's key."}, False
            except rbac_service.RbacServiceError:
                # A timeout can follow a write the service made.
                return {"productId": pid, "status": "unknown",
                        "message": "The RBAC service did not answer. Reload to see whether this one changed."}, True
        if written.ok:
            return {"productId": pid, "status": "done", "message": done}, True
        return {"productId": pid, "status": "stale" if stale else "refused", "message": written.message}, stale

    outcomes = await asyncio.gather(*(one(p) for p in pids))
    results = [r for r, _ in outcomes]
    summary = {status: sum(r["status"] == status for r in results) for status in BULK_STATUSES}
    if stop.is_set() and not any(changed for _, changed in outcomes):
        # Nothing was written: the same answer a single edit gives a refused key.
        raise rbac_service.KeyRefused("rbac-service refused the key; nothing was written")

    done = summary["done"]
    out = {"ok": done == len(pids), "message": f"Changed {done} of {len(pids)}.",
           "results": results, "summary": summary}
    if not any(changed for _, changed in outcomes):
        # Nothing could have changed: the surface keeps the list it has.
        return out
    cache.invalidate("rbac-service")
    if time.monotonic() - started > BULK_REREAD_DEADLINE_SECONDS:
        # No time to re-read inside the load balancer's timeout: the page reads it.
        return out
    try:
        listing = await asyncio.wait_for(
            list_products(client, profile, email),
            timeout=max(0.0, BULK_REREAD_STOP_SECONDS - (time.monotonic() - started)))
        return {**out, **listing}
    except (rbac_service.RbacServiceError, ApolloError, asyncio.TimeoutError):
        # As for a single edit: the writes stand whatever the re-read says.
        return out
