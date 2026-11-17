"""Product tags: every Apollo product with the owner, source and shares the rbac-service holds."""

from __future__ import annotations

from cube_common.apollo_pagination import fetch_all_products
from cube_cloud.console import cache
from cube_cloud.console.reads import classify_entity
from cube_cloud.manage.access import require_staff

# Serialize through this allowlist, never by passing an Apollo or rbac-service object
# through (the rule `console/reads.py` states for every console payload). Apollo's
# product labels are deliberately not carried: nothing sets them today.
PRODUCT_FIELDS = frozenset({"productId", "kind", "owner", "source", "shares", "in_apollo"})

# What a product the rbac-service has no row for is shown as. The service treats a
# missing row as `internal` (invisible to every customer) and says so in its docs;
# `source: None` is what tells a reader the row is missing rather than declared.
UNTAGGED_OWNER = "internal"


async def _apollo_products(client, profile: str) -> tuple[list[dict], bool]:
    async def produce() -> tuple[list[dict], bool]:
        result = await fetch_all_products(client)
        return result.items, result.truncated

    return await cache.get_or_set(profile, "products", produce)


def _summary(pid: str, apollo: dict | None, tag: dict | None) -> dict:
    shares = [
        {"company": str(s.get("company")), "role": str(s.get("role"))}
        for s in ((tag or {}).get("shares") or [])
        if isinstance(s, dict) and s.get("company")
    ]
    return {
        "productId": pid,
        # The console's hand-maintained platform list (`console_platform_product_*`),
        # not an access decision. A reader uses it to spot products that are probably
        # `shared` or `internal` rather than one customer's.
        "kind": classify_entity(pid),
        "owner": str((tag or {}).get("owner") or UNTAGGED_OWNER),
        # Text whatever the service sent, as owner and shares are: the page renders an
        # unknown source as written, and an object there would fail the whole render.
        # None stays None, because it is what marks the product untagged.
        "source": str(tag["source"]) if tag and tag.get("source") is not None else None,
        "shares": shares,
        "in_apollo": apollo is not None,
    }


async def list_products(client, profile: str, email: str | None, *, fresh: bool = False) -> dict:
    """Every product Apollo has, each with its rbac-service tag, plus tags Apollo lacks.

    `client` is an `ApolloClient` for the caller's own profile, opened by the surface;
    it is read only after `require_staff` passes, because the result names every
    customer's products. A tag whose product Apollo did not return is kept with
    `in_apollo: false` rather than dropped: the product was deleted (a stale row to
    clean up) or the Apollo read was cut short, which `truncated` reports.

    `fresh` re-reads the tags from the service (bounded, see `require_staff`); the
    Apollo half stays cached, since a tag edit never changes it.
    """
    answer = await require_staff(email, fresh=fresh)
    products, truncated = await _apollo_products(client, profile)
    by_tag = {t["productId"]: t for t in answer.items if t.get("productId")}
    by_apollo = {p["productId"]: p for p in products if isinstance(p, dict) and p.get("productId")}
    rows = [_summary(pid, by_apollo.get(pid), by_tag.get(pid))
            for pid in sorted(set(by_apollo) | set(by_tag))]
    return {"products": rows, "count": len(rows), "truncated": truncated}
