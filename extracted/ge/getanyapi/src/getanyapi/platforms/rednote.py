# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the rednote platform."""

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


class RednoteNoteInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) Note."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    noteId: Required[str]
    """RedNote (Xiaohongshu) note ID."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class RednoteNoteCommentsInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) Note Comments."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from the previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    noteId: Required[str]
    """RedNote (Xiaohongshu) note ID."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class RednoteProfileInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    userId: Required[str]
    """RedNote (Xiaohongshu) user ID."""


class RednoteSearchInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from the previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search for on RedNote (Xiaohongshu)."""
    sort: NotRequired[Literal["general", "hot", "time"]]
    """Sort order for matching notes. Default: general."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class RednoteSearchUsersInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) User Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from the previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Keyword to search for on RedNote (Xiaohongshu)."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class RednoteUserNotesInput(TypedDict, total=False):
    """Input for RedNote (Xiaohongshu) User Notes."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    cursor: NotRequired[str]
    """Pagination cursor from the previous response."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    userId: Required[str]
    """RedNote (Xiaohongshu) user ID."""


class RednoteNoteData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="URL of the author's avatar. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Display name of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_red_id: str | None = Field(
        default=None,
        alias="authorRedId",
        description="Author's public RedNote ID. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Identifier of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_verified: bool | None = Field(
        default=None,
        alias="authorVerified",
        description="Whether the author carries RedNote's official verification.",
    )
    collect_count: int | None = Field(
        default=None,
        alias="collectCount",
        description="Number of times the note was collected.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the note.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None,
        description="Note body text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the note cover image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    language: str | None = Field(
        default=None,
        description="Detected language of the note. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Number of likes on the note."
    )
    location: str | None = Field(
        default=None,
        description="Location the note was posted from, as RedNote reports it.",
    )
    note_id: str = Field(
        alias="noteId",
        description="Note identifier. Populated whenever the provider has data for the entity.",
    )
    share_count: int | None = Field(
        default=None,
        alias="shareCount",
        description="Number of times the note was shared.",
    )
    title: str | None = Field(
        default=None,
        description="Note title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Note type, e.g. "normal" or "video". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    url: str | None = Field(
        default=None,
        description="Canonical URL of the note. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class RednoteNoteCommentsData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    comments: list[RednoteNoteCommentsComment] = Field(
        description="Comments on the note. Populated whenever the provider has data for the entity."
    )
    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="Whether another page of comments is available.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of comments, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    total: int | None = Field(
        default=None, description="Total number of comments on the note."
    )


class RednoteNoteCommentsComment(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    comment_id: str = Field(
        alias="commentId",
        description="Comment identifier. Populated whenever the provider has data for the entity.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the author's avatar. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Number of likes on the comment."
    )
    nickname: str | None = Field(
        default=None,
        description="Display name of the comment author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    note_id: str | None = Field(
        default=None,
        alias="noteId",
        description="Identifier of the note the comment belongs to. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    red_id: str | None = Field(
        default=None,
        alias="redId",
        description="Author's public RedNote ID. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    reply_count: int | None = Field(
        default=None,
        alias="replyCount",
        description="Number of replies to the comment.",
    )
    text: str | None = Field(
        default=None,
        description="Comment text content. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    user_id: str | None = Field(
        default=None,
        alias="userId",
        description="Identifier of the comment author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class RednoteProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    collected_count: int | None = Field(default=None, alias="collectedCount")
    description: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    followers: int | None = None
    following: int | None = None
    gender: int | None = None
    image: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    liked_count: int | None = Field(default=None, alias="likedCount")
    location: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    nickname: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    posted_notes: int | None = Field(default=None, alias="postedNotes")
    red_id: str | None = Field(
        default=None,
        alias="redId",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    share_url: str | None = Field(
        default=None,
        alias="shareUrl",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    user_id: str = Field(
        alias="userId",
        description="Populated whenever the provider has data for the entity.",
    )
    verified: bool | None = None
    verify_type: int | None = Field(default=None, alias="verifyType")


class RednoteSearchData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of notes, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    notes: list[RednoteSearchNote] = Field(
        description="Notes matching the search. Populated whenever the provider has data for the entity."
    )


class RednoteSearchNote(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="URL of the author's avatar. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Display name of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_red_id: str | None = Field(
        default=None,
        alias="authorRedId",
        description="Author's public RedNote ID. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Identifier of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    collect_count: int | None = Field(
        default=None,
        alias="collectCount",
        description="Number of times the note was collected.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the note.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str | None = Field(
        default=None,
        description="Note body text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the note cover image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Number of likes on the note."
    )
    note_id: str = Field(
        alias="noteId",
        description="Note identifier. Populated whenever the provider has data for the entity.",
    )
    share_count: int | None = Field(
        default=None,
        alias="shareCount",
        description="Number of times the note was shared.",
    )
    title: str | None = Field(
        default=None,
        description="Note title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Note type, e.g. "normal" or "video". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    xsec_token: str | None = Field(
        default=None,
        alias="xsecToken",
        description="Security token required to fetch the note's full detail. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )


class RednoteSearchUsersData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of users, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    users: list[RednoteSearchUsersUser] = Field(
        description="Populated whenever the provider has data for the entity."
    )


class RednoteSearchUsersUser(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    description: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    link: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    name: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    red_id: str | None = Field(
        default=None,
        alias="redId",
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    subtitle: str | None = Field(
        default=None,
        description="Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    user_id: str = Field(
        alias="userId",
        description="Populated whenever the provider has data for the entity.",
    )
    verified: bool | None = None
    verify_type: int | None = Field(default=None, alias="verifyType")


class RednoteUserNotesData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    has_more: bool | None = Field(
        default=None,
        alias="hasMore",
        description="Whether another page of notes is available.",
    )
    next_cursor: str | None = Field(
        alias="nextCursor",
        description="Opaque cursor for the next page of notes, or null when this lane has no more. Pass it back as cursor to continue.",
    )
    notes: list[RednoteUserNotesNote] = Field(
        description="The user's notes. Populated whenever the provider has data for the entity."
    )


class RednoteUserNotesNote(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None,
        alias="authorImage",
        description="URL of the author's avatar. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_nickname: str | None = Field(
        default=None,
        alias="authorNickname",
        description="Display name of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_user_id: str | None = Field(
        default=None,
        alias="authorUserId",
        description="Identifier of the note author. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    collect_count: int | None = Field(
        default=None,
        alias="collectCount",
        description="Number of times the note was collected.",
    )
    comment_count: int | None = Field(
        default=None,
        alias="commentCount",
        description="Number of comments on the note.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    description: str | None = Field(
        default=None,
        description="Note body text. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    image: str | None = Field(
        default=None,
        description="URL of the note cover image. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    like_count: int | None = Field(
        default=None, alias="likeCount", description="Number of likes on the note."
    )
    note_id: str = Field(
        alias="noteId",
        description="Note identifier. Populated whenever the provider has data for the entity.",
    )
    share_count: int | None = Field(
        default=None,
        alias="shareCount",
        description="Number of times the note was shared.",
    )
    title: str | None = Field(
        default=None,
        description="Note title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    type_: str | None = Field(
        default=None,
        alias="type",
        description='Note type, e.g. "normal" or "video". Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.',
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class RednoteNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def note(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteInput],
    ) -> RunResult[RednoteNoteData]:
        """RedNote (Xiaohongshu) Note

        Look up a RedNote (Xiaohongshu) note by note ID and return normalized note
        details.

        Price: $0.012 per request.

        Example:
            res = client.rednote.note(noteId="6a8fe7c20000000026003bbf")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.note", dict(input), options
        )
        return RunResult[RednoteNoteData].model_validate(raw)

    def note_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteCommentsInput],
    ) -> RunResult[RednoteNoteCommentsData]:
        """RedNote (Xiaohongshu) Note Comments

        List comments on a RedNote (Xiaohongshu) note and return normalized comment
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.note_comments(noteId="68dd422c0000000203019829")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.note_comments", dict(input), options
        )
        return RunResult[RednoteNoteCommentsData].model_validate(raw)

    def iter_note_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteCommentsInput],
    ) -> Paginator[RednoteNoteCommentsComment, RednoteNoteCommentsData]:
        """Iterate RedNote (Xiaohongshu) Note Comments results, following pagination cursors.

        Yields validated `RednoteNoteCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "rednote.note_comments",
            dict(input),
            "comments",
            item_model=RednoteNoteCommentsComment,
            data_model=RednoteNoteCommentsData,
            bare=False,
            options=options,
        )

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteProfileInput],
    ) -> RunResult[RednoteProfileData]:
        """RedNote (Xiaohongshu) Profile

        Look up a RedNote (Xiaohongshu) profile by user ID and return normalized
        profile details.

        Price: $0.012 per request.

        Example:
            res = client.rednote.profile(userId="56b0a4491c07df6365277af7")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.profile", dict(input), options
        )
        return RunResult[RednoteProfileData].model_validate(raw)

    def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchInput],
    ) -> RunResult[RednoteSearchData]:
        """RedNote (Xiaohongshu) Search

        Search RedNote (Xiaohongshu) notes by keyword and return normalized note
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.search(query="coffee", sort="general")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.search", dict(input), options
        )
        return RunResult[RednoteSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchInput],
    ) -> Paginator[RednoteSearchNote, RednoteSearchData]:
        """Iterate RedNote (Xiaohongshu) Search results, following pagination cursors.

        Yields validated `RednoteSearchNote` items from the `notes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "rednote.search",
            dict(input),
            "notes",
            item_model=RednoteSearchNote,
            data_model=RednoteSearchData,
            bare=False,
            options=options,
        )

    def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchUsersInput],
    ) -> RunResult[RednoteSearchUsersData]:
        """RedNote (Xiaohongshu) User Search

        Search RedNote (Xiaohongshu) users by keyword and return normalized user
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.search_users(query="coffee")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.search_users", dict(input), options
        )
        return RunResult[RednoteSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchUsersInput],
    ) -> Paginator[RednoteSearchUsersUser, RednoteSearchUsersData]:
        """Iterate RedNote (Xiaohongshu) User Search results, following pagination cursors.

        Yields validated `RednoteSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "rednote.search_users",
            dict(input),
            "users",
            item_model=RednoteSearchUsersUser,
            data_model=RednoteSearchUsersData,
            bare=False,
            options=options,
        )

    def user_notes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteUserNotesInput],
    ) -> RunResult[RednoteUserNotesData]:
        """RedNote (Xiaohongshu) User Notes

        List notes posted by a RedNote (Xiaohongshu) user and return normalized note
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.user_notes(userId="56b0a4491c07df6365277af7")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.user_notes", dict(input), options
        )
        return RunResult[RednoteUserNotesData].model_validate(raw)

    def iter_user_notes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteUserNotesInput],
    ) -> Paginator[RednoteUserNotesNote, RednoteUserNotesData]:
        """Iterate RedNote (Xiaohongshu) User Notes results, following pagination cursors.

        Yields validated `RednoteUserNotesNote` items from the `notes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return paginate(
            self._client,
            "rednote.user_notes",
            dict(input),
            "notes",
            item_model=RednoteUserNotesNote,
            data_model=RednoteUserNotesData,
            bare=False,
            options=options,
        )


class AsyncRednoteNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def note(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteInput],
    ) -> RunResult[RednoteNoteData]:
        """RedNote (Xiaohongshu) Note

        Look up a RedNote (Xiaohongshu) note by note ID and return normalized note
        details.

        Price: $0.012 per request.

        Example:
            res = client.rednote.note(noteId="6a8fe7c20000000026003bbf")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.note", dict(input), options
        )
        return RunResult[RednoteNoteData].model_validate(raw)

    async def note_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteCommentsInput],
    ) -> RunResult[RednoteNoteCommentsData]:
        """RedNote (Xiaohongshu) Note Comments

        List comments on a RedNote (Xiaohongshu) note and return normalized comment
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.note_comments(noteId="68dd422c0000000203019829")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.note_comments", dict(input), options
        )
        return RunResult[RednoteNoteCommentsData].model_validate(raw)

    def iter_note_comments(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteNoteCommentsInput],
    ) -> AsyncPaginator[RednoteNoteCommentsComment, RednoteNoteCommentsData]:
        """Iterate RedNote (Xiaohongshu) Note Comments results, following pagination cursors.

        Yields validated `RednoteNoteCommentsComment` items from the `comments` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "rednote.note_comments",
            dict(input),
            "comments",
            item_model=RednoteNoteCommentsComment,
            data_model=RednoteNoteCommentsData,
            bare=False,
            options=options,
        )

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteProfileInput],
    ) -> RunResult[RednoteProfileData]:
        """RedNote (Xiaohongshu) Profile

        Look up a RedNote (Xiaohongshu) profile by user ID and return normalized
        profile details.

        Price: $0.012 per request.

        Example:
            res = client.rednote.profile(userId="56b0a4491c07df6365277af7")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.profile", dict(input), options
        )
        return RunResult[RednoteProfileData].model_validate(raw)

    async def search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchInput],
    ) -> RunResult[RednoteSearchData]:
        """RedNote (Xiaohongshu) Search

        Search RedNote (Xiaohongshu) notes by keyword and return normalized note
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.search(query="coffee", sort="general")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.search", dict(input), options
        )
        return RunResult[RednoteSearchData].model_validate(raw)

    def iter_search(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchInput],
    ) -> AsyncPaginator[RednoteSearchNote, RednoteSearchData]:
        """Iterate RedNote (Xiaohongshu) Search results, following pagination cursors.

        Yields validated `RednoteSearchNote` items from the `notes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "rednote.search",
            dict(input),
            "notes",
            item_model=RednoteSearchNote,
            data_model=RednoteSearchData,
            bare=False,
            options=options,
        )

    async def search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchUsersInput],
    ) -> RunResult[RednoteSearchUsersData]:
        """RedNote (Xiaohongshu) User Search

        Search RedNote (Xiaohongshu) users by keyword and return normalized user
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.search_users(query="coffee")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.search_users", dict(input), options
        )
        return RunResult[RednoteSearchUsersData].model_validate(raw)

    def iter_search_users(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteSearchUsersInput],
    ) -> AsyncPaginator[RednoteSearchUsersUser, RednoteSearchUsersData]:
        """Iterate RedNote (Xiaohongshu) User Search results, following pagination cursors.

        Yields validated `RednoteSearchUsersUser` items from the `users` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "rednote.search_users",
            dict(input),
            "users",
            item_model=RednoteSearchUsersUser,
            data_model=RednoteSearchUsersData,
            bare=False,
            options=options,
        )

    async def user_notes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteUserNotesInput],
    ) -> RunResult[RednoteUserNotesData]:
        """RedNote (Xiaohongshu) User Notes

        List notes posted by a RedNote (Xiaohongshu) user and return normalized note
        records with pagination.

        Price: $0.012 per request.

        Example:
            res = client.rednote.user_notes(userId="56b0a4491c07df6365277af7")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "rednote.user_notes", dict(input), options
        )
        return RunResult[RednoteUserNotesData].model_validate(raw)

    def iter_user_notes(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[RednoteUserNotesInput],
    ) -> AsyncPaginator[RednoteUserNotesNote, RednoteUserNotesData]:
        """Iterate RedNote (Xiaohongshu) User Notes results, following pagination cursors.

        Yields validated `RednoteUserNotesNote` items from the `notes` field of
        each page. Use `.pages()` on the returned paginator to walk whole
        `RunResult` pages.
        """
        return apaginate(
            self._client,
            "rednote.user_notes",
            dict(input),
            "notes",
            item_model=RednoteUserNotesNote,
            data_model=RednoteUserNotesData,
            bare=False,
            options=options,
        )
