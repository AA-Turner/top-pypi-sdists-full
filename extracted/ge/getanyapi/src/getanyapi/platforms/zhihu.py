# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the zhihu platform."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class ZhihuAnswerInput(TypedDict, total=False):
    """Input for Zhihu Answer."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    answerId: Required[str]
    """Zhihu answer identifier."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ZhihuProfileInput(TypedDict, total=False):
    """Input for Zhihu Profile."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    userToken: Required[str]
    """Zhihu user URL token."""


class ZhihuQuestionInput(TypedDict, total=False):
    """Input for Zhihu Question."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    questionId: Required[str]
    """Zhihu question identifier."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ZhihuQuestionAnswersInput(TypedDict, total=False):
    """Input for Zhihu Question Answers."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[int]
    """Number of answers requested on the first page. Pagination is not supported. Default: 5."""
    order: NotRequired[Literal["default", "updated"]]
    """Answer ordering: default ranking or recently updated. Default: default."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    questionId: Required[str]
    """Zhihu question identifier."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class ZhihuSearchArticlesInput(TypedDict, total=False):
    """Input for Zhihu Article Search."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    limit: NotRequired[str]
    """Number of articles requested per page. Default: 20."""
    offset: NotRequired[str]
    """Result offset returned as nextOffset in the previous response. Default: 0."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    query: Required[str]
    """Search keyword."""
    searchHashId: NotRequired[str]
    """Search hash identifier returned in the previous response. Default: ."""
    showAllTopics: NotRequired[int]
    """Whether to include all topics: 0 excludes them and 1 includes them. Default: 0."""
    sort: NotRequired[Literal["", "upvoted_count", "created_time"]]
    """Article ordering: comprehensive, most upvoted, or newest. Default: ."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""
    timeInterval: NotRequired[
        Literal[
            "", "a_day", "a_week", "a_month", "three_months", "half_a_year", "a_year"
        ]
    ]
    """Optional publication-time filter. Default: ."""
    verticalInfo: NotRequired[str]
    """Article-search vertical continuation state returned as nextVerticalInfo in the previous response. Default: 0,0,0,0,0,0,0,0,0,2,0,0."""


class ZhihuAnswerData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_headline: str | None = Field(
        default=None, alias="authorHeadline", description="Author headline."
    )
    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_token: str | None = Field(
        default=None, alias="authorToken", description="Author URL token."
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Zhihu profile.",
    )
    author_user_id: str | None = Field(
        default=None, alias="authorUserId", description="Author identifier."
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    excerpt: str | None = Field(
        default=None,
        description="Answer excerpt. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Answer identifier. Populated whenever the provider has data for the entity."
    )
    question_id: str | None = Field(
        default=None,
        alias="questionId",
        description="Parent question identifier. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    question_title: str | None = Field(
        default=None,
        alias="questionTitle",
        description="Parent question title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    text: str | None = Field(
        default=None,
        description="Full body text of the answer, with HTML markup stripped.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="Last update UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical answer URL. Populated whenever the provider has data for the entity."
    )


class ZhihuProfileData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    answers: int | None = Field(default=None, description="Published answer count.")
    articles: int | None = Field(default=None, description="Published article count.")
    followers: int | None = Field(default=None, description="Follower count.")
    gender: int | None = Field(
        default=None, description="Gender code reported by Zhihu."
    )
    headline: str | None = Field(
        default=None,
        description="Profile headline. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="User identifier. Populated whenever the provider has data for the entity."
    )
    image: str | None = Field(
        default=None,
        description="Profile image URL. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    ip_location: str | None = Field(
        default=None,
        alias="ipLocation",
        description="IP location label reported by Zhihu.",
    )
    name: str | None = Field(
        default=None,
        description="Display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    organization: bool | None = Field(
        default=None, description="Whether this is an organization profile."
    )
    url: str = Field(
        description="Canonical profile URL. Populated whenever the provider has data for the entity."
    )
    user_token: str = Field(
        alias="userToken",
        description="User URL token. Populated whenever the provider has data for the entity.",
    )


class ZhihuQuestionData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    answers: int | None = Field(default=None, description="Answer count.")
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    description: str | None = Field(
        default=None,
        description="Question body as returned by Zhihu. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    excerpt: str | None = Field(default=None, description="Short question excerpt.")
    followers: int | None = Field(default=None, description="Follower count.")
    id: str = Field(
        description="Question identifier. Populated whenever the provider has data for the entity."
    )
    title: str | None = Field(
        default=None,
        description="Question title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="Last update UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical question URL. Populated whenever the provider has data for the entity."
    )
    views: int | None = Field(default=None, description="View count.")


class ZhihuQuestionAnswersData(BaseModel):
    answers: list[ZhihuQuestionAnswersAnswer] = Field(
        description="Normalized answers. Populated whenever the provider has data for the entity."
    )


class ZhihuQuestionAnswersAnswer(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_headline: str | None = Field(
        default=None,
        alias="authorHeadline",
        description="One-line headline the author shows on their Zhihu profile.",
    )
    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_token: str | None = Field(
        default=None, alias="authorToken", description="Author URL token."
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Zhihu profile.",
    )
    author_user_id: str | None = Field(
        default=None, alias="authorUserId", description="Author identifier."
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    excerpt: str | None = Field(
        default=None,
        description="Answer excerpt. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Answer identifier. Populated whenever the provider has data for the entity."
    )
    question_id: str | None = Field(
        default=None,
        alias="questionId",
        description="Zhihu ID of the question the answer belongs to.",
    )
    question_title: str | None = Field(
        default=None,
        alias="questionTitle",
        description="Title of the question the answer belongs to.",
    )
    saves: int | None = Field(default=None, description="Save count.")
    text: str | None = Field(
        default=None,
        description="Full body text of the answer, with HTML markup stripped.",
    )
    thanks: int | None = Field(default=None, description="Thanks count.")
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="Last update UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical answer URL. Populated whenever the provider has data for the entity."
    )
    votes: int | None = Field(default=None, description="Upvote count.")


class ZhihuSearchArticlesData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    articles: list[ZhihuSearchArticlesArticle] = Field(
        description="Normalized article results. Populated whenever the provider has data for the entity."
    )
    is_end: bool = Field(
        alias="isEnd", description="Whether the result set has reached its final page."
    )
    next_offset: str = Field(
        alias="nextOffset",
        description="Result offset to pass as offset when requesting the next page.",
    )
    next_vertical_info: str = Field(
        alias="nextVerticalInfo",
        description="Article-search vertical continuation state to pass as verticalInfo when requesting the next page.",
    )
    search_hash_id: str = Field(
        alias="searchHashId",
        description="Search hash identifier to pass when requesting another page.",
    )


class ZhihuSearchArticlesArticle(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    author_image: str | None = Field(
        default=None, alias="authorImage", description="Author avatar URL."
    )
    author_name: str | None = Field(
        default=None,
        alias="authorName",
        description="Author display name. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    author_token: str | None = Field(
        default=None, alias="authorToken", description="Author URL token."
    )
    author_url: str | None = Field(
        default=None,
        alias="authorUrl",
        description="Canonical URL of the author's Zhihu profile.",
    )
    author_user_id: str | None = Field(
        default=None, alias="authorUserId", description="Author identifier."
    )
    comments: int | None = Field(default=None, description="Comment count.")
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    excerpt: str | None = Field(
        default=None,
        description="Article excerpt. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    id: str = Field(
        description="Article identifier. Populated whenever the provider has data for the entity."
    )
    saves: int | None = Field(
        default=None,
        description="Number of times the article was saved to a collection.",
    )
    text: str | None = Field(
        default=None,
        description="Full body text of the article, with HTML markup stripped.",
    )
    title: str | None = Field(
        default=None,
        description="Article title. Populated whenever the provider has data for the entity. Present whenever the upstream returns this record.",
    )
    updated_utc: float | None = Field(
        default=None,
        alias="updatedUtc",
        description="Last update UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    url: str = Field(
        description="Canonical article URL. Populated whenever the provider has data for the entity."
    )
    votes: int | None = Field(default=None, description="Upvote count.")


class ZhihuNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def answer(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuAnswerInput],
    ) -> RunResult[ZhihuAnswerData]:
        """Zhihu Answer

        Fetch a public Zhihu answer with normalized author and question data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.answer(answerId="2054145988235880002")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.answer", dict(input), options
        )
        return RunResult[ZhihuAnswerData].model_validate(raw)

    def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuProfileInput],
    ) -> RunResult[ZhihuProfileData]:
        """Zhihu Profile

        Fetch a public Zhihu profile with normalized identity and audience data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.profile(userToken="ming-he-43-93")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.profile", dict(input), options
        )
        return RunResult[ZhihuProfileData].model_validate(raw)

    def question(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuQuestionInput],
    ) -> RunResult[ZhihuQuestionData]:
        """Zhihu Question

        Fetch a public Zhihu question with normalized text and engagement
        statistics.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.question(questionId="37811449")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.question", dict(input), options
        )
        return RunResult[ZhihuQuestionData].model_validate(raw)

    def question_answers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuQuestionAnswersInput],
    ) -> RunResult[ZhihuQuestionAnswersData]:
        """Zhihu Question Answers

        List the first page of public answers to a Zhihu question with normalized
        authors and engagement data. Pagination is not supported.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.question_answers(limit=5, order="default", questionId="37811449")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.question_answers", dict(input), options
        )
        return RunResult[ZhihuQuestionAnswersData].model_validate(raw)

    def search_articles(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuSearchArticlesInput],
    ) -> RunResult[ZhihuSearchArticlesData]:
        """Zhihu Article Search

        Search public Zhihu articles by keyword with normalized author and
        engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.search_articles(limit="20", query="deepseek", showAllTopics=0)
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.search_articles", dict(input), options
        )
        return RunResult[ZhihuSearchArticlesData].model_validate(raw)


class AsyncZhihuNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def answer(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuAnswerInput],
    ) -> RunResult[ZhihuAnswerData]:
        """Zhihu Answer

        Fetch a public Zhihu answer with normalized author and question data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.answer(answerId="2054145988235880002")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.answer", dict(input), options
        )
        return RunResult[ZhihuAnswerData].model_validate(raw)

    async def profile(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuProfileInput],
    ) -> RunResult[ZhihuProfileData]:
        """Zhihu Profile

        Fetch a public Zhihu profile with normalized identity and audience data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.profile(userToken="ming-he-43-93")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.profile", dict(input), options
        )
        return RunResult[ZhihuProfileData].model_validate(raw)

    async def question(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuQuestionInput],
    ) -> RunResult[ZhihuQuestionData]:
        """Zhihu Question

        Fetch a public Zhihu question with normalized text and engagement
        statistics.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.question(questionId="37811449")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.question", dict(input), options
        )
        return RunResult[ZhihuQuestionData].model_validate(raw)

    async def question_answers(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuQuestionAnswersInput],
    ) -> RunResult[ZhihuQuestionAnswersData]:
        """Zhihu Question Answers

        List the first page of public answers to a Zhihu question with normalized
        authors and engagement data. Pagination is not supported.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.question_answers(limit=5, order="default", questionId="37811449")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.question_answers", dict(input), options
        )
        return RunResult[ZhihuQuestionAnswersData].model_validate(raw)

    async def search_articles(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[ZhihuSearchArticlesInput],
    ) -> RunResult[ZhihuSearchArticlesData]:
        """Zhihu Article Search

        Search public Zhihu articles by keyword with normalized author and
        engagement data.

        Price: $0.0012 per request.

        Example:
            res = client.zhihu.search_articles(limit="20", query="deepseek", showAllTopics=0)
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "zhihu.search_articles", dict(input), options
        )
        return RunResult[ZhihuSearchArticlesData].model_validate(raw)
