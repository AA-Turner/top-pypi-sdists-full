# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the substack platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class SubstackPostsInput(TypedDict, total=False):
    """Input for Substack Posts."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    contentType: NotRequired[Literal["all", "newsletter", "podcast", "thread"]]
    """Restrict to a single post type, or 'all' (e.g. newsletter). Default: all."""
    endDate: NotRequired[str]
    """Only return posts published on or before this date, format YYYY-MM-DD (e.g. 2024-12-31). Applied within the most recent 'limit' posts scanned."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    includeComments: NotRequired[bool]
    """Include public comment threads and their direct replies on each post (e.g. true). Default: false."""
    includeContent: NotRequired[bool]
    """Include the full article body as text, HTML and Markdown. Set false for metadata only, which is faster (e.g. false). Default: true."""
    limit: NotRequired[int]
    """Maximum number of recent posts to return when given a publication URL (1-100, default 25); ignored for a single post URL, which always returns that one post. You are billed per post returned, so a lower limit costs less. Range: 1 to 100."""
    maxComments: NotRequired[int]
    """Maximum comments collected per post when 'includeComments' is true (0-500, default 20). Costs nothing extra (e.g. 50). Range: 0 to 500."""
    minComments: NotRequired[int]
    """Only return posts with at least this many comments (e.g. 10). Minimum: 0."""
    minReactions: NotRequired[int]
    """Only return posts with at least this many reactions (e.g. 100). Minimum: 0."""
    minWordCount: NotRequired[int]
    """Only return posts with at least this many words, which filters out short notes and announcements (e.g. 1000). Minimum: 0."""
    onlyFree: NotRequired[bool]
    """Return only free (non-paywalled) posts (e.g. true). Default: false."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    startDate: NotRequired[str]
    """Only return posts published on or after this date, format YYYY-MM-DD (e.g. 2024-01-01). Applied within the most recent 'limit' posts scanned, so raise 'limit' to reach older date ranges."""
    url: Required[str]
    """Either a Substack publication URL / custom domain to fetch its recent posts (e.g. https://www.astralcodexten.com), OR a single post URL to fetch just that one article with full content (e.g. https://www.astralcodexten.com/p/your-book-review)."""


class SubstackPostsData(BaseModel):
    items: list[SubstackPostsItem] = Field(
        description="Post records: title, subtitle, URL, publish date, paywall status, word count, engagement (reactions, comments, restacks), author profile, publication details, the article body as text, HTML and Markdown, and comment threads when requested. Populated whenever the provider has data for the entity."
    )


class SubstackPostsItem(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_bio: str | None = Field(
        default=None,
        alias="authorBio",
        description="Author bio as shown on their Substack profile.",
    )
    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Substack handle of the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile photo URL of the post author.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the post author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Substack profile URL of the post author.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of top-level comments on the post.",
    )
    comments: list[SubstackPostsComment] | None = Field(
        default=None,
        description="Top-level comment threads on the post, each with its direct replies. Empty unless 'includeComments' is true. Replies nested more than one level deep are not returned.",
    )
    content_status: str | None = Field(
        default=None,
        alias="contentStatus",
        description="How much of the article body this record carries: 'full' for the whole article, 'preview_only' for the public excerpt of a paywalled post, 'metadata_only' when no body was requested or available, or 'failed' when extraction failed. Read this before trusting 'text', 'html', or 'markdown'. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None,
        description="Short post description, usually the subtitle or an excerpt.",
    )
    has_voiceover: bool | None = Field(
        default=None,
        alias="hasVoiceover",
        description="Whether the post carries a narrated audio version.",
    )
    html: str | None = Field(
        default=None,
        description="Article body as HTML. Present when 'includeContent' is true and 'contentStatus' is 'full' or 'preview_only'.",
    )
    image: str | None = Field(default=None, description="Cover image URL.")
    is_paid: bool | None = Field(
        default=None,
        alias="isPaid",
        description="Whether the post is behind a paywall.",
    )
    language: str | None = Field(
        default=None, description="Two-letter language code of the post."
    )
    markdown: str | None = Field(
        default=None,
        description="Article body as Markdown. Present when 'includeContent' is true and 'contentStatus' is 'full' or 'preview_only'.",
    )
    podcast_url: str | None = Field(
        default=None,
        alias="podcastUrl",
        description="Audio URL for a podcast post or a narrated voiceover, when the post has one.",
    )
    post_id: str | None = Field(
        default=None,
        alias="postId",
        description="Substack post identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    post_type: str | None = Field(
        default=None,
        alias="postType",
        description="Post type (newsletter, podcast, or thread). Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    publication: SubstackPostsPublication | None = Field(
        default=None, description="The publication the post belongs to."
    )
    reaction_count: int | None = Field(
        default=None,
        alias="reactionCount",
        description="Number of reactions (likes) on the post.",
    )
    reply_count: int | None = Field(
        default=None,
        alias="replyCount",
        description="Number of replies to comments on the post.",
    )
    restack_count: int | None = Field(
        default=None,
        alias="restackCount",
        description="Number of times the post was restacked.",
    )
    slug: str | None = Field(
        default=None,
        description="Post slug, the last path segment of the post URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    subtitle: str | None = Field(default=None, description="Post subtitle or deck.")
    text: str | None = Field(
        default=None,
        description="Article body as plain text. Present when 'includeContent' is true and 'contentStatus' is 'full' or 'preview_only'.",
    )
    title: str = Field(
        description="Post title. Populated whenever the provider has data for the entity."
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical post URL. Populated whenever the provider has data for the entity."
    )
    wordcount: int | None = Field(
        default=None, description="Approximate word count of the article."
    )


class SubstackPostsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Substack handle of the comment author.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile photo URL of the comment author.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the comment author.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Substack profile URL of the comment author.",
    )
    comment_id: str = Field(
        alias="commentId", description="Substack comment identifier."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    edited_utc: float | None = Field(
        default=None,
        alias="editedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    is_author: bool | None = Field(
        default=None,
        alias="isAuthor",
        description="Whether the comment was written by the post author.",
    )
    is_pinned: bool | None = Field(
        default=None,
        alias="isPinned",
        description="Whether the comment is pinned by the publication.",
    )
    reaction_count: int | None = Field(
        default=None,
        alias="reactionCount",
        description="Number of reactions on the comment.",
    )
    replies: list[SubstackPostsReplie] | None = Field(
        default=None, description="Direct replies to this comment."
    )
    restack_count: int | None = Field(
        default=None,
        alias="restackCount",
        description="Number of times the comment was restacked.",
    )
    text: str | None = Field(default=None, description="Comment body text.")


class SubstackPostsReplie(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_handle: str | None = Field(
        default=None,
        alias="authorHandle",
        description="Substack handle of the reply author.",
    )
    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="Profile photo URL of the reply author.",
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Display name of the reply author.",
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Substack profile URL of the reply author.",
    )
    comment_id: str = Field(
        alias="commentId", description="Substack comment identifier."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    edited_utc: float | None = Field(
        default=None,
        alias="editedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    is_author: bool | None = Field(
        default=None,
        alias="isAuthor",
        description="Whether the reply was written by the post author.",
    )
    is_pinned: bool | None = Field(
        default=None,
        alias="isPinned",
        description="Whether the reply is pinned by the publication.",
    )
    reaction_count: int | None = Field(
        default=None,
        alias="reactionCount",
        description="Number of reactions on the reply.",
    )
    restack_count: int | None = Field(
        default=None,
        alias="restackCount",
        description="Number of times the reply was restacked.",
    )
    text: str | None = Field(default=None, description="Reply body text.")


class SubstackPostsPublication(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    custom_domain: str | None = Field(
        default=None,
        alias="customDomain",
        description="Custom domain the publication is served on, when it has one.",
    )
    description: str | None = Field(
        default=None, description="Publication tagline or hero text."
    )
    id: str | None = Field(default=None, description="Substack publication identifier.")
    image: str | None = Field(default=None, description="Publication logo URL.")
    language: str | None = Field(
        default=None, description="Two-letter language code of the publication."
    )
    name: str | None = Field(default=None, description="Publication name.")
    payments_enabled: bool | None = Field(
        default=None,
        alias="paymentsEnabled",
        description="Whether the publication sells paid subscriptions.",
    )
    subdomain: str | None = Field(
        default=None, description="Publication subdomain on substack.com."
    )
    subscriber_count: int | None = Field(
        default=None,
        alias="subscriberCount",
        description="Subscriber count, when the publication publishes it.",
    )
    url: str | None = Field(default=None, description="Publication home URL.")


class SubstackNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SubstackPostsInput],
    ) -> RunResult[SubstackPostsData]:
        """Substack Posts

        Pull posts from any Substack publication by its URL, or pass a single post
        URL (…/p/slug) to fetch just that one article. Returns title, subtitle,
        publish date, paywall status, word count, engagement (reactions, comments,
        restacks), author profile, publication details, the full article body as
        text, HTML and Markdown, and optional comment threads.

        Price: $0.00039 per request plus $0.00044 per result (maximum $0.0444).

        Example:
            res = client.substack.posts(limit=3, url="https://www.astralcodexten.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "substack.posts", dict(input), options
        )
        return RunResult[SubstackPostsData].model_validate(raw)


class AsyncSubstackNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def posts(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[SubstackPostsInput],
    ) -> RunResult[SubstackPostsData]:
        """Substack Posts

        Pull posts from any Substack publication by its URL, or pass a single post
        URL (…/p/slug) to fetch just that one article. Returns title, subtitle,
        publish date, paywall status, word count, engagement (reactions, comments,
        restacks), author profile, publication details, the full article body as
        text, HTML and Markdown, and optional comment threads.

        Price: $0.00039 per request plus $0.00044 per result (maximum $0.0444).

        Example:
            res = client.substack.posts(limit=3, url="https://www.astralcodexten.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "substack.posts", dict(input), options
        )
        return RunResult[SubstackPostsData].model_validate(raw)
