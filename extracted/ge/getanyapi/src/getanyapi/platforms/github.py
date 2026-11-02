# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the github platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult
from .._pagination import (
    AsyncPaginator,
    Paginator,
    apaginate,
    paginate,
)

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class GithubIssueCommentsInput(TypedDict, total=False):
    """Input for GitHub Issue Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response's nextCursor."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows per page, 1-100 (GitHub's own page-size limit). Each call returns one full page of this size; use nextCursor for the next page. Range: 1 to 100. Default: 100."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[
            Literal["authorAssociation", "authorId", "authorType", "body", "updatedUtc"]
        ]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `authorAssociation` or `body`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a comment that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    since: NotRequired[str]
    """Only comments updated on or after this date (YYYY-MM-DD)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """URL of a GitHub issue or pull request, e.g. https://github.com/openai/whisper/pull/1838."""


class GithubRepositoryInput(TypedDict, total=False):
    """Input for GitHub Repository."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """GitHub repository URL (e.g. https://github.com/facebook/react)."""


class GithubRepositoryContributorsInput(TypedDict, total=False):
    """Input for GitHub Repository Contributors."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows per page, 1-100 (GitHub's own page-size limit). Keep it the same while walking pages, because it sets the page size. Range: 1 to 100. Default: 100."""
    page: NotRequired[int]
    """1-based page of contributors. Request page + 1 while hasMore is true. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """GitHub repository URL, e.g. https://github.com/openai/whisper."""


class GithubRepositoryForksInput(TypedDict, total=False):
    """Input for GitHub Repository Forks."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows per page, 1-100 (GitHub's own page-size limit). Keep it the same while walking pages, because it sets the page size. Range: 1 to 100. Default: 100."""
    page: NotRequired[int]
    """1-based page of forks. Request page + 1 while hasMore is true. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sort: NotRequired[Literal["newest", "oldest", "stargazers", "watchers"]]
    """Order of the forks. Defaults to newest."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """GitHub repository URL, e.g. https://github.com/openai/whisper."""


class GithubRepositoryIssuesInput(TypedDict, total=False):
    """Input for GitHub Repository Issues."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows per page, 1-100 (GitHub's own page-size limit). Keep it the same while walking pages, because it sets the page size. Range: 1 to 100. Default: 100."""
    order: NotRequired[Literal["desc", "asc"]]
    """Sort direction. Defaults to desc."""
    page: NotRequired[int]
    """1-based page of issues. Request page + 1 while hasMore is true. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    since: NotRequired[str]
    """Only issues updated on or after this date (YYYY-MM-DD)."""
    sort: NotRequired[Literal["created", "updated", "comments"]]
    """Sort by creation date, last update, or number of comments. Defaults to created."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    state: NotRequired[Literal["open", "closed", "all"]]
    """Which issues to list. Defaults to open."""
    url: Required[str]
    """GitHub repository URL, e.g. https://github.com/openai/whisper."""


class GithubRepositoryReadmeInput(TypedDict, total=False):
    """Input for GitHub Repository README."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    requireFields: NotRequired[
        list[Literal["content", "downloadUrl", "name", "path", "sha", "size", "url"]]
    ]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Name the output fields this request must be able to return, for example `content` or `size`, and it is served only by a source that returns every one of them. Fields you do not name are still returned whenever the serving source has them. This can raise your price: when the cheapest source cannot return a named field, a dearer source serves, and you are quoted and charged its price. A named field can still be absent on a README that genuinely lacks it. Naming a combination that no single source returns together is refused as invalid input, with no charge."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    url: Required[str]
    """GitHub repository URL, e.g. https://github.com/openai/whisper. The README of the default branch is returned."""


class GithubSearchIssuesInput(TypedDict, total=False):
    """Input for GitHub Issue and PR Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Rows per page, 1-100 (GitHub's own page-size limit). Keep it the same while walking pages, because it sets the page size. Range: 1 to 100. Default: 100."""
    order: NotRequired[Literal["desc", "asc"]]
    """Sort direction when sort is set. Defaults to desc."""
    page: NotRequired[int]
    """1-based page of results. Request page + 1 while hasMore is true. Minimum: 1. Default: 1."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """GitHub issue search query with any of GitHub's qualifiers, e.g. "repo:openai/whisper is:pr", "is:issue label:bug author:octocat", "repo:ggml-org/llama.cpp is:pr is:merged created:>2026-01-01"."""
    sort: NotRequired[Literal["comments", "created", "updated", "reactions"]]
    """Sort by number of comments, creation date, last update, or reactions. Omit for best match."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubTrendingDevelopersInput(TypedDict, total=False):
    """Input for GitHub Trending Developers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Programming language to filter trending developers (e.g. javascript, python, go)."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    since: NotRequired[Literal["daily", "weekly", "monthly"]]
    """Trending range: daily, weekly, or monthly (defaults to daily)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubTrendingRepositoriesInput(TypedDict, total=False):
    """Input for GitHub Trending Repositories."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    language: NotRequired[str]
    """Filter by programming language (e.g. "go", "typescript"). Omit for all languages."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    since: NotRequired[Literal["daily", "weekly", "monthly"]]
    """Trending window. Default: daily."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubUserInput(TypedDict, total=False):
    """Input for GitHub User."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubUserActivityInput(TypedDict, total=False):
    """Input for GitHub User Activity."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response (pages backward by month)."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    year: NotRequired[str]
    """Year of contribution activity to return (defaults to the current year)."""


class GithubUserContributionsInput(TypedDict, total=False):
    """Input for GitHub User Contributions."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    year: NotRequired[int]
    """Calendar year of the contribution graph. Defaults to the current year."""


class GithubUserFollowersInput(TypedDict, total=False):
    """Input for GitHub User Followers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response (page number, defaults to 1)."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubUserFollowingInput(TypedDict, total=False):
    """Input for GitHub User Following."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response (page number, defaults to 1)."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class GithubUserPullRequestsInput(TypedDict, total=False):
    """Input for GitHub User Pull Requests."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from a previous response (page number, defaults to 1)."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    since: NotRequired[str]
    """Only include pull requests created on or after this date (YYYY-MM-DD)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    until: NotRequired[str]
    """Only include pull requests created on or before this date (YYYY-MM-DD)."""


class GithubUserRepositoriesInput(TypedDict, total=False):
    """Input for GitHub User Repositories."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Opaque pagination cursor from a previous response's nextCursor. Omit for the first page; pass it back to fetch the next page."""
    direction: NotRequired[Literal["asc", "desc"]]
    """Sort direction, ascending or descending, paired with sort."""
    handle: Required[str]
    """GitHub username."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    sort: NotRequired[Literal["created", "updated", "pushed", "full_name"]]
    """Repository ordering. Default: updated."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    type: NotRequired[Literal["owner", "all", "member"]]
    """Which repositories to include: owner (default), all, or member."""


class GithubIssueCommentsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comments: list[GithubIssueCommentsComment] = Field(
        description="Comments in the order they were posted. Review comments on pull request code lines are not included. Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when there are no more. Pass it back as cursor to continue.",
    )


class GithubIssueCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        description="GitHub login of the commenter. Populated whenever the provider has data for the entity."
    )
    author_association: str | None = Field(
        alias="authorAssociation",
        description="The commenter's relationship to the repository, as GitHub reports it: OWNER, MEMBER, COLLABORATOR, CONTRIBUTOR, FIRST_TIME_CONTRIBUTOR, FIRST_TIMER or NONE.",
    )
    author_avatar_url: str | None = Field(
        alias="authorAvatarUrl", description="Avatar image URL of the commenter."
    )
    author_id: str | None = Field(
        alias="authorId",
        description="GitHub's numeric user id of the commenter, as a string.",
    )
    author_type: str | None = Field(
        alias="authorType",
        description="Account type of the commenter: User, Bot or Organization.",
    )
    body: str | None = Field(
        description="Comment text in Markdown. One source returns it with HTML tags removed; name body in requireFields for the exact Markdown."
    )
    created_utc: float | None = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    id: str = Field(description="GitHub's numeric comment id, as a string.")
    reactions: int | None = Field(
        description="Total number of reactions of every kind."
    )
    updated_utc: float | None = Field(
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical GitHub URL of the comment. Populated whenever the provider has data for the entity."
    )


class GithubRepositoryData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    archived: bool | None = Field(
        default=None, description="Whether the repository is archived."
    )
    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="Avatar image URL of the repository owner.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    default_branch: str | None = Field(
        default=None,
        alias="defaultBranch",
        description="Name of the default branch. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None, description="Short repository description, or null if none."
    )
    fork: bool | None = Field(
        default=None, description="Whether the repository is a fork."
    )
    forks: int | None = Field(default=None, description="Number of forks.")
    full_name: str = Field(
        alias="fullName",
        description="Full repository name in owner/name form. Populated whenever the provider has data for the entity.",
    )
    homepage: str | None = Field(
        default=None, description="Project homepage URL, or null if none."
    )
    id: str | None = Field(
        default=None, description="GitHub's numeric repository id, as a string."
    )
    language: str | None = Field(
        default=None, description="Primary programming language, or null if undetected."
    )
    license: str | None = Field(
        default=None, description="License name, or null if unlicensed."
    )
    name: str = Field(
        description="Repository short name (without owner). Populated whenever the provider has data for the entity."
    )
    open_issues: int | None = Field(
        default=None,
        alias="openIssues",
        description="Count of open issues and pull requests.",
    )
    owner: str | None = Field(
        default=None,
        description="Login of the repository owner (user or organization). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    private: bool | None = Field(
        default=None, description="Whether the repository is private."
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="GitHub profile URL of the repository owner.",
    )
    pushed_at: str | None = Field(
        default=None,
        alias="pushedAt",
        description="Last push timestamp (ISO 8601). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    size: int | None = Field(
        default=None, description="Repository size in kilobytes as reported by GitHub."
    )
    stars: int | None = Field(default=None, description="Number of stargazers.")
    topics: list[str] | None = Field(default=None, description="Repository topic tags.")
    updated_at: str | None = Field(
        default=None,
        alias="updatedAt",
        description="Last metadata update timestamp (ISO 8601). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str = Field(
        description="Canonical URL of the repository. Populated whenever the provider has data for the entity."
    )
    watchers: int | None = Field(default=None, description="Number of watchers.")


class GithubRepositoryContributorsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    contributors: list[GithubRepositoryContributorsContributor] = Field(
        description="Contributors with a GitHub account, most commits first. Populated whenever the provider has data for the entity."
    )
    has_more: bool | None = Field(
        alias="hasMore",
        description="True when another page of contributors exists; request page + 1 to continue.",
    )


class GithubRepositoryContributorsContributor(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str | None = Field(alias="avatarUrl", description="Avatar image URL.")
    contributions: int | None = Field(
        description="Number of commits to the repository's default branch. Populated whenever the provider has data for the entity."
    )
    id: str | None = Field(description="GitHub's numeric user id, as a string.")
    login: str = Field(
        description="GitHub login of the contributor. Populated whenever the provider has data for the entity."
    )
    site_admin: bool | None = Field(
        alias="siteAdmin",
        description="Whether the account is a GitHub staff administrator.",
    )
    type_: str | None = Field(
        alias="type", description="Account type: User, Bot or Organization."
    )
    url: str | None = Field(
        description="GitHub profile URL. Populated whenever the provider has data for the entity."
    )


class GithubRepositoryForksData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    forks: list[GithubRepositoryForksFork] = Field(
        description="Forks of the repository. Populated whenever the provider has data for the entity."
    )
    has_more: bool | None = Field(
        alias="hasMore",
        description="True when another page of forks exists; request page + 1 to continue.",
    )


class GithubRepositoryForksFork(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    archived: bool | None = Field(description="Whether the fork is archived.")
    created_utc: float | None = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. When the fork was created.",
    )
    default_branch: str | None = Field(
        alias="defaultBranch", description="Name of the default branch."
    )
    description: str | None = Field(description="Repository description.")
    forks: int | None = Field(description="Number of forks of this fork.")
    full_name: str = Field(
        alias="fullName",
        description="Fork's full name in owner/name form. Populated whenever the provider has data for the entity.",
    )
    homepage: str | None = Field(description="Project homepage URL, or null if none.")
    id: str = Field(
        description="GitHub's numeric repository id of the fork, as a string."
    )
    language: str | None = Field(description="Primary language GitHub detected.")
    name: str = Field(
        description="Fork's repository name (without owner). Populated whenever the provider has data for the entity."
    )
    open_issues: int | None = Field(
        alias="openIssues", description="Count of open issues and pull requests."
    )
    owner: str | None = Field(
        description="Login of the fork's owner. Populated whenever the provider has data for the entity."
    )
    owner_avatar_url: str | None = Field(
        alias="ownerAvatarUrl", description="Avatar image URL of the owner."
    )
    owner_type: str | None = Field(
        alias="ownerType",
        description="Account type of the owner: User or Organization.",
    )
    owner_url: str | None = Field(
        alias="ownerUrl", description="GitHub profile URL of the owner."
    )
    pushed_utc: float | None = Field(
        alias="pushedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Last push to any branch; a fork never pushed to keeps its parent's last push.",
    )
    size: int | None = Field(
        description="Repository size in kilobytes as reported by GitHub."
    )
    stars: int | None = Field(description="Number of stars.")
    topics: list[str] = Field(description="Topics set on the fork.")
    updated_utc: float | None = Field(
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical GitHub URL of the fork. Populated whenever the provider has data for the entity."
    )
    watchers: int | None = Field(
        description="Number of watchers as GitHub counts them (equal to stars)."
    )


class GithubRepositoryIssuesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        alias="hasMore",
        description="True when another page of issues exists; request page + 1 to continue.",
    )
    issues: list[GithubRepositoryIssuesIssue] = Field(
        description="Issues and pull requests, newest first unless sorted otherwise. Populated whenever the provider has data for the entity."
    )


class GithubRepositoryIssuesIssue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        description="GitHub login of the person who opened it. Populated whenever the provider has data for the entity."
    )
    author_association: str | None = Field(
        alias="authorAssociation",
        description="The author's relationship to the repository, as GitHub reports it: OWNER, MEMBER, COLLABORATOR, CONTRIBUTOR, FIRST_TIME_CONTRIBUTOR, FIRST_TIMER or NONE.",
    )
    author_avatar_url: str | None = Field(
        alias="authorAvatarUrl", description="Avatar image URL of the author."
    )
    author_id: str | None = Field(
        alias="authorId",
        description="GitHub's numeric user id of the author, as a string.",
    )
    author_type: str | None = Field(
        alias="authorType",
        description="Account type of the author: User, Bot or Organization.",
    )
    body: str | None = Field(
        description="Markdown body as written, or null when empty."
    )
    closed_utc: float | None = Field(
        alias="closedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Null while open.",
    )
    comments: int | None = Field(description="Number of comments.")
    created_utc: float | None = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    draft: bool | None = Field(
        description="Whether a pull request is a draft; null for an issue."
    )
    id: str = Field(description="GitHub's numeric issue id, as a string.")
    is_pull_request: bool = Field(
        alias="isPullRequest",
        description="True for a pull request, false for an issue.",
    )
    labels: list[str] = Field(description="Names of the labels applied.")
    merged_utc: float | None = Field(
        alias="mergedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Set only on a merged pull request.",
    )
    number: int | None = Field(
        description="Issue or pull request number within its repository (the #N shown on GitHub)."
    )
    reactions: int | None = Field(
        description="Total number of reactions of every kind."
    )
    repo: str | None = Field(
        description="Repository the issue belongs to, in owner/name form."
    )
    state: str | None = Field(
        description="open or closed. A merged pull request is closed and has mergedUtc set."
    )
    title: str = Field(
        description="Title of the issue or pull request. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical GitHub URL of the issue or pull request. Populated whenever the provider has data for the entity."
    )


class GithubRepositoryReadmeData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    content: str = Field(
        description="The README text exactly as committed, usually Markdown that may include HTML. One source returns it with HTML tags removed; name content in requireFields for the exact file."
    )
    download_url: str | None = Field(
        alias="downloadUrl", description="Raw download URL of the README file."
    )
    name: str | None = Field(description="File name of the README, e.g. README.md.")
    path: str | None = Field(description="Path of the README inside the repository.")
    sha: str | None = Field(description="Git blob SHA of the README file.")
    size: int | None = Field(description="Size of the README file in bytes.")
    url: str | None = Field(description="GitHub URL of the README file.")


class GithubSearchIssuesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool | None = Field(
        alias="hasMore",
        description="True when another page of results exists; request page + 1 to continue.",
    )
    issues: list[GithubSearchIssuesIssue] = Field(
        description="Matching issues and pull requests. Populated whenever the provider has data for the entity."
    )
    total: int | None = Field(
        description="Total number of matches GitHub reports. GitHub serves only the first 1,000 of them, so page times limit can be at most 1,000."
    )


class GithubSearchIssuesIssue(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author: str | None = Field(
        description="GitHub login of the person who opened it. Populated whenever the provider has data for the entity."
    )
    author_association: str | None = Field(
        alias="authorAssociation",
        description="The author's relationship to the repository, as GitHub reports it: OWNER, MEMBER, COLLABORATOR, CONTRIBUTOR, FIRST_TIME_CONTRIBUTOR, FIRST_TIMER or NONE.",
    )
    author_avatar_url: str | None = Field(
        alias="authorAvatarUrl", description="Avatar image URL of the author."
    )
    author_id: str | None = Field(
        alias="authorId",
        description="GitHub's numeric user id of the author, as a string.",
    )
    author_type: str | None = Field(
        alias="authorType",
        description="Account type of the author: User, Bot or Organization.",
    )
    body: str | None = Field(
        description="Markdown body as written, or null when empty."
    )
    closed_utc: float | None = Field(
        alias="closedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Null while open.",
    )
    comments: int | None = Field(description="Number of comments.")
    created_utc: float | None = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    draft: bool | None = Field(
        description="Whether a pull request is a draft; null for an issue."
    )
    id: str = Field(description="GitHub's numeric issue id, as a string.")
    is_pull_request: bool = Field(
        alias="isPullRequest",
        description="True for a pull request, false for an issue.",
    )
    labels: list[str] = Field(description="Names of the labels applied.")
    merged_utc: float | None = Field(
        alias="mergedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Set only on a merged pull request.",
    )
    number: int | None = Field(
        description="Issue or pull request number within its repository (the #N shown on GitHub)."
    )
    reactions: int | None = Field(
        description="Total number of reactions of every kind."
    )
    repo: str | None = Field(
        description="Repository the issue belongs to, in owner/name form."
    )
    state: str | None = Field(
        description="open or closed. A merged pull request is closed and has mergedUtc set."
    )
    title: str = Field(
        description="Title of the issue or pull request. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical GitHub URL of the issue or pull request. Populated whenever the provider has data for the entity."
    )


class GithubTrendingDevelopersData(BaseModel):
    developers: list[GithubTrendingDevelopersDeveloper] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    language: str
    since: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubTrendingDevelopersDeveloper(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    name: str
    popular_repo: str = Field(alias="popularRepo")
    popular_repo_description: str = Field(alias="popularRepoDescription")
    popular_repo_url: str = Field(alias="popularRepoUrl")
    rank: int
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubTrendingRepositoriesData(BaseModel):
    repos: list[GithubTrendingRepositoriesRepo] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    since: str | None = Field(
        default=None,
        description="Trending window the listing was read for (daily, weekly, or monthly).",
    )


class GithubTrendingRepositoriesRepo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str
    forks: int
    full_name: str = Field(
        alias="fullName",
        description="Populated whenever the provider has data for the entity.",
    )
    language: str
    name: str | None = Field(
        default=None, description="Repository short name (without owner)."
    )
    owner: str | None = Field(
        default=None,
        description="Login of the repository owner (user or organization).",
    )
    rank: int
    stars: int
    stars_today: int = Field(alias="starsToday")
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubUserData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="URL of the profile avatar image. Populated whenever the provider has data for the entity.",
    )
    bio: str = Field(description="Profile bio text.")
    blog: str | None = Field(
        default=None, description="Blog or website URL from the profile."
    )
    company: str | None = Field(
        default=None, description="Company listed on the profile."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    followers: int = Field(description="Number of followers.")
    following: int = Field(description="Number of accounts the user follows.")
    id: str | None = Field(
        default=None, description="GitHub's numeric user id, as a string."
    )
    location: str | None = Field(
        default=None, description="Location listed on the profile."
    )
    login: str = Field(
        description="GitHub username (handle). Populated whenever the provider has data for the entity."
    )
    name: str = Field(
        description="Display name, or empty string if unset. Populated whenever the provider has data for the entity."
    )
    profile_url: str | None = Field(
        default=None, alias="profileUrl", description="Canonical GitHub profile URL."
    )
    public_gists: int | None = Field(
        default=None, alias="publicGists", description="Count of public gists."
    )
    public_repos: int = Field(
        alias="publicRepos", description="Count of public repositories."
    )
    twitter_username: str | None = Field(
        default=None, alias="twitterUsername", description="Linked X/Twitter username."
    )
    type_: str | None = Field(
        default=None, alias="type", description='"User" or "Organization".'
    )


class GithubUserActivityData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    activity: list[GithubUserActivityActivity] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    month: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of activity, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    no_activity: bool = Field(alias="noActivity")
    username: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    year: int


class GithubUserActivityActivity(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[GithubUserActivityItem] | None = Field(
        default=None,
        description="The individual entries behind this activity summary. Empty when the upstream published no breakdown.",
    )
    summary: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubUserActivityItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    repo: str | None = Field(
        default=None,
        description="Full repository name in owner/name form for this entry.",
    )
    text: str | None = Field(
        default=None,
        description='The entry as GitHub renders it, e.g. "owner/repo 353 commits".',
    )
    url: str | None = Field(
        default=None, description="Canonical URL of the repository for this entry."
    )


class GithubUserContributionsData(BaseModel):
    days: list[GithubUserContributionsDay] = Field(
        description="Per-day contribution buckets for the year. Populated whenever the provider has data for the entity."
    )
    total: int = Field(description="Total contributions across the year.")
    username: str = Field(
        description="GitHub username the contribution graph belongs to. Populated whenever the provider has data for the entity."
    )
    year: int = Field(description="Calendar year of the contribution graph.")


class GithubUserContributionsDay(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    count: int = Field(description="Number of contributions on this day.")
    date_utc: float = Field(
        alias="dateUtc",
        description="UTC epoch seconds at 00:00 UTC of the contribution day. Populated whenever the provider has data for the entity.",
    )
    intensity: int = Field(description="Heatmap level 0-4.")


class GithubUserFollowersData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    followers: list[GithubUserFollowersFollower] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of followers, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class GithubUserFollowersFollower(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    id: int
    login: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    site_admin: bool = Field(alias="siteAdmin")
    type_: str = Field(
        alias="type",
        description="Populated whenever the provider has data for the entity.",
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubUserFollowingData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    following: list[GithubUserFollowingFollowing] = Field(
        description="Populated whenever the provider has data for the entity."
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of followed accounts, or null when this lane has no more. Pass it back as cursor to continue.",
    )


class GithubUserFollowingFollowing(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    avatar_url: str = Field(
        alias="avatarUrl",
        description="Populated whenever the provider has data for the entity.",
    )
    id: int
    login: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    site_admin: bool = Field(alias="siteAdmin")
    type_: str = Field(
        alias="type",
        description="Populated whenever the provider has data for the entity.",
    )
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubUserPullRequestsData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(
        alias="hasMore",
        description="Whether more pull requests are available beyond this page.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of pull requests, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    pull_requests: list[GithubUserPullRequestsPullRequest] = Field(
        alias="pullRequests",
        description="The user's public pull requests for this page. Populated whenever the provider has data for the entity.",
    )


class GithubUserPullRequestsPullRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created_utc: float = Field(
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity.",
    )
    repo: str = Field(
        description="Repository the pull request targets, in owner/name form. Populated whenever the provider has data for the entity."
    )
    state: str = Field(
        description="Pull request state (e.g. open, closed, merged). Populated whenever the provider has data for the entity."
    )
    title: str = Field(
        description="Pull request title. Populated whenever the provider has data for the entity."
    )
    url: str = Field(
        description="Canonical URL of the pull request. Populated whenever the provider has data for the entity."
    )


class GithubUserRepositoriesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    has_more: bool = Field(alias="hasMore")
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of repositories, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    repos: list[GithubUserRepositoriesRepo] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class GithubUserRepositoriesRepo(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    archived: bool
    avatar_url: str | None = Field(
        default=None,
        alias="avatarUrl",
        description="URL of the repository owner's avatar image.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    default_branch: str | None = Field(
        default=None, alias="defaultBranch", description="Name of the default branch."
    )
    description: str
    fork: bool
    forks: int
    full_name: str = Field(
        alias="fullName",
        description="Populated whenever the provider has data for the entity.",
    )
    homepage: str | None = Field(
        default=None, description="Project homepage URL, or empty string if none."
    )
    id: str | None = Field(
        default=None, description="GitHub's numeric repository id, as a string."
    )
    language: str
    license: str | None = Field(
        default=None, description="License name, or empty string if unlicensed."
    )
    name: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    open_issues: int | None = Field(
        default=None,
        alias="openIssues",
        description="Count of open issues and pull requests.",
    )
    owner: str | None = Field(
        default=None,
        description="Login of the repository owner (user or organization).",
    )
    private: bool | None = Field(
        default=None, description="Whether the repository is private."
    )
    profile_url: str | None = Field(
        default=None,
        alias="profileUrl",
        description="GitHub profile URL of the repository owner.",
    )
    pushed_at: str = Field(alias="pushedAt")
    size: int | None = Field(
        default=None, description="Repository size in kilobytes as reported by GitHub."
    )
    stars: int
    topics: list[str] | None = Field(default=None, description="Repository topic tags.")
    updated_at: str = Field(alias="updatedAt")
    url: str = Field(
        description="Populated whenever the provider has data for the entity."
    )
    watchers: int | None = Field(default=None, description="Number of watchers.")


class GithubNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def issue_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubIssueCommentsInput],
    ) -> RunResult[GithubIssueCommentsData]:
        """GitHub Issue Comments

        List the comments on a GitHub issue or pull request by its URL, oldest
        first, with each commenter's login, their relationship to the repository,
        reactions and the comment text.

        Price: $0.0012 per request.

        Example:
            res = client.github.issue_comments(limit=10, url="https://github.com/openai/whisper/pull/1838")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.issue_comments", dict(input), options
        )
        return RunResult[GithubIssueCommentsData].model_validate(raw)

    def iter_issue_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubIssueCommentsInput],
    ) -> Paginator[GithubIssueCommentsComment, GithubIssueCommentsData]:
        """Iterate GitHub Issue Comments results, following pagination cursors.

        Yields validated `GithubIssueCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.issue_comments",
            dict(input),
            "comments",
            item_model=GithubIssueCommentsComment,
            data_model=GithubIssueCommentsData,
            bare=False,
            options=options,
        )

    def repository(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryInput],
    ) -> RunResult[GithubRepositoryData]:
        """GitHub Repository

        Fetch a GitHub repository's metadata by URL (stars, forks, language, topics,
        license, and timestamps).

        Price: $0.0012 per request.

        Example:
            res = client.github.repository(url="https://github.com/facebook/react")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository", dict(input), options
        )
        return RunResult[GithubRepositoryData].model_validate(raw)

    def repository_contributors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryContributorsInput],
    ) -> RunResult[GithubRepositoryContributorsData]:
        """GitHub Repository Contributors

        List the people who have committed to a GitHub repository by repository URL,
        ordered by number of commits, with each contributor's login, profile URL and
        commit count. Look each one up with github.user for their profile, website
        and socials.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_contributors(limit=10, url="https://github.com/openai/whisper")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_contributors", dict(input), options
        )
        return RunResult[GithubRepositoryContributorsData].model_validate(raw)

    def repository_forks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryForksInput],
    ) -> RunResult[GithubRepositoryForksData]:
        """GitHub Repository Forks

        List the forks of a GitHub repository by repository URL, with each fork's
        owner, description, stars, language and last push. Sort by newest, oldest or
        most starred.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_forks(url="https://github.com/openai/whisper")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_forks", dict(input), options
        )
        return RunResult[GithubRepositoryForksData].model_validate(raw)

    def repository_issues(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryIssuesInput],
    ) -> RunResult[GithubRepositoryIssuesData]:
        """GitHub Repository Issues

        List a GitHub repository's issues and pull requests by repository URL
        (GitHub lists pull requests as issues), with each one's author, state,
        labels, counts and body. Filter by state, sort and update date.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_issues(url="https://github.com/openai/whisper")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_issues", dict(input), options
        )
        return RunResult[GithubRepositoryIssuesData].model_validate(raw)

    def repository_readme(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryReadmeInput],
    ) -> RunResult[GithubRepositoryReadmeData]:
        """GitHub Repository README

        Get a GitHub repository's README by repository URL, as the Markdown text the
        maintainers wrote, with its file name, path and size. Use it to learn what a
        project does, which models and tools it uses, and how to reach its authors.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_readme(url="https://github.com/openai/whisper")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_readme", dict(input), options
        )
        return RunResult[GithubRepositoryReadmeData].model_validate(raw)

    def search_issues(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubSearchIssuesInput],
    ) -> RunResult[GithubSearchIssuesData]:
        """GitHub Issue and PR Search

        Search issues and pull requests across GitHub with GitHub's own search
        syntax (repo:, is:pr, is:issue, author:, label:, created:...), with each
        result's author, state, labels, counts and body. Use it to find who opens
        issues and pull requests on a repository.

        Price: $0.0024 per request.

        Example:
            res = client.github.search_issues(query="repo:openai/whisper is:pr")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.search_issues", dict(input), options
        )
        return RunResult[GithubSearchIssuesData].model_validate(raw)

    def trending_developers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubTrendingDevelopersInput],
    ) -> RunResult[GithubTrendingDevelopersData]:
        """GitHub Trending Developers

        List trending GitHub developers (rank, username, name, avatar, and their
        most popular repository), optionally filtered by programming language and
        time range.

        Price: $0.0012 per request.

        Example:
            res = client.github.trending_developers(language="go", since="weekly")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.trending_developers", dict(input), options
        )
        return RunResult[GithubTrendingDevelopersData].model_validate(raw)

    def trending_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubTrendingRepositoriesInput],
    ) -> RunResult[GithubTrendingRepositoriesData]:
        """GitHub Trending Repositories

        List GitHub Trending repositories (rank, stars, stars gained today,
        language, and description), filterable by language and time window.

        Price: $0.0012 per request.

        Example:
            res = client.github.trending_repositories(language="python", since="daily")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.trending_repositories", dict(input), options
        )
        return RunResult[GithubTrendingRepositoriesData].model_validate(raw)

    def user(
        self, *, options: RequestOptions | None = None, **input: Unpack[GithubUserInput]
    ) -> RunResult[GithubUserData]:
        """GitHub User

        Fetch a GitHub user's public profile by handle (name, bio, company,
        location, followers, and repo counts).

        Price: $0.0012 per request.

        Example:
            res = client.github.user(handle="torvalds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user", dict(input), options
        )
        return RunResult[GithubUserData].model_validate(raw)

    def user_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserActivityInput],
    ) -> RunResult[GithubUserActivityData]:
        """GitHub User Activity

        List a GitHub user's public contribution activity by handle (grouped monthly
        summaries of commits, pull requests, and issues with repository links) for a
        given year.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_activity(handle="kentcdodds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_activity", dict(input), options
        )
        return RunResult[GithubUserActivityData].model_validate(raw)

    def iter_user_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserActivityInput],
    ) -> Paginator[GithubUserActivityActivity, GithubUserActivityData]:
        """Iterate GitHub User Activity results, following pagination cursors.

        Yields validated `GithubUserActivityActivity` items from the `activity` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.user_activity",
            dict(input),
            "activity",
            item_model=GithubUserActivityActivity,
            data_model=GithubUserActivityData,
            bare=False,
            options=options,
        )

    def user_contributions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserContributionsInput],
    ) -> RunResult[GithubUserContributionsData]:
        """GitHub User Contributions

        Fetch a GitHub user's contribution graph for a year (total contributions
        plus per-day counts and heatmap intensity).

        Price: $0.0012 per request.

        Example:
            res = client.github.user_contributions(handle="torvalds", year=2024)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_contributions", dict(input), options
        )
        return RunResult[GithubUserContributionsData].model_validate(raw)

    def user_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowersInput],
    ) -> RunResult[GithubUserFollowersData]:
        """GitHub User Followers

        List a GitHub user's followers by handle (each follower's login, type,
        avatar, and profile URL) with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_followers(handle="torvalds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_followers", dict(input), options
        )
        return RunResult[GithubUserFollowersData].model_validate(raw)

    def iter_user_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowersInput],
    ) -> Paginator[GithubUserFollowersFollower, GithubUserFollowersData]:
        """Iterate GitHub User Followers results, following pagination cursors.

        Yields validated `GithubUserFollowersFollower` items from the `followers` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.user_followers",
            dict(input),
            "followers",
            item_model=GithubUserFollowersFollower,
            data_model=GithubUserFollowersData,
            bare=False,
            options=options,
        )

    def user_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowingInput],
    ) -> RunResult[GithubUserFollowingData]:
        """GitHub User Following

        List the GitHub users a given user follows by handle (each account's login,
        type, avatar, and profile URL) with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_following(handle="kentcdodds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_following", dict(input), options
        )
        return RunResult[GithubUserFollowingData].model_validate(raw)

    def iter_user_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowingInput],
    ) -> Paginator[GithubUserFollowingFollowing, GithubUserFollowingData]:
        """Iterate GitHub User Following results, following pagination cursors.

        Yields validated `GithubUserFollowingFollowing` items from the `following` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.user_following",
            dict(input),
            "following",
            item_model=GithubUserFollowingFollowing,
            data_model=GithubUserFollowingData,
            bare=False,
            options=options,
        )

    def user_pull_requests(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserPullRequestsInput],
    ) -> RunResult[GithubUserPullRequestsData]:
        """GitHub User Pull Requests

        List a GitHub user's public pull requests by handle (title, repository,
        state, creation date, and URL) with optional date filtering and pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_pull_requests(handle="torvalds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_pull_requests", dict(input), options
        )
        return RunResult[GithubUserPullRequestsData].model_validate(raw)

    def iter_user_pull_requests(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserPullRequestsInput],
    ) -> Paginator[GithubUserPullRequestsPullRequest, GithubUserPullRequestsData]:
        """Iterate GitHub User Pull Requests results, following pagination cursors.

        Yields validated `GithubUserPullRequestsPullRequest` items from the `pullRequests` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.user_pull_requests",
            dict(input),
            "pullRequests",
            item_model=GithubUserPullRequestsPullRequest,
            data_model=GithubUserPullRequestsData,
            bare=False,
            options=options,
        )

    def user_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserRepositoriesInput],
    ) -> RunResult[GithubUserRepositoriesData]:
        """GitHub User Repositories

        List a GitHub user's public repositories (name, description, language,
        stars, and forks) with sorting and cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_repositories(handle="torvalds")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_repositories", dict(input), options
        )
        return RunResult[GithubUserRepositoriesData].model_validate(raw)

    def iter_user_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserRepositoriesInput],
    ) -> Paginator[GithubUserRepositoriesRepo, GithubUserRepositoriesData]:
        """Iterate GitHub User Repositories results, following pagination cursors.

        Yields validated `GithubUserRepositoriesRepo` items from the `repos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "github.user_repositories",
            dict(input),
            "repos",
            item_model=GithubUserRepositoriesRepo,
            data_model=GithubUserRepositoriesData,
            bare=False,
            options=options,
        )


class AsyncGithubNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def issue_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubIssueCommentsInput],
    ) -> RunResult[GithubIssueCommentsData]:
        """GitHub Issue Comments

        List the comments on a GitHub issue or pull request by its URL, oldest
        first, with each commenter's login, their relationship to the repository,
        reactions and the comment text.

        Price: $0.0012 per request.

        Example:
            res = client.github.issue_comments(limit=10, url="https://github.com/openai/whisper/pull/1838")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.issue_comments", dict(input), options
        )
        return RunResult[GithubIssueCommentsData].model_validate(raw)

    def iter_issue_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubIssueCommentsInput],
    ) -> AsyncPaginator[GithubIssueCommentsComment, GithubIssueCommentsData]:
        """Iterate GitHub Issue Comments results, following pagination cursors.

        Yields validated `GithubIssueCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.issue_comments",
            dict(input),
            "comments",
            item_model=GithubIssueCommentsComment,
            data_model=GithubIssueCommentsData,
            bare=False,
            options=options,
        )

    async def repository(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryInput],
    ) -> RunResult[GithubRepositoryData]:
        """GitHub Repository

        Fetch a GitHub repository's metadata by URL (stars, forks, language, topics,
        license, and timestamps).

        Price: $0.0012 per request.

        Example:
            res = client.github.repository(url="https://github.com/facebook/react")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository", dict(input), options
        )
        return RunResult[GithubRepositoryData].model_validate(raw)

    async def repository_contributors(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryContributorsInput],
    ) -> RunResult[GithubRepositoryContributorsData]:
        """GitHub Repository Contributors

        List the people who have committed to a GitHub repository by repository URL,
        ordered by number of commits, with each contributor's login, profile URL and
        commit count. Look each one up with github.user for their profile, website
        and socials.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_contributors(limit=10, url="https://github.com/openai/whisper")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_contributors", dict(input), options
        )
        return RunResult[GithubRepositoryContributorsData].model_validate(raw)

    async def repository_forks(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryForksInput],
    ) -> RunResult[GithubRepositoryForksData]:
        """GitHub Repository Forks

        List the forks of a GitHub repository by repository URL, with each fork's
        owner, description, stars, language and last push. Sort by newest, oldest or
        most starred.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_forks(url="https://github.com/openai/whisper")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_forks", dict(input), options
        )
        return RunResult[GithubRepositoryForksData].model_validate(raw)

    async def repository_issues(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryIssuesInput],
    ) -> RunResult[GithubRepositoryIssuesData]:
        """GitHub Repository Issues

        List a GitHub repository's issues and pull requests by repository URL
        (GitHub lists pull requests as issues), with each one's author, state,
        labels, counts and body. Filter by state, sort and update date.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_issues(url="https://github.com/openai/whisper")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_issues", dict(input), options
        )
        return RunResult[GithubRepositoryIssuesData].model_validate(raw)

    async def repository_readme(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubRepositoryReadmeInput],
    ) -> RunResult[GithubRepositoryReadmeData]:
        """GitHub Repository README

        Get a GitHub repository's README by repository URL, as the Markdown text the
        maintainers wrote, with its file name, path and size. Use it to learn what a
        project does, which models and tools it uses, and how to reach its authors.

        Price: $0.0012 per request.

        Example:
            res = client.github.repository_readme(url="https://github.com/openai/whisper")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.repository_readme", dict(input), options
        )
        return RunResult[GithubRepositoryReadmeData].model_validate(raw)

    async def search_issues(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubSearchIssuesInput],
    ) -> RunResult[GithubSearchIssuesData]:
        """GitHub Issue and PR Search

        Search issues and pull requests across GitHub with GitHub's own search
        syntax (repo:, is:pr, is:issue, author:, label:, created:...), with each
        result's author, state, labels, counts and body. Use it to find who opens
        issues and pull requests on a repository.

        Price: $0.0024 per request.

        Example:
            res = client.github.search_issues(query="repo:openai/whisper is:pr")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.search_issues", dict(input), options
        )
        return RunResult[GithubSearchIssuesData].model_validate(raw)

    async def trending_developers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubTrendingDevelopersInput],
    ) -> RunResult[GithubTrendingDevelopersData]:
        """GitHub Trending Developers

        List trending GitHub developers (rank, username, name, avatar, and their
        most popular repository), optionally filtered by programming language and
        time range.

        Price: $0.0012 per request.

        Example:
            res = client.github.trending_developers(language="go", since="weekly")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.trending_developers", dict(input), options
        )
        return RunResult[GithubTrendingDevelopersData].model_validate(raw)

    async def trending_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubTrendingRepositoriesInput],
    ) -> RunResult[GithubTrendingRepositoriesData]:
        """GitHub Trending Repositories

        List GitHub Trending repositories (rank, stars, stars gained today,
        language, and description), filterable by language and time window.

        Price: $0.0012 per request.

        Example:
            res = client.github.trending_repositories(language="python", since="daily")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.trending_repositories", dict(input), options
        )
        return RunResult[GithubTrendingRepositoriesData].model_validate(raw)

    async def user(
        self, *, options: RequestOptions | None = None, **input: Unpack[GithubUserInput]
    ) -> RunResult[GithubUserData]:
        """GitHub User

        Fetch a GitHub user's public profile by handle (name, bio, company,
        location, followers, and repo counts).

        Price: $0.0012 per request.

        Example:
            res = client.github.user(handle="torvalds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user", dict(input), options
        )
        return RunResult[GithubUserData].model_validate(raw)

    async def user_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserActivityInput],
    ) -> RunResult[GithubUserActivityData]:
        """GitHub User Activity

        List a GitHub user's public contribution activity by handle (grouped monthly
        summaries of commits, pull requests, and issues with repository links) for a
        given year.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_activity(handle="kentcdodds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_activity", dict(input), options
        )
        return RunResult[GithubUserActivityData].model_validate(raw)

    def iter_user_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserActivityInput],
    ) -> AsyncPaginator[GithubUserActivityActivity, GithubUserActivityData]:
        """Iterate GitHub User Activity results, following pagination cursors.

        Yields validated `GithubUserActivityActivity` items from the `activity` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.user_activity",
            dict(input),
            "activity",
            item_model=GithubUserActivityActivity,
            data_model=GithubUserActivityData,
            bare=False,
            options=options,
        )

    async def user_contributions(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserContributionsInput],
    ) -> RunResult[GithubUserContributionsData]:
        """GitHub User Contributions

        Fetch a GitHub user's contribution graph for a year (total contributions
        plus per-day counts and heatmap intensity).

        Price: $0.0012 per request.

        Example:
            res = client.github.user_contributions(handle="torvalds", year=2024)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_contributions", dict(input), options
        )
        return RunResult[GithubUserContributionsData].model_validate(raw)

    async def user_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowersInput],
    ) -> RunResult[GithubUserFollowersData]:
        """GitHub User Followers

        List a GitHub user's followers by handle (each follower's login, type,
        avatar, and profile URL) with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_followers(handle="torvalds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_followers", dict(input), options
        )
        return RunResult[GithubUserFollowersData].model_validate(raw)

    def iter_user_followers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowersInput],
    ) -> AsyncPaginator[GithubUserFollowersFollower, GithubUserFollowersData]:
        """Iterate GitHub User Followers results, following pagination cursors.

        Yields validated `GithubUserFollowersFollower` items from the `followers` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.user_followers",
            dict(input),
            "followers",
            item_model=GithubUserFollowersFollower,
            data_model=GithubUserFollowersData,
            bare=False,
            options=options,
        )

    async def user_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowingInput],
    ) -> RunResult[GithubUserFollowingData]:
        """GitHub User Following

        List the GitHub users a given user follows by handle (each account's login,
        type, avatar, and profile URL) with pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_following(handle="kentcdodds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_following", dict(input), options
        )
        return RunResult[GithubUserFollowingData].model_validate(raw)

    def iter_user_following(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserFollowingInput],
    ) -> AsyncPaginator[GithubUserFollowingFollowing, GithubUserFollowingData]:
        """Iterate GitHub User Following results, following pagination cursors.

        Yields validated `GithubUserFollowingFollowing` items from the `following` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.user_following",
            dict(input),
            "following",
            item_model=GithubUserFollowingFollowing,
            data_model=GithubUserFollowingData,
            bare=False,
            options=options,
        )

    async def user_pull_requests(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserPullRequestsInput],
    ) -> RunResult[GithubUserPullRequestsData]:
        """GitHub User Pull Requests

        List a GitHub user's public pull requests by handle (title, repository,
        state, creation date, and URL) with optional date filtering and pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_pull_requests(handle="torvalds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_pull_requests", dict(input), options
        )
        return RunResult[GithubUserPullRequestsData].model_validate(raw)

    def iter_user_pull_requests(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserPullRequestsInput],
    ) -> AsyncPaginator[GithubUserPullRequestsPullRequest, GithubUserPullRequestsData]:
        """Iterate GitHub User Pull Requests results, following pagination cursors.

        Yields validated `GithubUserPullRequestsPullRequest` items from the `pullRequests` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.user_pull_requests",
            dict(input),
            "pullRequests",
            item_model=GithubUserPullRequestsPullRequest,
            data_model=GithubUserPullRequestsData,
            bare=False,
            options=options,
        )

    async def user_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserRepositoriesInput],
    ) -> RunResult[GithubUserRepositoriesData]:
        """GitHub User Repositories

        List a GitHub user's public repositories (name, description, language,
        stars, and forks) with sorting and cursor pagination.

        Price: $0.0012 per request.

        Example:
            res = client.github.user_repositories(handle="torvalds")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "github.user_repositories", dict(input), options
        )
        return RunResult[GithubUserRepositoriesData].model_validate(raw)

    def iter_user_repositories(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[GithubUserRepositoriesInput],
    ) -> AsyncPaginator[GithubUserRepositoriesRepo, GithubUserRepositoriesData]:
        """Iterate GitHub User Repositories results, following pagination cursors.

        Yields validated `GithubUserRepositoriesRepo` items from the `repos` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "github.user_repositories",
            dict(input),
            "repos",
            item_model=GithubUserRepositoriesRepo,
            data_model=GithubUserRepositoriesData,
            bare=False,
            options=options,
        )
