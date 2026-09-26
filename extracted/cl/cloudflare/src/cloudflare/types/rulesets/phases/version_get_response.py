# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..kind import Kind
from ..phase import Phase
from ..logging import Logging
from ..log_rule import LogRule
from ...._models import BaseModel
from ..skip_rule import SkipRule
from ..block_rule import BlockRule
from ..route_rule import RouteRule
from ..score_rule import ScoreRule
from ..execute_rule import ExecuteRule
from ..rewrite_rule import RewriteRule
from ..redirect_rule import RedirectRule
from ..set_config_rule import SetConfigRule
from ..serve_error_rule import ServeErrorRule
from ..ddos_dynamic_rule import DDoSDynamicRule
from ..log_custom_field_rule import LogCustomFieldRule
from ..compress_response_rule import CompressResponseRule
from ..managed_challenge_rule import ManagedChallengeRule
from ..set_cache_settings_rule import SetCacheSettingsRule
from ..force_connection_close_rule import ForceConnectionCloseRule

__all__ = [
    "VersionGetResponse",
    "Rule",
    "RuleBlockRule",
    "RuleChallengeRule",
    "RuleChallengeRuleExposedCredentialCheck",
    "RuleChallengeRuleRatelimit",
    "RuleResponseCompressionRule",
    "RuleDDoSDynamicRule",
    "RuleExecuteRule",
    "RuleForceConnectionCloseRule",
    "RuleJavaScriptChallengeRule",
    "RuleJavaScriptChallengeRuleExposedCredentialCheck",
    "RuleJavaScriptChallengeRuleRatelimit",
    "RuleLogRule",
    "RuleLogCustomFieldRule",
    "RuleManagedChallengeRule",
    "RuleRedirectRule",
    "RuleRewriteRule",
    "RuleRouteRule",
    "RuleScoreRule",
    "RuleServeErrorRule",
    "RuleSetCacheControlRule",
    "RuleSetCacheControlRuleActionParameters",
    "RuleSetCacheControlRuleActionParametersImmutable",
    "RuleSetCacheControlRuleActionParametersImmutableSetDirective",
    "RuleSetCacheControlRuleActionParametersImmutableRemoveDirective",
    "RuleSetCacheControlRuleActionParametersMaxAge",
    "RuleSetCacheControlRuleActionParametersMaxAgeSetDirective",
    "RuleSetCacheControlRuleActionParametersMaxAgeRemoveDirective",
    "RuleSetCacheControlRuleActionParametersMustRevalidate",
    "RuleSetCacheControlRuleActionParametersMustRevalidateSetDirective",
    "RuleSetCacheControlRuleActionParametersMustRevalidateRemoveDirective",
    "RuleSetCacheControlRuleActionParametersMustUnderstand",
    "RuleSetCacheControlRuleActionParametersMustUnderstandSetDirective",
    "RuleSetCacheControlRuleActionParametersMustUnderstandRemoveDirective",
    "RuleSetCacheControlRuleActionParametersNoCache",
    "RuleSetCacheControlRuleActionParametersNoCacheSetDirective",
    "RuleSetCacheControlRuleActionParametersNoCacheRemoveDirective",
    "RuleSetCacheControlRuleActionParametersNoStore",
    "RuleSetCacheControlRuleActionParametersNoStoreSetDirective",
    "RuleSetCacheControlRuleActionParametersNoStoreRemoveDirective",
    "RuleSetCacheControlRuleActionParametersNoTransform",
    "RuleSetCacheControlRuleActionParametersNoTransformSetDirective",
    "RuleSetCacheControlRuleActionParametersNoTransformRemoveDirective",
    "RuleSetCacheControlRuleActionParametersPrivate",
    "RuleSetCacheControlRuleActionParametersPrivateSetDirective",
    "RuleSetCacheControlRuleActionParametersPrivateRemoveDirective",
    "RuleSetCacheControlRuleActionParametersProxyRevalidate",
    "RuleSetCacheControlRuleActionParametersProxyRevalidateSetDirective",
    "RuleSetCacheControlRuleActionParametersProxyRevalidateRemoveDirective",
    "RuleSetCacheControlRuleActionParametersPublic",
    "RuleSetCacheControlRuleActionParametersPublicSetDirective",
    "RuleSetCacheControlRuleActionParametersPublicRemoveDirective",
    "RuleSetCacheControlRuleActionParametersSMaxage",
    "RuleSetCacheControlRuleActionParametersSMaxageSetDirective",
    "RuleSetCacheControlRuleActionParametersSMaxageRemoveDirective",
    "RuleSetCacheControlRuleActionParametersStaleIfError",
    "RuleSetCacheControlRuleActionParametersStaleIfErrorSetDirective",
    "RuleSetCacheControlRuleActionParametersStaleIfErrorRemoveDirective",
    "RuleSetCacheControlRuleActionParametersStaleWhileRevalidate",
    "RuleSetCacheControlRuleActionParametersStaleWhileRevalidateSetDirective",
    "RuleSetCacheControlRuleActionParametersStaleWhileRevalidateRemoveDirective",
    "RuleSetCacheControlRuleExposedCredentialCheck",
    "RuleSetCacheControlRuleRatelimit",
    "RuleSetCacheSettingsRule",
    "RuleSetCacheTagsRule",
    "RuleSetCacheTagsRuleActionParameters",
    "RuleSetCacheTagsRuleActionParametersAddCacheTagsValues",
    "RuleSetCacheTagsRuleActionParametersAddCacheTagsExpression",
    "RuleSetCacheTagsRuleActionParametersRemoveCacheTagsValues",
    "RuleSetCacheTagsRuleActionParametersRemoveCacheTagsExpression",
    "RuleSetCacheTagsRuleActionParametersSetCacheTagsValues",
    "RuleSetCacheTagsRuleActionParametersSetCacheTagsExpression",
    "RuleSetCacheTagsRuleExposedCredentialCheck",
    "RuleSetCacheTagsRuleRatelimit",
    "RuleSetConfigurationRule",
    "RuleSkipRule",
    "RuleTransformResponseHTMLRule",
    "RuleTransformResponseHTMLRuleActionParameters",
    "RuleTransformResponseHTMLRuleExposedCredentialCheck",
    "RuleTransformResponseHTMLRuleRatelimit",
]


class RuleBlockRule(BlockRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleChallengeRuleExposedCredentialCheck(BaseModel):
    """Configuration for exposed credential checking."""

    password_expression: str
    """An expression that selects the password used in the credentials check."""

    username_expression: str
    """An expression that selects the user ID used in the credentials check."""


class RuleChallengeRuleRatelimit(BaseModel):
    """An object configuring the rule's rate limit behavior."""

    characteristics: List[str]
    """
    Characteristics of the request on which the rate limit counter will be
    incremented.
    """

    period: int
    """Period in seconds over which the counter is being incremented."""

    counting_expression: Optional[str] = None
    """An expression that defines when the rate limit counter should be incremented.

    It defaults to the same as the rule's expression.
    """

    mitigation_timeout: Optional[int] = None
    """
    Period of time in seconds after which the action will be disabled following its
    first execution.
    """

    requests_per_period: Optional[int] = None
    """
    The threshold of requests per period after which the action will be executed for
    the first time.
    """

    requests_to_origin: Optional[bool] = None
    """Whether counting is only performed when an origin is reached."""

    score_per_period: Optional[int] = None
    """
    The score threshold per period for which the action will be executed the first
    time.
    """

    score_response_header_name: Optional[str] = None
    """
    A response header name provided by the origin, which contains the score to
    increment rate limit counter with.
    """


class RuleChallengeRule(BaseModel):
    id: str
    """The unique ID of the rule."""

    action: Literal["challenge"]
    """The action to perform when the rule matches."""

    enabled: bool
    """Whether the rule should be executed."""

    expression: str
    """The expression defining which traffic will match the rule."""

    last_updated: datetime
    """The timestamp of when the rule was last modified."""

    ref: str
    """The reference of the rule (the rule's ID by default)."""

    version: str
    """The version of the rule."""

    action_parameters: Optional[object] = None
    """The parameters configuring the rule's action."""

    categories: Optional[List[str]] = None
    """The categories of the rule."""

    description: Optional[str] = None
    """An informative description of the rule."""

    exposed_credential_check: Optional[RuleChallengeRuleExposedCredentialCheck] = None
    """Configuration for exposed credential checking."""

    logging: Optional[Logging] = None
    """An object configuring the rule's logging behavior."""

    ratelimit: Optional[RuleChallengeRuleRatelimit] = None
    """An object configuring the rule's rate limit behavior."""


class RuleResponseCompressionRule(CompressResponseRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleDDoSDynamicRule(DDoSDynamicRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleExecuteRule(ExecuteRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleForceConnectionCloseRule(ForceConnectionCloseRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleJavaScriptChallengeRuleExposedCredentialCheck(BaseModel):
    """Configuration for exposed credential checking."""

    password_expression: str
    """An expression that selects the password used in the credentials check."""

    username_expression: str
    """An expression that selects the user ID used in the credentials check."""


class RuleJavaScriptChallengeRuleRatelimit(BaseModel):
    """An object configuring the rule's rate limit behavior."""

    characteristics: List[str]
    """
    Characteristics of the request on which the rate limit counter will be
    incremented.
    """

    period: int
    """Period in seconds over which the counter is being incremented."""

    counting_expression: Optional[str] = None
    """An expression that defines when the rate limit counter should be incremented.

    It defaults to the same as the rule's expression.
    """

    mitigation_timeout: Optional[int] = None
    """
    Period of time in seconds after which the action will be disabled following its
    first execution.
    """

    requests_per_period: Optional[int] = None
    """
    The threshold of requests per period after which the action will be executed for
    the first time.
    """

    requests_to_origin: Optional[bool] = None
    """Whether counting is only performed when an origin is reached."""

    score_per_period: Optional[int] = None
    """
    The score threshold per period for which the action will be executed the first
    time.
    """

    score_response_header_name: Optional[str] = None
    """
    A response header name provided by the origin, which contains the score to
    increment rate limit counter with.
    """


class RuleJavaScriptChallengeRule(BaseModel):
    id: str
    """The unique ID of the rule."""

    action: Literal["js_challenge"]
    """The action to perform when the rule matches."""

    enabled: bool
    """Whether the rule should be executed."""

    expression: str
    """The expression defining which traffic will match the rule."""

    last_updated: datetime
    """The timestamp of when the rule was last modified."""

    ref: str
    """The reference of the rule (the rule's ID by default)."""

    version: str
    """The version of the rule."""

    action_parameters: Optional[object] = None
    """The parameters configuring the rule's action."""

    categories: Optional[List[str]] = None
    """The categories of the rule."""

    description: Optional[str] = None
    """An informative description of the rule."""

    exposed_credential_check: Optional[RuleJavaScriptChallengeRuleExposedCredentialCheck] = None
    """Configuration for exposed credential checking."""

    logging: Optional[Logging] = None
    """An object configuring the rule's logging behavior."""

    ratelimit: Optional[RuleJavaScriptChallengeRuleRatelimit] = None
    """An object configuring the rule's rate limit behavior."""


class RuleLogRule(LogRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleLogCustomFieldRule(LogCustomFieldRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleManagedChallengeRule(ManagedChallengeRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleRedirectRule(RedirectRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleRewriteRule(RewriteRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleRouteRule(RouteRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleScoreRule(ScoreRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleServeErrorRule(ServeErrorRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleSetCacheControlRuleActionParametersImmutableSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersImmutableRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersImmutable: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersImmutableSetDirective,
    RuleSetCacheControlRuleActionParametersImmutableRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersMaxAgeSetDirective(BaseModel):
    """Set the directive with a duration value in seconds."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    value: int
    """The duration value in seconds for the directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersMaxAgeRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersMaxAge: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersMaxAgeSetDirective,
    RuleSetCacheControlRuleActionParametersMaxAgeRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersMustRevalidateSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersMustRevalidateRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersMustRevalidate: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersMustRevalidateSetDirective,
    RuleSetCacheControlRuleActionParametersMustRevalidateRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersMustUnderstandSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersMustUnderstandRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersMustUnderstand: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersMustUnderstandSetDirective,
    RuleSetCacheControlRuleActionParametersMustUnderstandRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersNoCacheSetDirective(BaseModel):
    """Set the directive with optional qualifiers."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""

    qualifiers: Optional[List[str]] = None
    """
    Optional list of header names to qualify the directive (e.g., for "private" or
    "no-cache" directives).
    """


class RuleSetCacheControlRuleActionParametersNoCacheRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersNoCache: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersNoCacheSetDirective,
    RuleSetCacheControlRuleActionParametersNoCacheRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersNoStoreSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersNoStoreRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersNoStore: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersNoStoreSetDirective,
    RuleSetCacheControlRuleActionParametersNoStoreRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersNoTransformSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersNoTransformRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersNoTransform: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersNoTransformSetDirective,
    RuleSetCacheControlRuleActionParametersNoTransformRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersPrivateSetDirective(BaseModel):
    """Set the directive with optional qualifiers."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""

    qualifiers: Optional[List[str]] = None
    """
    Optional list of header names to qualify the directive (e.g., for "private" or
    "no-cache" directives).
    """


class RuleSetCacheControlRuleActionParametersPrivateRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersPrivate: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersPrivateSetDirective,
    RuleSetCacheControlRuleActionParametersPrivateRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersProxyRevalidateSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersProxyRevalidateRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersProxyRevalidate: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersProxyRevalidateSetDirective,
    RuleSetCacheControlRuleActionParametersProxyRevalidateRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersPublicSetDirective(BaseModel):
    """Set the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersPublicRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersPublic: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersPublicSetDirective,
    RuleSetCacheControlRuleActionParametersPublicRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersSMaxageSetDirective(BaseModel):
    """Set the directive with a duration value in seconds."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    value: int
    """The duration value in seconds for the directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersSMaxageRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersSMaxage: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersSMaxageSetDirective,
    RuleSetCacheControlRuleActionParametersSMaxageRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersStaleIfErrorSetDirective(BaseModel):
    """Set the directive with a duration value in seconds."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    value: int
    """The duration value in seconds for the directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersStaleIfErrorRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersStaleIfError: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersStaleIfErrorSetDirective,
    RuleSetCacheControlRuleActionParametersStaleIfErrorRemoveDirective,
]


class RuleSetCacheControlRuleActionParametersStaleWhileRevalidateSetDirective(BaseModel):
    """Set the directive with a duration value in seconds."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    value: int
    """The duration value in seconds for the directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


class RuleSetCacheControlRuleActionParametersStaleWhileRevalidateRemoveDirective(BaseModel):
    """Remove the directive."""

    operation: Literal["set", "remove"]
    """The operation to perform on the cache-control directive."""

    cloudflare_only: Optional[bool] = None
    """Whether the directive should only be applied to the Cloudflare CDN cache."""


RuleSetCacheControlRuleActionParametersStaleWhileRevalidate: TypeAlias = Union[
    RuleSetCacheControlRuleActionParametersStaleWhileRevalidateSetDirective,
    RuleSetCacheControlRuleActionParametersStaleWhileRevalidateRemoveDirective,
]


class RuleSetCacheControlRuleActionParameters(BaseModel):
    """The parameters configuring the rule's action."""

    immutable: Optional[RuleSetCacheControlRuleActionParametersImmutable] = None
    """A cache-control directive configuration."""

    max_age: Optional[RuleSetCacheControlRuleActionParametersMaxAge] = FieldInfo(alias="max-age", default=None)
    """
    A cache-control directive configuration that accepts a duration value in
    seconds.
    """

    must_revalidate: Optional[RuleSetCacheControlRuleActionParametersMustRevalidate] = FieldInfo(
        alias="must-revalidate", default=None
    )
    """A cache-control directive configuration."""

    must_understand: Optional[RuleSetCacheControlRuleActionParametersMustUnderstand] = FieldInfo(
        alias="must-understand", default=None
    )
    """A cache-control directive configuration."""

    no_cache: Optional[RuleSetCacheControlRuleActionParametersNoCache] = FieldInfo(alias="no-cache", default=None)
    """
    A cache-control directive configuration that accepts optional qualifiers (header
    names).
    """

    no_store: Optional[RuleSetCacheControlRuleActionParametersNoStore] = FieldInfo(alias="no-store", default=None)
    """A cache-control directive configuration."""

    no_transform: Optional[RuleSetCacheControlRuleActionParametersNoTransform] = FieldInfo(
        alias="no-transform", default=None
    )
    """A cache-control directive configuration."""

    private: Optional[RuleSetCacheControlRuleActionParametersPrivate] = None
    """
    A cache-control directive configuration that accepts optional qualifiers (header
    names).
    """

    proxy_revalidate: Optional[RuleSetCacheControlRuleActionParametersProxyRevalidate] = FieldInfo(
        alias="proxy-revalidate", default=None
    )
    """A cache-control directive configuration."""

    public: Optional[RuleSetCacheControlRuleActionParametersPublic] = None
    """A cache-control directive configuration."""

    s_maxage: Optional[RuleSetCacheControlRuleActionParametersSMaxage] = FieldInfo(alias="s-maxage", default=None)
    """
    A cache-control directive configuration that accepts a duration value in
    seconds.
    """

    stale_if_error: Optional[RuleSetCacheControlRuleActionParametersStaleIfError] = FieldInfo(
        alias="stale-if-error", default=None
    )
    """
    A cache-control directive configuration that accepts a duration value in
    seconds.
    """

    stale_while_revalidate: Optional[RuleSetCacheControlRuleActionParametersStaleWhileRevalidate] = FieldInfo(
        alias="stale-while-revalidate", default=None
    )
    """
    A cache-control directive configuration that accepts a duration value in
    seconds.
    """


class RuleSetCacheControlRuleExposedCredentialCheck(BaseModel):
    """Configuration for exposed credential checking."""

    password_expression: str
    """An expression that selects the password used in the credentials check."""

    username_expression: str
    """An expression that selects the user ID used in the credentials check."""


class RuleSetCacheControlRuleRatelimit(BaseModel):
    """An object configuring the rule's rate limit behavior."""

    characteristics: List[str]
    """
    Characteristics of the request on which the rate limit counter will be
    incremented.
    """

    period: int
    """Period in seconds over which the counter is being incremented."""

    counting_expression: Optional[str] = None
    """An expression that defines when the rate limit counter should be incremented.

    It defaults to the same as the rule's expression.
    """

    mitigation_timeout: Optional[int] = None
    """
    Period of time in seconds after which the action will be disabled following its
    first execution.
    """

    requests_per_period: Optional[int] = None
    """
    The threshold of requests per period after which the action will be executed for
    the first time.
    """

    requests_to_origin: Optional[bool] = None
    """Whether counting is only performed when an origin is reached."""

    score_per_period: Optional[int] = None
    """
    The score threshold per period for which the action will be executed the first
    time.
    """

    score_response_header_name: Optional[str] = None
    """
    A response header name provided by the origin, which contains the score to
    increment rate limit counter with.
    """


class RuleSetCacheControlRule(BaseModel):
    id: str
    """The unique ID of the rule."""

    action: Literal["set_cache_control"]
    """The action to perform when the rule matches."""

    enabled: bool

    expression: str
    """The expression defining which traffic will match the rule."""

    last_updated: datetime
    """The timestamp of when the rule was last modified."""

    ref: str
    """The reference of the rule (the rule's ID by default)."""

    version: str
    """The version of the rule."""

    action_parameters: Optional[RuleSetCacheControlRuleActionParameters] = None
    """The parameters configuring the rule's action."""

    categories: Optional[List[str]] = None
    """The categories of the rule."""

    description: Optional[str] = None
    """An informative description of the rule."""

    exposed_credential_check: Optional[RuleSetCacheControlRuleExposedCredentialCheck] = None
    """Configuration for exposed credential checking."""

    logging: Optional[Logging] = None
    """An object configuring the rule's logging behavior."""

    ratelimit: Optional[RuleSetCacheControlRuleRatelimit] = None
    """An object configuring the rule's rate limit behavior."""


class RuleSetCacheSettingsRule(SetCacheSettingsRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleSetCacheTagsRuleActionParametersAddCacheTagsValues(BaseModel):
    """Add cache tags using a list of values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""

    values: List[str]
    """A list of cache tag values."""


class RuleSetCacheTagsRuleActionParametersAddCacheTagsExpression(BaseModel):
    """Add cache tags using an expression."""

    expression: str
    """An expression that evaluates to an array of cache tag values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""


class RuleSetCacheTagsRuleActionParametersRemoveCacheTagsValues(BaseModel):
    """Remove cache tags using a list of values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""

    values: List[str]
    """A list of cache tag values."""


class RuleSetCacheTagsRuleActionParametersRemoveCacheTagsExpression(BaseModel):
    """Remove cache tags using an expression."""

    expression: str
    """An expression that evaluates to an array of cache tag values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""


class RuleSetCacheTagsRuleActionParametersSetCacheTagsValues(BaseModel):
    """Set cache tags using a list of values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""

    values: List[str]
    """A list of cache tag values."""


class RuleSetCacheTagsRuleActionParametersSetCacheTagsExpression(BaseModel):
    """Set cache tags using an expression."""

    expression: str
    """An expression that evaluates to an array of cache tag values."""

    operation: Literal["add", "remove", "set"]
    """The operation to perform on the cache tags."""


RuleSetCacheTagsRuleActionParameters: TypeAlias = Union[
    RuleSetCacheTagsRuleActionParametersAddCacheTagsValues,
    RuleSetCacheTagsRuleActionParametersAddCacheTagsExpression,
    RuleSetCacheTagsRuleActionParametersRemoveCacheTagsValues,
    RuleSetCacheTagsRuleActionParametersRemoveCacheTagsExpression,
    RuleSetCacheTagsRuleActionParametersSetCacheTagsValues,
    RuleSetCacheTagsRuleActionParametersSetCacheTagsExpression,
]


class RuleSetCacheTagsRuleExposedCredentialCheck(BaseModel):
    """Configuration for exposed credential checking."""

    password_expression: str
    """An expression that selects the password used in the credentials check."""

    username_expression: str
    """An expression that selects the user ID used in the credentials check."""


class RuleSetCacheTagsRuleRatelimit(BaseModel):
    """An object configuring the rule's rate limit behavior."""

    characteristics: List[str]
    """
    Characteristics of the request on which the rate limit counter will be
    incremented.
    """

    period: int
    """Period in seconds over which the counter is being incremented."""

    counting_expression: Optional[str] = None
    """An expression that defines when the rate limit counter should be incremented.

    It defaults to the same as the rule's expression.
    """

    mitigation_timeout: Optional[int] = None
    """
    Period of time in seconds after which the action will be disabled following its
    first execution.
    """

    requests_per_period: Optional[int] = None
    """
    The threshold of requests per period after which the action will be executed for
    the first time.
    """

    requests_to_origin: Optional[bool] = None
    """Whether counting is only performed when an origin is reached."""

    score_per_period: Optional[int] = None
    """
    The score threshold per period for which the action will be executed the first
    time.
    """

    score_response_header_name: Optional[str] = None
    """
    A response header name provided by the origin, which contains the score to
    increment rate limit counter with.
    """


class RuleSetCacheTagsRule(BaseModel):
    id: str
    """The unique ID of the rule."""

    action: Literal["set_cache_tags"]
    """The action to perform when the rule matches."""

    enabled: bool

    expression: str
    """The expression defining which traffic will match the rule."""

    last_updated: datetime
    """The timestamp of when the rule was last modified."""

    ref: str
    """The reference of the rule (the rule's ID by default)."""

    version: str
    """The version of the rule."""

    action_parameters: Optional[RuleSetCacheTagsRuleActionParameters] = None
    """The parameters configuring the rule's action."""

    categories: Optional[List[str]] = None
    """The categories of the rule."""

    description: Optional[str] = None
    """An informative description of the rule."""

    exposed_credential_check: Optional[RuleSetCacheTagsRuleExposedCredentialCheck] = None
    """Configuration for exposed credential checking."""

    logging: Optional[Logging] = None
    """An object configuring the rule's logging behavior."""

    ratelimit: Optional[RuleSetCacheTagsRuleRatelimit] = None
    """An object configuring the rule's rate limit behavior."""


class RuleSetConfigurationRule(SetConfigRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleSkipRule(SkipRule):
    id: str  # type: ignore

    action: str  # type: ignore

    enabled: bool  # type: ignore

    expression: str  # type: ignore

    ref: str  # type: ignore


class RuleTransformResponseHTMLRuleActionParameters(BaseModel):
    """The parameters configuring the rule's action."""

    link_maze: object
    """Enables the link maze transformation on the response."""


class RuleTransformResponseHTMLRuleExposedCredentialCheck(BaseModel):
    """Configuration for exposed credential checking."""

    password_expression: str
    """An expression that selects the password used in the credentials check."""

    username_expression: str
    """An expression that selects the user ID used in the credentials check."""


class RuleTransformResponseHTMLRuleRatelimit(BaseModel):
    """An object configuring the rule's rate limit behavior."""

    characteristics: List[str]
    """
    Characteristics of the request on which the rate limit counter will be
    incremented.
    """

    period: int
    """Period in seconds over which the counter is being incremented."""

    counting_expression: Optional[str] = None
    """An expression that defines when the rate limit counter should be incremented.

    It defaults to the same as the rule's expression.
    """

    mitigation_timeout: Optional[int] = None
    """
    Period of time in seconds after which the action will be disabled following its
    first execution.
    """

    requests_per_period: Optional[int] = None
    """
    The threshold of requests per period after which the action will be executed for
    the first time.
    """

    requests_to_origin: Optional[bool] = None
    """Whether counting is only performed when an origin is reached."""

    score_per_period: Optional[int] = None
    """
    The score threshold per period for which the action will be executed the first
    time.
    """

    score_response_header_name: Optional[str] = None
    """
    A response header name provided by the origin, which contains the score to
    increment rate limit counter with.
    """


class RuleTransformResponseHTMLRule(BaseModel):
    id: str
    """The unique ID of the rule."""

    action: Literal["transform_response_html"]
    """The action to perform when the rule matches."""

    enabled: bool

    expression: str
    """The expression defining which traffic will match the rule."""

    last_updated: datetime
    """The timestamp of when the rule was last modified."""

    ref: str
    """The reference of the rule (the rule's ID by default)."""

    version: str
    """The version of the rule."""

    action_parameters: Optional[RuleTransformResponseHTMLRuleActionParameters] = None
    """The parameters configuring the rule's action."""

    categories: Optional[List[str]] = None
    """The categories of the rule."""

    description: Optional[str] = None
    """An informative description of the rule."""

    exposed_credential_check: Optional[RuleTransformResponseHTMLRuleExposedCredentialCheck] = None
    """Configuration for exposed credential checking."""

    logging: Optional[Logging] = None
    """An object configuring the rule's logging behavior."""

    ratelimit: Optional[RuleTransformResponseHTMLRuleRatelimit] = None
    """An object configuring the rule's rate limit behavior."""


Rule: TypeAlias = Union[
    RuleBlockRule,
    RuleChallengeRule,
    RuleResponseCompressionRule,
    RuleDDoSDynamicRule,
    RuleExecuteRule,
    RuleForceConnectionCloseRule,
    RuleJavaScriptChallengeRule,
    RuleLogRule,
    RuleLogCustomFieldRule,
    RuleManagedChallengeRule,
    RuleRedirectRule,
    RuleRewriteRule,
    RuleRouteRule,
    RuleScoreRule,
    RuleServeErrorRule,
    RuleSetCacheControlRule,
    RuleSetCacheSettingsRule,
    RuleSetCacheTagsRule,
    RuleSetConfigurationRule,
    RuleSkipRule,
    RuleTransformResponseHTMLRule,
]


class VersionGetResponse(BaseModel):
    """A ruleset object."""

    id: str
    """The unique ID of the ruleset."""

    kind: Kind
    """The kind of the ruleset."""

    last_updated: datetime
    """The timestamp of when the ruleset was last modified."""

    name: str
    """The human-readable name of the ruleset."""

    phase: Phase
    """The phase of the ruleset."""

    rules: List[Rule]
    """The list of rules in the ruleset."""

    version: str
    """The version of the ruleset."""

    description: Optional[str] = None
    """An informative description of the ruleset."""
