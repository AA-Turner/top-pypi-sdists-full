"""One product's details: its releases and where it is installed (docs/console-spec.md §4.30).

Read for ONE product, when a person opens it, never for the whole list: each source is
a few targeted Apollo reads, and nothing here scans environments or the fleet.

The order is the one every `manage` operation follows: `require_staff` first, then the
product id is checked against the Apollo catalog the Products tab already lists (an
enumerated argument, console rule 2), then the reads.

**Each source degrades on its own.** A section is `{state, partial, items}`:

- `ok`: the read answered and found rows. `partial` says it stopped before the end
  (the page cap, a stalled token, a missing page), and the rows are still shown.
- `none`: the read answered and there are none.
- `unavailable`: the read failed. Never shown as `none`.

One section failing never fails the other or the request.

**Installs are found through the product's PACKAGE rid, which is derived, not read.**
`entities` filters by `packageRids`, and passing the product's own rid matches nothing
(verified 2026-11-20). The rid every entity carries is `ri.apollo.main.package.` plus the
product id in URL-safe base64 with the padding dropped (`package_rid`); padding is
rejected as an invalid rid. That form was read off live entities on three products and
is NOT documented anywhere, so two guards keep a change to it visible:

1. every returned entity must name this product (`product.productId`); one that does
   not is dropped and logged, and if every one is dropped the section is `unavailable`;
2. the caveat that remains: if the form changes, Apollo answers an empty list, which
   reads as `none`. Nothing on this side can tell those apart.

**What the caller sees is what their Apollo profile may see, and WE enforce that.**
Apollo's `entities` read is not scoped by team: verified live 2026-11-21, two
customer-scoped profiles got all 98 installs of a product, as admin did. Cube
visibility is team-based and decided here, as everywhere in the console
(`console/reads.py::_visible_environments`). So every install and recent-change row
is kept only when its environment is one the caller's teams have a role on, and a
failed visibility read makes the section `unavailable`, never unfiltered. That also
keeps inventory asked only about cubes the caller can see (AGENTS.md *Inventory join*
item 1), since the company hint is driven by the filtered installs.
"""

from __future__ import annotations

import asyncio
import base64
import logging
from typing import Any

from cube_common.apollo_pagination import drain_pages
from cube_common.apollo_queries import (
    MANAGE_INSTALLS_PAGE_SIZE,
    MANAGE_PRODUCT_INSTALLS,
    MANAGE_PRODUCT_RECENT_PLANS,
    MANAGE_PRODUCT_RELEASES,
    MANAGE_RECENT_CHANGES_LIMIT,
    MANAGE_RELEASES_PAGE_SIZE,
)
from cube_cloud import inventory
from cube_cloud.console import cache
from cube_cloud.console.reads import _display_name, _last_change_for, _visible_environments
from cube_cloud.manage.access import require_staff
from cube_cloud.manage.products import _apollo_products

logger = logging.getLogger(__name__)

# Page caps bound the cost of one click, not the data: 4 x 50 releases, 2 x 500
# installs (~1 s a page measured). Past them a section is `partial`, never silently short.
RELEASES_MAX_PAGES = 4
INSTALLS_MAX_PAGES = 2

# The allowlists every row is built from (console rule 3). Nothing Apollo returns is
# passed through.
RELEASE_FIELDS = frozenset({"version", "created", "created_by", "channels", "recalled"})
INSTALL_FIELDS = frozenset({
    "cube", "display_name", "entity", "version", "health", "rollout", "lifecycle", "module",
})
SECTION_STATES = ("ok", "none", "unavailable")
CHANGE_FIELDS = frozenset({"cube", "entity", "last_changed", "state"})
INSTALL_COMPANY_FIELDS = frozenset({"cube", "company", "resolved"})

# How many cubes get an inventory company hint: the first this many installs in the
# panel's order, which is also how many rows it shows before "Show all"
# (`ProductDetails.tsx::INSTALLS_SHOWN`). One inventory lookup per cube, ~3.3 s cold
# and 8 at a time (`inventory/client.py`), so it is bounded rather than per install.
COMPANY_HINT_LIMIT = 25

_PACKAGE_RID_PREFIX = "ri.apollo.main.package."
_RECALLED = "ApolloProductReleaseRecallStatus_Recalled"

# Held briefly so a person clicking between rows does not re-read Apollo each time.
# A result with a section `unavailable` is not held at all.
DETAILS_CACHE_TTL_SECONDS = 30.0


class UnknownProduct(LookupError):
    """The product is not in the Apollo catalog the Products tab lists."""


class CatalogIncomplete(RuntimeError):
    """The catalog read stopped early and the product was not in the part it read, so
    whether the product exists is not known. A surface renders "could not read", never
    "no such product"."""


def package_rid(product_id: str) -> str:
    """The package rid Apollo's entities carry for `product_id` (see the module docstring)."""
    encoded = base64.urlsafe_b64encode(product_id.encode()).decode().rstrip("=")
    return _PACKAGE_RID_PREFIX + encoded


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


async def _visible_cubes(client, profile: str) -> tuple[set[str], bool] | None:
    """`(names of the environments the caller may see, whether that read fell short)`,
    or None when it failed. Cached per profile by `_visible_environments`."""
    try:
        envs, truncated = await _visible_environments(client, profile)
    except Exception as e:
        logger.warning("manage product details: visibility read failed (%s)", type(e).__name__)
        return None
    return {_text(e.get("name")) for e in envs if _text(e.get("name"))}, truncated


def _env_name(entity: dict) -> str:
    return _text((entity.get("environment") or {}).get("name"))


def _section(items: list[dict], *, partial: bool) -> dict:
    return {"state": "ok" if items else "none", "partial": partial, "items": items}


def _unavailable() -> dict:
    return {"state": "unavailable", "partial": False, "items": []}


def _version(coordinate: Any) -> str:
    text = _text(coordinate)
    return text.rsplit(":", 1)[-1] if ":" in text else text


def _release_row(release: dict) -> dict:
    user = ((release.get("creationAttribution") or {}).get("user") or {})
    channels = sorted({
        _text(c.get("name")) for c in (release.get("releaseChannels") or [])
        if isinstance(c, dict) and _text(c.get("name"))
    })
    recall = (release.get("recallStatus") or {}).get("__typename")
    return {
        "version": _version(release.get("mavenCoordinate")),
        "created": _text(release.get("created")) or None,
        # The Apollo account that created the release: a service account (the MCP
        # one, CI, a per-profile one) or a person's token. None for releases made
        # before Apollo recorded it (about May 2026), shown as "not recorded".
        "created_by": _text(user.get("displayName")) or _text(user.get("username")) or None,
        "channels": channels,
        "recalled": recall == _RECALLED,
    }


def _install_row(entity: dict) -> dict:
    env = entity.get("environment") or {}
    status = entity.get("reportedStatus") or {}
    module = (entity.get("installedByModuleV2") or {}).get("moduleMavenCoordinate")
    locator = entity.get("entityLocator") or {}
    return {
        "cube": _text(env.get("name")),
        "display_name": _display_name(env),
        # The entity's name on that cube. Rows are keyed on (cube, entity), since one
        # cube may hold two installs of a product under different names.
        "entity": _text(locator.get("entityName")),
        "version": _text(status.get("version")) or None,
        "health": _text(status.get("healthStatus")) or None,
        "rollout": _text(status.get("rolloutStatus")) or None,
        "lifecycle": _text(entity.get("lifecycleStatus")) or None,
        # The coordinate of the module that installed it, or None for a direct install.
        # Not secret (`entity_health` prints it); module VARIABLES are never selected.
        "module": _text(module) or None,
    }


async def _releases(client, product_id: str) -> dict:
    async def fetch_page(token):
        data = await client.graphql(MANAGE_PRODUCT_RELEASES, {
            "productId": product_id, "pageSize": MANAGE_RELEASES_PAGE_SIZE, "pageToken": token,
        })
        product = ((data or {}).get("apollo") or {}).get("productByProductIdV2")
        return (product or {}).get("productReleases")

    try:
        result = await drain_pages(fetch_page, items_key="productReleases",
                                   what="manage product releases", max_pages=RELEASES_MAX_PAGES)
    except Exception as e:
        # Class only: an ApolloError's text is the raw response body.
        logger.warning("manage product details: releases read failed (%s)", type(e).__name__)
        return _unavailable()
    rows = [_release_row(r) for r in result.items]
    # A missing first page is a failed read, not "no releases".
    if not rows and result.truncated:
        return _unavailable()
    return _section(rows, partial=result.truncated)


async def _installs(client, profile: str, product_id: str) -> dict:
    rid = package_rid(product_id)
    received = 0

    async def fetch_page(token):
        nonlocal received
        data = await client.graphql(MANAGE_PRODUCT_INSTALLS, {
            "packageRid": rid, "pageSize": MANAGE_INSTALLS_PAGE_SIZE, "pageToken": token,
        })
        page = ((data or {}).get("apollo") or {}).get("entities")
        if isinstance(page, dict) and isinstance(page.get("entities"), list):
            # Dicts only: `drain_pages` skips anything else without counting it as a repeat.
            received += sum(isinstance(e, dict) for e in page["entities"])
        return page

    async def drain():
        try:
            return await drain_pages(fetch_page, items_key="entities",
                                     what="manage product installs", max_pages=INSTALLS_MAX_PAGES)
        except Exception as e:
            logger.warning("manage product details: installs read failed (%s)", type(e).__name__)
            return None

    visibility, result = await asyncio.gather(_visible_cubes(client, profile), drain())
    if visibility is None or result is None:
        return _unavailable()
    visible, visibility_short = visibility

    # `drain_pages` drops a row it has already seen (keyed on the entity `id`). The
    # page token is an offset over a sort that can change mid-read, so a repeat means
    # the pages shifted and some other install may have been skipped: incomplete.
    shifted = received > len(result.items)
    if shifted:
        logger.warning("manage product details: install pages shifted during the read "
                       "(%d repeated); reporting the list as incomplete",
                       received - len(result.items))

    mine = [e for e in result.items if ((e.get("product") or {}).get("productId")) == product_id]
    foreign = len(result.items) - len(mine)
    if foreign:
        # The package-rid form no longer maps to this product alone. Counted, never
        # named: another product's entity is not this read's to describe.
        logger.error(
            "manage product details: %d of %d entities for the derived package rid name "
            "another product; the package rid form may have changed (manage/details.py)",
            foreign, len(result.items),
        )
        if not mine:
            return _unavailable()
    if not mine and result.truncated:
        return _unavailable()
    # Apollo does not scope `entities` by team; this is the filter (module docstring).
    seen = [e for e in mine if _env_name(e) in visible]
    # A short visibility read may have left out a cube the caller can see.
    hidden_maybe_visible = visibility_short and len(seen) < len(mine)
    rows = [_install_row(e) for e in seen]
    rows.sort(key=lambda r: ((r["display_name"] or r["cube"]).casefold(), r["cube"], r["entity"]))
    return _section(rows, partial=result.truncated or bool(foreign) or shifted or hidden_maybe_visible)


async def product_details(client, profile: str, email: str | None, product_id: Any) -> dict:
    """`{productId, releases, installs}` for one product in the Apollo catalog.

    `client` is an `ApolloClient` for the caller's own profile, opened by the surface
    and read only after `require_staff` passes. Raises `NotPermitted` (from
    `require_staff`), `UnknownProduct` and `CatalogIncomplete`; lets `RbacServiceError` and a failed CATALOG
    read through. A failed release or install read is a section state, not an error.
    """
    await require_staff(email)
    pid = _text(product_id)
    if not pid:
        raise UnknownProduct()
    products, truncated = await _apollo_products(client, profile)
    if not any(isinstance(p, dict) and p.get("productId") == pid for p in products):
        # Absent from a catalog read that stopped early is "could not tell", not "no
        # such product": the id is still not read, since it is not known to be one.
        raise CatalogIncomplete() if truncated else UnknownProduct()

    async def produce() -> dict:
        releases, installs = await asyncio.gather(_releases(client, pid), _installs(client, profile, pid))
        return {"productId": pid, "releases": releases, "installs": installs}

    def ttl_for(value: dict) -> float:
        failed = any(value[k]["state"] == "unavailable" for k in ("releases", "installs"))
        return 0.0 if failed else DETAILS_CACHE_TTL_SECONDS

    # Keyed under the caller's profile like every console cache entry; `pid` is a
    # catalog member by now, so the key space is bounded by the catalog.
    return await cache.get_or_set(profile, f"product_details\0{pid}", produce,
                                  ttl=DETAILS_CACHE_TTL_SECONDS, ttl_for=ttl_for)


# --- The second request: last change and company (spec §4.30) ---------------------
#
# Both are slower than the panel itself, so the panel draws first and these fill in.
# Each is bounded, and each is its own section that fails alone.


async def _recent_changes(client, profile: str, product_id: str) -> dict:
    """The last change of the MANAGE_RECENT_CHANGES_LIMIT installs Apollo lists as most
    recently updated. "Most recently updated" is Apollo's LAST_UPDATED sort, whose
    meaning is not documented, so the panel names the rows by that sort and no more.
    Rows on cubes the caller may not see are left out, as for the installs."""
    visibility = await _visible_cubes(client, profile)
    if visibility is None:
        return _unavailable()
    visible, visibility_short = visibility
    try:
        data = await client.graphql(MANAGE_PRODUCT_RECENT_PLANS, {
            "packageRid": package_rid(product_id), "pageSize": MANAGE_RECENT_CHANGES_LIMIT,
        })
    except Exception as e:
        logger.warning("manage product details: recent changes read failed (%s)", type(e).__name__)
        return _unavailable()
    page = ((data or {}).get("apollo") or {}).get("entities")
    entities = page.get("entities") if isinstance(page, dict) else None
    if not isinstance(entities, list):
        return _unavailable()

    rows = []
    foreign = 0
    hidden = 0
    for e in entities:
        if not isinstance(e, dict):
            continue
        if ((e.get("product") or {}).get("productId")) != product_id:
            foreign += 1  # same guard as `_installs`: the derived rid must name this product
            continue
        if _env_name(e) not in visible:
            hidden += 1  # Apollo does not scope `entities` by team (module docstring)
            continue
        plans = ((e.get("nonGenericPlans") or {}).get("plans")) or []
        change = _last_change_for(plans if isinstance(plans, list) else [])
        rows.append({
            "cube": _text((e.get("environment") or {}).get("name")),
            "entity": _text((e.get("entityLocator") or {}).get("entityName")),
            # `age_seconds` is left out on purpose: this result is cached, and a held
            # age would go stale. The time is absolute.
            "last_changed": change["last_changed"],
            "state": change["state"],
        })
    if foreign:
        logger.error("manage product details: %d of %d recently updated entities name another "
                     "product; the package rid form may have changed (manage/details.py)",
                     foreign, len(entities))
        if not rows:
            return _unavailable()
    return _section(rows, partial=bool(foreign) or (visibility_short and hidden > 0))


async def _companies(installs: dict) -> dict:
    """The inventory customer for the cubes of the first COMPANY_HINT_LIMIT installs.

    A hint, not an authority: inventory is filed by hand, and Apollo has no company. The
    cubes asked about are ones the caller's Apollo profile returned (the installs read),
    so inventory is asked only about cubes the caller can see (AGENTS.md *Inventory
    join* item 1). `lookup_each` never takes the fleet sweep, whatever the threshold.
    """
    if not inventory.is_enabled():
        return {"state": "off", "partial": False, "simulated": False, "items": []}
    if installs["state"] == "unavailable":
        return _unavailable() | {"simulated": False}
    cubes: list[str] = []
    for row in installs["items"][:COMPANY_HINT_LIMIT]:
        if row["cube"] and row["cube"] not in cubes:
            cubes.append(row["cube"])
    if not cubes:
        return {"state": "none", "partial": False, "simulated": False, "items": []}
    found = await inventory.lookup_each(set(cubes))
    if not found.available:
        return _unavailable() | {"simulated": False}
    items = []
    for cube in cubes:
        record = found.records.get(cube)
        items.append({
            "cube": cube,
            "company": (record.customer if record is not None else "") or "",
            # False when inventory holds more than one record for the cube and refused
            # to pick: "two records disagree", never "none recorded".
            "resolved": cube not in found.unresolved,
        })
    return {"state": "ok", "partial": False, "simulated": found.simulated, "items": items}


async def install_facts(client, profile: str, email: str | None, product_id: Any) -> dict:
    """`{productId, changes, companies}` for one product: the second request of its
    details panel.

    Authorizes exactly as `product_details` does, by calling it: `require_staff`, then
    the catalog check, then the installs read, which is usually already cached because
    the panel asked for it a moment ago. Raises what it raises.

    `changes` is a section of `{cube, entity, last_changed, state}` (`state` as
    `console/reads.py::_last_change_for` defines it). `companies` is a section of
    `{cube, company, resolved}`, plus `simulated`, and its state may also be `off` when
    the inventory join is disabled on this stack.
    """
    details = await product_details(client, profile, email, product_id)
    pid = details["productId"]

    async def produce() -> dict:
        changes, companies = await asyncio.gather(
            _recent_changes(client, profile, pid), _companies(details["installs"]),
        )
        return {"productId": pid, "changes": changes, "companies": companies}

    def ttl_for(value: dict) -> float:
        failed = any(value[k]["state"] == "unavailable" for k in ("changes", "companies"))
        return 0.0 if failed else DETAILS_CACHE_TTL_SECONDS

    return await cache.get_or_set(profile, f"install_facts\0{pid}", produce,
                                  ttl=DETAILS_CACHE_TTL_SECONDS, ttl_for=ttl_for)


__all__ = [
    "CHANGE_FIELDS", "COMPANY_HINT_LIMIT", "INSTALL_COMPANY_FIELDS", "INSTALL_FIELDS",
    "CatalogIncomplete", "RELEASE_FIELDS", "SECTION_STATES", "UnknownProduct", "install_facts",
    "package_rid", "product_details",
]
