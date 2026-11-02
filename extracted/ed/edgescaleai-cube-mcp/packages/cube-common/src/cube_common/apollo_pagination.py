"""Drain a paginated Apollo read to completion.

**Why this exists.** Three reads asked Apollo for `pageSize: 200` environments,
selected `nextPageToken`, and none of them ever sent it back (issue 252 / OI-6 in
`docs/console-spec.md`). Below the page size that is invisible. Above it every one
of them silently returns a short list, and the symptoms are worse than the cause:

  * `auth/apollo_rbac.py::allowed_cubes` is the **authorization** set for the
    Groundcover tools, so a dropped environment reads to its owner as
    *"Access denied: cube 'x' is not in your authorized set"*;
  * `tools/environments.py::_resolve_environment` backs every MCP tool that takes
    a cube name, so a dropped environment reads to an agent as *"No environment
    found matching 'x'"* — and that message then tells the agent to run
    `list_environments`, which is truncated the same way;
  * the console cube list simply loses rows.

None of those say "pagination". A user reads all three as *the cube was deleted*
or *I lost access*.

It was not hypothetical by the time it was fixed: on 2026-09-21 the fleet was 202
environments, so `tristan-cubelet` and `vcve` were invisible everywhere.

**Verified, not inferred.** The argument is `pageToken`, confirmed by introspection
against the live schema (`scripts/apollo_introspect.py --queries environment`)
rather than copied from the `apollo.products` precedent — AGENTS.md rule 9, and the
reason `--queries` was added to that script. Live behaviour on the same date:
9 pages of 25 drained to 202 unique rows with zero duplicates, and the drained set
equalled a single `pageSize: 1000` read exactly.
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, NamedTuple

from cube_common.apollo_queries import ENVIRONMENTS_PAGE_SIZE

logger = logging.getLogger(__name__)

# Ceiling on how many pages one drain will fetch. At the default page size this is
# 5,000 environments — 25x a fleet that took years to reach 202 — so reaching it
# means something is wrong rather than something is big.
#
# The cap is not about size. It is about never letting a malformed or looping
# upstream turn one request into an unbounded number of Apollo calls:
# `allowed_cubes` runs on every Groundcover tool call, so an unbounded loop there
# is an outage with our name on it. Hitting the cap reports `truncated`, which is
# the same honest signal a stalled token gives.
#
# **It is sized against per-request LATENCY, not against the fleet**, and that is
# what picked 10 over a roomier number. `allowed_cubes` is uncached, and the
# console's `_fetch_environments` sits under `console/cache.py`, whose bounded
# acquire gives up after `_ACQUIRE_TIMEOUT_SECONDS` (20s) and lets the waiter
# fetch CONCURRENTLY. A drain slower than that window turns the convoy guard into
# an amplifier — K concurrent page loads become K independent full drains —
# precisely in the pathological case the cap exists for. At the measured ~0.6s a
# page, 10 pages is ~6s and stays inside the window; 50 would be ~30s and step
# outside it. Raising this means re-checking it against that timeout, not just
# against how many cubes exist.
MAX_PAGES = 10


class PagedResult(NamedTuple):
    """Everything fetched, plus whether the drain actually finished.

    `truncated` means **the loop stopped early** — the page cap was hit, or the
    token stopped advancing. It does NOT mean "the last page was full", which is
    what the pre-pagination code had to use as a proxy and is now simply the
    normal state of every page but the last.

    Returned rather than raised. A partial list with a banner is strictly better
    than an error page: the console can still show the cubes it did get, and
    `allowed_cubes` failing hard would take every Groundcover tool down for
    everyone rather than degrading for whoever is past the cap.
    """

    items: list[dict]
    truncated: bool


def _identity(item: dict) -> str:
    """A stable key for de-duplicating across pages.

    `id` first because it is Apollo's own key; `rid` and `name` are fallbacks so a
    payload missing `id` still de-duplicates rather than silently disabling the
    guard. An item with none of the three is kept as-is (keyed by its position),
    since dropping rows is the failure this module exists to prevent.
    """
    for key in ("id", "rid", "name"):
        value = item.get(key)
        if value:
            return f"{key}:{value}"
    return ""


async def drain_pages(
    fetch_page: Callable[[str | None], Awaitable[dict | None]],
    *,
    items_key: str,
    what: str,
    max_pages: int = MAX_PAGES,
) -> PagedResult:
    """Call `fetch_page(token)` until Apollo stops handing back a next-page token.

    `fetch_page` returns the page object itself — the dict holding `items_key` and
    `nextPageToken` — so this function needs to know nothing about the query or
    where the page sits in the response envelope. It returns **`None` when the
    page did not come back at all**, which is a third outcome and not a synonym
    for an empty one; see guard 4.

    Four guards, each against a distinct way this can go wrong:

    1. **A token that does not advance.** If Apollo ever returns the same token
       twice, the naive loop never terminates. This is not a theoretical worry
       about Apollo so much as a practical one about *fakes*: a test double that
       returns a constant `nextPageToken` is the obvious way to write one, and
       without this guard it hangs CI instead of failing it. Seen tokens are
       tracked, and a repeat stops the drain and reports `truncated`.

    2. **A page cap**, per `MAX_PAGES` above.

    3. **De-duplication across pages.** Apollo's ordering across a paginated read
       is not documented, and the fleet is written to while we read it, so an
       environment created mid-drain can plausibly appear on two pages. The live
       probe saw zero duplicates, so this is insurance rather than a fix for an
       observed bug — but it is cheap insurance for a real rendering bug: the
       console keys cube rows on `rid || name`, and React duplicate keys are a
       genuinely confusing failure. First occurrence wins.

    4. **An absent page envelope OR an absent items list, neither of which may
       read as a finished drain.** `{"environments": [], "nextPageToken": null}`
       means "no more rows"; a null or missing envelope — or an envelope whose
       `items_key` is null or missing — means "we could not read this page", and
       collapsing the second into the first returns a short list reporting itself
       COMPLETE, exactly the silent truncation this module exists to end,
       reintroduced one level down. Both are `truncated=True`.

       **The list is checked as well as the envelope because the two are nullable
       independently**, and a guard on only the outer one is the easier half. For
       environments the inner list is `[ApolloEnvironment!]!` (NON_NULL, verified
       by introspection) so it cannot arrive null — but `items_key` is a parameter,
       and the queries this is written to be reused for have to answer the
       question again for `entities`, `nonGenericPlans` and `productReleases`.
       Checking it here answers it once, for all of them.

       Worth knowing how reachable that is, because it differs by query.
       `Query.apollo`, `ApolloQuery.environments` and
       `ApolloEnvironmentPage.environments` are all NON_NULL (verified by
       introspection), so on the environment reads a field error propagates to a
       null `data` and `ApolloClient.graphql` raises before reaching here. But
       `graphql` returns the payload rather than raising whenever `data` is
       merely truthy ("GraphQL partial errors (returning data)"), and
       `environmentById` IS nullable — so for the reuse this module was written
       for (`CONSOLE_ENVIRONMENT_ENTITIES`, whose page hangs off it) a null branch
       arrives as an ordinary partial success. Guard 4 is what makes that a
       reported failure there rather than "this cube has no entities".

    Note what is deliberately NOT guarded: an empty page carrying a token is
    followed rather than treated as the end. Apollo is entitled to return one, and
    guard 1 already bounds the case where doing so loops.
    """
    items: list[dict] = []
    seen_keys: set[str] = set()
    seen_tokens: set[str] = set()
    token: str | None = None
    pages = 0

    while True:
        page = await fetch_page(token)
        pages += 1

        if page is None:
            logger.error(
                "%s: page %d did not come back (no page envelope in the response) "
                "after %d item(s) — reporting the read as INCOMPLETE rather than "
                "as finished. See issue 252 / OI-6.",
                what, pages, len(items),
            )
            return PagedResult(items, truncated=True)

        raw_items = page.get(items_key)
        if raw_items is None:
            logger.error(
                "%s: page %d came back with no %r list (the envelope was present "
                "but the list was null or missing) after %d item(s) — reporting "
                "the read as INCOMPLETE rather than as finished. "
                "See issue 252 / OI-6.",
                what, pages, items_key, len(items),
            )
            return PagedResult(items, truncated=True)

        for item in raw_items:
            if not isinstance(item, dict):
                continue
            key = _identity(item)
            if key and key in seen_keys:
                logger.warning(
                    "%s: page %d repeated an item already seen (%s) — Apollo's "
                    "page ordering may have shifted mid-drain; keeping the first.",
                    what, pages, key,
                )
                continue
            if key:
                seen_keys.add(key)
            items.append(item)

        token = page.get("nextPageToken") or None
        if not token:
            return PagedResult(items, truncated=False)

        if token in seen_tokens:
            logger.error(
                "%s: Apollo returned the same nextPageToken twice after %d page(s) "
                "and %d item(s) — stopping the drain rather than looping. The list "
                "is INCOMPLETE. See issue 252 / OI-6.",
                what, pages, len(items),
            )
            return PagedResult(items, truncated=True)
        seen_tokens.add(token)

        if pages >= max_pages:
            logger.error(
                "%s: hit the %d-page cap with %d item(s) and a next-page token still "
                "outstanding — the list is INCOMPLETE. Either the fleet has grown "
                "past what this cap was sized for, or the read is looping. "
                "See issue 252 / OI-6.",
                what, max_pages, len(items),
            )
            return PagedResult(items, truncated=True)


async def fetch_all_environments(
    client: Any,
    query: str,
    *,
    page_size: int = ENVIRONMENTS_PAGE_SIZE,
    max_pages: int = MAX_PAGES,
) -> PagedResult:
    """Every environment `query` returns, across every page.

    `query` is `LIST_ENVIRONMENTS` or `CONSOLE_LIST_ENVIRONMENTS` — both take
    `$pageSize`/`$pageToken` and select `nextPageToken`, which is the whole
    contract this needs. Keeping the query a parameter is what lets one drain serve
    the console's richer selection and the two hot-path reads without either of
    them re-implementing the loop, and it is why fixing this in `cube_common` fixed
    all four call sites at once.

    `client` is an `ApolloClient`, typed loosely on purpose: importing it here
    would make the published agent package's query module depend on the HTTP
    client for a type annotation it never uses at runtime.
    """

    async def fetch_page(token: str | None) -> dict | None:
        # `None` for an absent envelope, never `{}`: a missing page and an empty
        # page take different exits in `drain_pages`, and squashing them here is
        # what made a short read look complete. This also restores the loudness
        # the pre-pagination callers had by accident — they did
        # `data["apollo"]["environments"]["environments"]` and raised
        # `AttributeError` on a null branch, which pagination would otherwise have
        # quietly turned into "you have no cubes".
        data = await client.graphql(query, {"pageSize": page_size, "pageToken": token})
        apollo = (data or {}).get("apollo")
        if not isinstance(apollo, dict):
            return None
        page = apollo.get("environments")
        return page if isinstance(page, dict) else None

    return await drain_pages(
        fetch_page,
        items_key="environments",
        what="Apollo environments",
        max_pages=max_pages,
    )
