"""State module for managing Amazon WAF v2 web ACLs."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    scope: str,
    default_action: make_dataclass(
        """The action to perform if none of the ``Rules`` contained in the ``WebACL`` match."""
        "DefaultAction",
        [
            (
                "Block",
                make_dataclass(
                    """Specifies that WAF should block requests by default."""
                    "BlockAction",
                    [
                        (
                            "CustomResponse",
                            make_dataclass(
                                """Defines a custom response for the web request."""
                                "CustomResponse",
                                [
                                    ("ResponseCode", int),
                                    ("CustomResponseBodyKey", str, field(default=None)),
                                    (
                                        "ResponseHeaders",
                                        List[
                                            make_dataclass(
                                                """A custom header for custom request and response handling."""
                                                "CustomHTTPHeader",
                                                [("Name", str), ("Value", str)],
                                            )
                                        ],
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "Allow",
                make_dataclass(
                    """Specifies that WAF should allow requests by default."""
                    "AllowAction",
                    [
                        (
                            "CustomRequestHandling",
                            make_dataclass(
                                """Defines custom handling for the web request."""
                                "CustomRequestHandling",
                                [
                                    (
                                        "InsertHeaders",
                                        List[
                                            make_dataclass(
                                                """A custom header for custom request and response handling."""
                                                "CustomHTTPHeader",
                                                [("Name", str), ("Value", str)],
                                            )
                                        ],
                                        field(default=None),
                                    )
                                ],
                            ),
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
        ],
    ),
    visibility_config: make_dataclass(
        """Defines and enables Amazon CloudWatch metrics and web request sample collection."""
        "VisibilityConfig",
        [
            ("SampledRequestsEnabled", bool),
            ("CloudWatchMetricsEnabled", bool),
            ("MetricName", str),
        ],
    ),
    resource_id: str = None,
    description: str = None,
    rules: List[
        make_dataclass(
            "Rule",
            [
                ("Name", str),
                ("Priority", int),
                (
                    "Statement",
                    make_dataclass(
                        "Statement",
                        [
                            (
                                "ByteMatchStatement",
                                make_dataclass(
                                    "ByteMatchStatement",
                                    [
                                        ("SearchString", bytes),
                                        (
                                            "FieldToMatch",
                                            make_dataclass(
                                                "FieldToMatch",
                                                [
                                                    (
                                                        "SingleHeader",
                                                        make_dataclass(
                                                            "SingleHeader",
                                                            [("Name", str)],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "SingleQueryArgument",
                                                        make_dataclass(
                                                            "SingleQueryArgument",
                                                            [("Name", str)],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AllQueryArguments",
                                                        Dict,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "UriPath",
                                                        Dict,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "QueryString",
                                                        Dict,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Body",
                                                        make_dataclass(
                                                            "Body",
                                                            [
                                                                (
                                                                    "OversizeHandling",
                                                                    str,
                                                                    field(default=None),
                                                                )
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Method",
                                                        Dict,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "JsonBody",
                                                        make_dataclass(
                                                            "JsonBody",
                                                            [
                                                                (
                                                                    "MatchPattern",
                                                                    make_dataclass(
                                                                        "JsonMatchPattern",
                                                                        [
                                                                            (
                                                                                "All",
                                                                                Dict,
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                            (
                                                                                "IncludedPaths",
                                                                                List[
                                                                                    str
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ),
                                                                ("MatchScope", str),
                                                                (
                                                                    "InvalidFallbackBehavior",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "OversizeHandling",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Headers",
                                                        make_dataclass(
                                                            "Headers",
                                                            [
                                                                (
                                                                    "MatchPattern",
                                                                    make_dataclass(
                                                                        "HeaderMatchPattern",
                                                                        [
                                                                            (
                                                                                "All",
                                                                                Dict,
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                            (
                                                                                "IncludedHeaders",
                                                                                List[
                                                                                    str
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                            (
                                                                                "ExcludedHeaders",
                                                                                List[
                                                                                    str
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ),
                                                                ("MatchScope", str),
                                                                (
                                                                    "OversizeHandling",
                                                                    str,
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "Cookies",
                                                        make_dataclass(
                                                            "Cookies",
                                                            [
                                                                (
                                                                    "MatchPattern",
                                                                    make_dataclass(
                                                                        "CookieMatchPattern",
                                                                        [
                                                                            (
                                                                                "All",
                                                                                Dict,
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                            (
                                                                                "IncludedCookies",
                                                                                List[
                                                                                    str
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                            (
                                                                                "ExcludedCookies",
                                                                                List[
                                                                                    str
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ),
                                                                ("MatchScope", str),
                                                                (
                                                                    "OversizeHandling",
                                                                    str,
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                        ),
                                        (
                                            "TextTransformations",
                                            List[
                                                make_dataclass(
                                                    "TextTransformation",
                                                    [("Priority", int), ("Type", str)],
                                                )
                                            ],
                                        ),
                                        ("PositionalConstraint", str),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "SqliMatchStatement",
                                make_dataclass(
                                    "SqliMatchStatement",
                                    [
                                        ("FieldToMatch", "FieldToMatch"),
                                        (
                                            "TextTransformations",
                                            List["TextTransformation"],
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "XssMatchStatement",
                                make_dataclass(
                                    "XssMatchStatement",
                                    [
                                        ("FieldToMatch", "FieldToMatch"),
                                        (
                                            "TextTransformations",
                                            List["TextTransformation"],
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "SizeConstraintStatement",
                                make_dataclass(
                                    "SizeConstraintStatement",
                                    [
                                        ("FieldToMatch", "FieldToMatch"),
                                        ("ComparisonOperator", str),
                                        ("Size", int),
                                        (
                                            "TextTransformations",
                                            List["TextTransformation"],
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "GeoMatchStatement",
                                make_dataclass(
                                    "GeoMatchStatement",
                                    [
                                        (
                                            "CountryCodes",
                                            List[str],
                                            field(default=None),
                                        ),
                                        (
                                            "ForwardedIPConfig",
                                            make_dataclass(
                                                "ForwardedIPConfig",
                                                [
                                                    ("HeaderName", str),
                                                    ("FallbackBehavior", str),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "RuleGroupReferenceStatement",
                                make_dataclass(
                                    "RuleGroupReferenceStatement",
                                    [
                                        ("ARN", str),
                                        (
                                            "ExcludedRules",
                                            List[
                                                make_dataclass(
                                                    "ExcludedRule", [("Name", str)]
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "IPSetReferenceStatement",
                                make_dataclass(
                                    "IPSetReferenceStatement",
                                    [
                                        ("ARN", str),
                                        (
                                            "IPSetForwardedIPConfig",
                                            make_dataclass(
                                                "IPSetForwardedIPConfig",
                                                [
                                                    ("HeaderName", str),
                                                    ("FallbackBehavior", str),
                                                    ("Position", str),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "RegexPatternSetReferenceStatement",
                                make_dataclass(
                                    "RegexPatternSetReferenceStatement",
                                    [
                                        ("ARN", str),
                                        ("FieldToMatch", "FieldToMatch"),
                                        (
                                            "TextTransformations",
                                            List["TextTransformation"],
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "RateBasedStatement",
                                make_dataclass(
                                    "RateBasedStatement",
                                    [
                                        ("Limit", int),
                                        ("AggregateKeyType", str),
                                        (
                                            "ScopeDownStatement",
                                            "Statement",
                                            field(default=None),
                                        ),
                                        (
                                            "ForwardedIPConfig",
                                            "ForwardedIPConfig",
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "AndStatement",
                                make_dataclass(
                                    "AndStatement",
                                    [
                                        (
                                            "Statements",
                                            List[
                                                make_dataclass(
                                                    "Statement",
                                                    [
                                                        (
                                                            "ByteMatchStatement",
                                                            "ByteMatchStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "SqliMatchStatement",
                                                            "SqliMatchStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "XssMatchStatement",
                                                            "XssMatchStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "SizeConstraintStatement",
                                                            "SizeConstraintStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "GeoMatchStatement",
                                                            "GeoMatchStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "RuleGroupReferenceStatement",
                                                            "RuleGroupReferenceStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "IPSetReferenceStatement",
                                                            "IPSetReferenceStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "RegexPatternSetReferenceStatement",
                                                            "RegexPatternSetReferenceStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "RateBasedStatement",
                                                            "RateBasedStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "AndStatement",
                                                            "AndStatement",
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "OrStatement",
                                                            make_dataclass(
                                                                "OrStatement",
                                                                [
                                                                    (
                                                                        "Statements",
                                                                        List[
                                                                            "Statement"
                                                                        ],
                                                                    )
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "NotStatement",
                                                            make_dataclass(
                                                                "NotStatement",
                                                                [
                                                                    (
                                                                        "Statement",
                                                                        "Statement",
                                                                    )
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "ManagedRuleGroupStatement",
                                                            make_dataclass(
                                                                "ManagedRuleGroupStatement",
                                                                [
                                                                    ("VendorName", str),
                                                                    ("Name", str),
                                                                    (
                                                                        "Version",
                                                                        str,
                                                                        field(
                                                                            default=None
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "ExcludedRules",
                                                                        List[
                                                                            "ExcludedRule"
                                                                        ],
                                                                        field(
                                                                            default=None
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "ScopeDownStatement",
                                                                        "Statement",
                                                                        field(
                                                                            default=None
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "ManagedRuleGroupConfigs",
                                                                        List[
                                                                            make_dataclass(
                                                                                "ManagedRuleGroupConfig",
                                                                                [
                                                                                    (
                                                                                        "LoginPath",
                                                                                        str,
                                                                                        field(
                                                                                            default=None
                                                                                        ),
                                                                                    ),
                                                                                    (
                                                                                        "PayloadType",
                                                                                        str,
                                                                                        field(
                                                                                            default=None
                                                                                        ),
                                                                                    ),
                                                                                    (
                                                                                        "UsernameField",
                                                                                        make_dataclass(
                                                                                            "UsernameField",
                                                                                            [
                                                                                                (
                                                                                                    "Identifier",
                                                                                                    str,
                                                                                                )
                                                                                            ],
                                                                                        ),
                                                                                        field(
                                                                                            default=None
                                                                                        ),
                                                                                    ),
                                                                                    (
                                                                                        "PasswordField",
                                                                                        make_dataclass(
                                                                                            "PasswordField",
                                                                                            [
                                                                                                (
                                                                                                    "Identifier",
                                                                                                    str,
                                                                                                )
                                                                                            ],
                                                                                        ),
                                                                                        field(
                                                                                            default=None
                                                                                        ),
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                        field(
                                                                            default=None
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "LabelMatchStatement",
                                                            make_dataclass(
                                                                "LabelMatchStatement",
                                                                [
                                                                    ("Scope", str),
                                                                    ("Key", str),
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "RegexMatchStatement",
                                                            make_dataclass(
                                                                "RegexMatchStatement",
                                                                [
                                                                    (
                                                                        "RegexString",
                                                                        str,
                                                                    ),
                                                                    (
                                                                        "FieldToMatch",
                                                                        "FieldToMatch",
                                                                    ),
                                                                    (
                                                                        "TextTransformations",
                                                                        List[
                                                                            "TextTransformation"
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                    ],
                                                )
                                            ],
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("OrStatement", "OrStatement", field(default=None)),
                            ("NotStatement", "NotStatement", field(default=None)),
                            (
                                "ManagedRuleGroupStatement",
                                "ManagedRuleGroupStatement",
                                field(default=None),
                            ),
                            (
                                "LabelMatchStatement",
                                "LabelMatchStatement",
                                field(default=None),
                            ),
                            (
                                "RegexMatchStatement",
                                "RegexMatchStatement",
                                field(default=None),
                            ),
                        ],
                    ),
                ),
                (
                    "Action",
                    make_dataclass(
                        "RuleAction",
                        [
                            (
                                "Block",
                                make_dataclass(
                                    "BlockAction",
                                    [
                                        (
                                            "CustomResponse",
                                            make_dataclass(
                                                "CustomResponse",
                                                [
                                                    ("ResponseCode", int),
                                                    (
                                                        "CustomResponseBodyKey",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "ResponseHeaders",
                                                        List[
                                                            make_dataclass(
                                                                "CustomHTTPHeader",
                                                                [
                                                                    ("Name", str),
                                                                    ("Value", str),
                                                                ],
                                                            )
                                                        ],
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "Allow",
                                make_dataclass(
                                    "AllowAction",
                                    [
                                        (
                                            "CustomRequestHandling",
                                            make_dataclass(
                                                "CustomRequestHandling",
                                                [
                                                    (
                                                        "InsertHeaders",
                                                        List["CustomHTTPHeader"],
                                                    )
                                                ],
                                            ),
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "Count",
                                make_dataclass(
                                    "CountAction",
                                    [
                                        (
                                            "CustomRequestHandling",
                                            "CustomRequestHandling",
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "Captcha",
                                make_dataclass(
                                    "CaptchaAction",
                                    [
                                        (
                                            "CustomRequestHandling",
                                            "CustomRequestHandling",
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "OverrideAction",
                    make_dataclass(
                        "OverrideAction",
                        [
                            ("Count", "CountAction", field(default=None)),
                            ("none", Dict, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "VisibilityConfig",
                    make_dataclass(
                        "VisibilityConfig",
                        [
                            ("SampledRequestsEnabled", bool),
                            ("CloudWatchMetricsEnabled", bool),
                            ("MetricName", str),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "CaptchaConfig",
                    make_dataclass(
                        "CaptchaConfig",
                        [
                            (
                                "ImmunityTimeProperty",
                                make_dataclass(
                                    "ImmunityTimeProperty", [("ImmunityTime", int)]
                                ),
                                field(default=None),
                            )
                        ],
                    ),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    custom_response_bodies: dict = None,
    captcha_config: dict = None,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
):
    r"""Creates a WebACL per the specifications provided.

    A web ACL defines a collection of rules to use to inspect and control web requests.
    Each rule has an action defined (allow, block, or count) for requests that match the statement of the rule.
    In the web ACL, you assign a default action to take (allow, block) for any request that does not match any of the rules.
    The rules in a web ACL can be a combination of the types Rule , RuleGroup , and managed rule group.
    You can associate a web ACL with one or more Amazon Web Services resources to protect.
    The resources can be an Amazon CloudFront distribution, an Amazon API Gateway REST API, an Application Load Balancer,
    an AppSync GraphQL API, or an Amazon Cognito user pool.

    Args:
        name(str):
            The name of the web ACL. You cannot change the name of a web ACL after you create it.
        resource_id(str, Optional):
            The ID of the web ACL in Amazon Web Services.
        scope(str):
            Specifies whether this is for an Amazon CloudFront distribution (``CLOUDFRONT``) or for a regional application (``REGIONAL``).
        default_action(dict):
            The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

            * Block (*dict, Optional*):
                Specifies that WAF should block requests by default.

                * CustomResponse (*dict, Optional*):
                    Defines a custom response for the web request.

                    * ResponseCode (*int*):
                        The HTTP status code to return to the client.
                    * CustomResponseBodyKey (*str, Optional*):
                        References the response body that you want WAF to return to the web request client. You can
                        define a custom response for a rule action or a default web ACL action that is set to block. To
                        do this, you first define the response body key and value in the ``CustomResponseBodies`` setting
                        for the WebACL or RuleGroup where you want to use it. Then, in the rule action or web ACL
                        default action ``BlockAction`` setting, you reference the response body using this key.
                    * ResponseHeaders (*list, Optional*):
                        The HTTP headers to use in the response. Duplicate header names are not allowed.

                        * Name (*str*):
                            The name of the custom header. For custom request header insertion, when WAF inserts the header
                            into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                            are already in the request. For example, for the header name ``sample``, WAF inserts the header
                            ``x-amzn-waf-sample``.
                        * Value (*str*):
                            The value of the custom header.

            * Allow (*dict, Optional*):
                Specifies that WAF should allow requests by default.

                * CustomRequestHandling (*dict, Optional*):
                    Defines custom handling for the web request.

                    * InsertHeaders (*list*):
                        The HTTP headers to insert into the request. Duplicate header names are not allowed.

                        * Name (*str*):
                            The name of the custom header. For custom request header insertion, when WAF inserts the header
                            into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                            are already in the request. For example, for the header name ``sample``, WAF inserts the header
                            ``x-amzn-waf-sample``.
                        * Value (*str*):
                            The value of the custom header.

        visibility_config(dict):
            Defines and enables Amazon CloudWatch metrics and web request sample collection.

            * SampledRequestsEnabled (*bool*):
                A boolean indicating whether WAF should store a sampling of the web requests that match the
                rules. You can view the sampled requests through the WAF console.
            * CloudWatchMetricsEnabled (*bool*):
                A boolean indicating whether the associated resource sends metrics to Amazon CloudWatch. For the
                list of available metrics, see WAF Metrics.
            * MetricName (*str*):
                A name of the Amazon CloudWatch metric. The name can contain only the characters: ``A-Z``, ``a-z``, ``0-9``,
                ``-`` (hyphen), and ``_`` (underscore). The name can be from one to 128 characters long. It can't
                contain whitespace or metric names reserved for WAF, for example ``All`` and ``Default_Action``.

        description(str, Optional):
            A description of the web ACL that helps with identification.
        rules(list, Optional):
            The Rule statements used to identify the web requests that you want to allow, block, or count.
            Each rule includes one top-level statement that WAF uses to identify matching web requests, and
            parameters that govern how WAF handles them.

            * Name (*str*):
                The name of the rule. You can't change the name of a ``Rule`` after you create it.
            * Priority (*int*):
                If you define more than one `Rule` in a WebACL, WAF evaluates each request against the Rules in
                order based on the value of Priority. WAF processes rules with lower priority first. The
                priorities don't need to be consecutive, but they must all be different.

                * Statement (*dict*):
                    The WAF processing statement for the rule, for example ``ByteMatchStatement`` or ``SizeConstraintStatement``.

                    * ByteMatchStatement (*dict, Optional*):
                        A rule statement that defines a string match search for WAF to apply to web requests. The byte
                        match statement provides the bytes to search for, the location in requests that you want WAF to
                        search, and other settings. The bytes to search for are typically a string that corresponds with
                        ASCII characters. In the WAF console and the developer guide, this is refered to as a string
                        match statement.

                        * SearchString (*byte*):
                            A string value that you want WAF to search for. WAF searches only in the part of web requests that you
                            designate for inspection in ``FieldToMatch``. The maximum length of the value is 50 bytes.

                            Valid values depend on the component that you specify for inspection in ``FieldToMatch``:

                            * ``Method``:
                                The HTTP method that you want WAF to search for. This indicates the type of operation specified in the request.
                            * ``UriPath``:
                                The value that you want WAF to search for in the URI path, for example, ``/images/daily-ad.jpg``.

                            If ``SearchString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.
                        * FieldToMatch (*dict*):
                            The part of the web request that you want WAF to inspect.

                            * SingleHeader (*dict, Optional*):
                                Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                                ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                                Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                                * Name (*str*):
                                    The name of the query header to inspect.
                            * SingleQueryArgument (*dict, Optional*):
                                Inspect a single query argument. Provide the name of the query argument to inspect, such as
                                ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                                Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                                * Name (*str*):
                                    The name of the query argument to inspect.
                            * AllQueryArguments (*dict, Optional*):
                                Inspect all query arguments.
                            * UriPath (*dict, Optional*):
                                Inspect the request URI path. This is the part of the web request that identifies a resource,
                                for example, ``/images/daily-ad.jpg``.
                            * QueryString (*dict, Optional*):
                                Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                            * Body (*dict, Optional*):
                                Inspect the request body as plain text. The request body immediately follows the request
                                headers. This is the part of a request that contains any additional data that you want to send
                                to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                                (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                                service. For information about how to handle oversized request bodies, see the Body object
                                configuration.

                                * OversizeHandling (*str, Optional*):
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Method (*dict, Optional*):
                                Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                            * JsonBody (*dict, Optional*):
                                Inspect the request body as JSON. The request body immediately follows the request headers. This
                                is the part of a request that contains any additional data that you want to send to your web
                                server as the HTTP request body, such as data from a form.

                                Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                                For information about how to handle oversized request bodies, see the JsonBody object configuration.

                                * MatchPattern (*dict*):
                                    The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                    * All (*dict, Optional*):
                                        Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                        setting or the ``IncludedPaths`` setting, but not both.
                                    * IncludedPaths (*dict, Optional*):
                                        Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                        paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                        For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                        JavaScript Object Notation (JSON) Pointer.
                                        You must specify either this setting or the ``All`` setting, but not both.

                                        .. note::
                                            Don't use this option to include all paths. Instead, use the ``All`` setting.
                                * MatchScope (*str*):
                                    The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                    against keys and values.
                                * InvalidFallbackBehavior (*str, Optional*):
                                    What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                    * ``EVALUATE_AS_STRING``:
                                        Inspect the body as plain text. WAF applies the text transformations and
                                        inspection criteria that you defined for the JSON inspection to the body text string.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE``:
                                        Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Headers (*dict, Optional*):
                                Inspect the request headers. You must configure scope and pattern matching filters in the
                                Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize header content in the Headers object. WAF applies the pattern matching filters to
                                the headers that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of headers to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                    * All (*dict, Optional*):
                                        Inspect all headers.
                                    * IncludedHeaders (*list, Optional*):
                                        Inspect only the headers that have a key that matches one of the strings specified here.
                                    * ExcludedHeaders (*list, Optional*):
                                        Inspect only the headers whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                    support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                    200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                    of header contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the headers normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                            * Cookies (*dict, Optional*):
                                Inspect the request cookies. You must configure scope and pattern matching filters in the
                                ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                                the cookies that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of cookies to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                    * All (*dict, Optional*):
                                        Inspect all cookies.
                                    * IncludedCookies (*list, Optional*):
                                        Inspect only the cookies that have a key that matches one of the strings specified here.
                                    * ExcludedCookies (*list, Optional*):
                                        Inspect only the cookies whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                    inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                    The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the cookies normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                        * TextTransformations (*list*):
                            Text transformations eliminate some of the unusual formatting that attackers use in web requests
                            in an effort to bypass detection. If you specify one or more transformations in a rule
                            statement, WAF performs all transformations on the content of the request component identified
                            by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                            match.

                            * Priority (*int*):
                                Sets the relative processing order for multiple transformations that are defined for a rule
                                statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                                the transformed content. The priorities don't need to be consecutive, but they must all be
                                different.
                            * Type (*str*):
                                You can specify the following transformation types:

                                * ``BASE64_DECODE``:
                                    Decode a Base64-encoded string.
                                * ``BASE64_DECODE_EXT``:
                                    Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                                * ``CMD_LINE``:
                                    Command-line transformations. These are helpful in reducing effectiveness of
                                    attackers who inject an operating system command-line command and use unusual formatting to
                                    disguise some or all of the command.

                                    * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                    * Delete spaces before the following characters: ``/`` ``(``
                                    * Replace the following characters with a space: ``,`` ``;``
                                    * Replace multiple spaces with one space
                                    * Convert uppercase letters (A-Z) to lowercase (a-z)
                                * ``COMPRESS_WHITE_SPACE``:
                                    Replace these characters with a space character (decimal 32):

                                    * ``\f``, formfeed, decimal 12
                                    * ``\t``, tab, decimal 9
                                    * ``\n``, newline, decimal 10
                                    * ``\r``, carriage return, decimal 13
                                    * ``\v``, vertical tab, decimal 11
                                    * Non-breaking space, decimal 160

                                    ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                                * ``CSS_DECODE``:
                                    Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                    This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                    characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                    It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                    characters. For example, ``ja\vascript`` for ``javascript``.

                                * ``ESCAPE_SEQ_DECODE``:
                                    Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                    Encodings that aren't valid remain in the output.
                                * ``HEX_DECODE``:
                                    Decode a string of hexadecimal characters into a binary.
                                * ``HTML_ENTITY_DECODE``:
                                    Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                    * Replaces ``(ampersand)quot;`` with ``"``
                                    * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                    * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                    * Replaces ``(ampersand)gt;`` with ``>``
                                    * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                    * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                                * ``JS_DECODE``:
                                    Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                    then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                    higher byte is zeroed, causing a possible loss of information.
                                * ``LOWERCASE``:
                                    Convert uppercase letters (A-Z) to lowercase (a-z).
                                * ``MD5``:
                                    Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                                * ``NONE``:
                                    Specify ``NONE`` if you don't want any text transformations.
                                * ``NORMALIZE_PATH``:
                                    Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                    beginning of the input from an input string.
                                * ``NORMALIZE_PATH_WIN``:
                                    This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                                * ``REMOVE_NULLS``:
                                    Remove all NULL bytes from the input.
                                * ``REPLACE_COMMENTS``:
                                    Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                    occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                    However, a standalone termination of a comment (``*/``) is not acted upon.
                                * ``REPLACE_NULLS``:
                                    Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                                * ``SQL_HEX_DECODE``:
                                    Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                                * ``URL_DECODE``:
                                    Decode a URL-encoded value.
                                * ``URL_DECODE_UNI``:
                                    Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                    ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                    only the lower byte is used and the higher byte is zeroed.
                                * ``UTF8_TO_UNICODE``:
                                    Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                    and false-negatives for non-English languages.
                        * PositionalConstraint (str):
                            The area within the portion of the web request that you want WAF to search for ``SearchString``.
                            Valid values include the following:

                            * ``CONTAINS``:
                                The specified part of the web request must include the value of ``SearchString``, but the location doesn't matter.
                            * ``CONTAINS_WORD``:
                                The specified part of the web request must include the value of ``SearchString``, and ``SearchString`` must
                                contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition,
                                ``SearchString`` must be a word, which means that both of the following are true:

                                ``SearchString`` is at the beginning of the specified part of the web request or is preceded by a character other
                                than an alphanumeric character or underscore (_). Examples include the value of a header and ``;BadBot``.

                                `SearchString`` is at the end of the specified part of the web request or is followed by a character other than
                                an alphanumeric character or underscore (_), for example, ``BadBot;`` and ``-BadBot;``.
                            * ``EXACTLY``:
                                The value of the specified part of the web request must exactly match the value of ``SearchString``.
                            * ``STARTS_WITH``:
                                The value of ``SearchString`` must appear at the beginning of the specified part of the web request.
                            * ``ENDS_WITH``:
                                The value of ``SearchString`` must appear at the end of the specified part of the web request.
                    * SqliMatchStatement (*dict, Optional*):
                        A rule statement that inspects for malicious SQL code. Attackers insert malicious SQL code into web requests to do
                        things like modify your database or extract data from it.

                        * FieldToMatch (*dict*):
                            The part of the web request that you want WAF to inspect.

                            * SingleHeader (*dict, Optional*):
                                Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                                ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                                Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                                * Name (*str*):
                                    The name of the query header to inspect.
                            * SingleQueryArgument (*dict, Optional*):
                                Inspect a single query argument. Provide the name of the query argument to inspect, such as
                                ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                                Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                                * Name (*str*):
                                    The name of the query argument to inspect.
                            * AllQueryArguments (*dict, Optional*):
                                Inspect all query arguments.
                            * UriPath (*dict, Optional*):
                                Inspect the request URI path. This is the part of the web request that identifies a resource,
                                for example, ``/images/daily-ad.jpg``.
                            * QueryString (*dict, Optional*):
                                Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                            * Body (*dict, Optional*):
                                Inspect the request body as plain text. The request body immediately follows the request
                                headers. This is the part of a request that contains any additional data that you want to send
                                to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                                (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                                service. For information about how to handle oversized request bodies, see the Body object
                                configuration.

                                * OversizeHandling (*str, Optional*):
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Method (*dict, Optional*):
                                Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                            * JsonBody (*dict, Optional*):
                                Inspect the request body as JSON. The request body immediately follows the request headers. This
                                is the part of a request that contains any additional data that you want to send to your web
                                server as the HTTP request body, such as data from a form.

                                Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                                For information about how to handle oversized request bodies, see the JsonBody object configuration.

                                * MatchPattern (*dict*):
                                    The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                    * All (*dict, Optional*):
                                        Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                        setting or the ``IncludedPaths`` setting, but not both.
                                    * IncludedPaths (*dict, Optional*):
                                        Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                        paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                        For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                        JavaScript Object Notation (JSON) Pointer.
                                        You must specify either this setting or the ``All`` setting, but not both.

                                        .. note::
                                            Don't use this option to include all paths. Instead, use the ``All`` setting.
                                * MatchScope (*str*):
                                    The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                    against keys and values.
                                * InvalidFallbackBehavior (*str, Optional*):
                                    What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                    * ``EVALUATE_AS_STRING``:
                                        Inspect the body as plain text. WAF applies the text transformations and
                                        inspection criteria that you defined for the JSON inspection to the body text string.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE``:
                                        Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Headers (*dict, Optional*):
                                Inspect the request headers. You must configure scope and pattern matching filters in the
                                Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize header content in the Headers object. WAF applies the pattern matching filters to
                                the headers that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of headers to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                    * All (*dict, Optional*):
                                        Inspect all headers.
                                    * IncludedHeaders (*list, Optional*):
                                        Inspect only the headers that have a key that matches one of the strings specified here.
                                    * ExcludedHeaders (*list, Optional*):
                                        Inspect only the headers whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                    support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                    200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                    of header contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the headers normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                            * Cookies (*dict, Optional*):
                                Inspect the request cookies. You must configure scope and pattern matching filters in the
                                ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                                the cookies that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of cookies to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                    * All (*dict, Optional*):
                                        Inspect all cookies.
                                    * IncludedCookies (*list, Optional*):
                                        Inspect only the cookies that have a key that matches one of the strings specified here.
                                    * ExcludedCookies (*list, Optional*):
                                        Inspect only the cookies whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                    inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                    The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the cookies normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                        * TextTransformations (*list*):
                            Text transformations eliminate some of the unusual formatting that attackers use in web requests
                            in an effort to bypass detection. If you specify one or more transformations in a rule
                            statement, WAF performs all transformations on the content of the request component identified
                            by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                            match.

                            * Priority (*int*):
                                Sets the relative processing order for multiple transformations that are defined for a rule
                                statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                                the transformed content. The priorities don't need to be consecutive, but they must all be
                                different.
                            * Type (*str*):
                                You can specify the following transformation types:

                                * ``BASE64_DECODE``:
                                    Decode a Base64-encoded string.
                                * ``BASE64_DECODE_EXT``:
                                    Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                                * ``CMD_LINE``:
                                    Command-line transformations. These are helpful in reducing effectiveness of
                                    attackers who inject an operating system command-line command and use unusual formatting to
                                    disguise some or all of the command.

                                    * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                    * Delete spaces before the following characters: ``/`` ``(``
                                    * Replace the following characters with a space: ``,`` ``;``
                                    * Replace multiple spaces with one space
                                    * Convert uppercase letters (A-Z) to lowercase (a-z)
                                * ``COMPRESS_WHITE_SPACE``:
                                    Replace these characters with a space character (decimal 32):

                                    * ``\f``, formfeed, decimal 12
                                    * ``\t``, tab, decimal 9
                                    * ``\n``, newline, decimal 10
                                    * ``\r``, carriage return, decimal 13
                                    * ``\v``, vertical tab, decimal 11
                                    * Non-breaking space, decimal 160

                                    ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                                * ``CSS_DECODE``:
                                    Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                    This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                    characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                    It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                    characters. For example, ``ja\vascript`` for ``javascript``.

                                * ``ESCAPE_SEQ_DECODE``:
                                    Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                    Encodings that aren't valid remain in the output.
                                * ``HEX_DECODE``:
                                    Decode a string of hexadecimal characters into a binary.
                                * ``HTML_ENTITY_DECODE``:
                                    Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                    * Replaces ``(ampersand)quot;`` with ``"``
                                    * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                    * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                    * Replaces ``(ampersand)gt;`` with ``>``
                                    * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                    * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                                * ``JS_DECODE``:
                                    Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                    then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                    higher byte is zeroed, causing a possible loss of information.
                                * ``LOWERCASE``:
                                    Convert uppercase letters (A-Z) to lowercase (a-z).
                                * ``MD5``:
                                    Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                                * ``NONE``:
                                    Specify ``NONE`` if you don't want any text transformations.
                                * ``NORMALIZE_PATH``:
                                    Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                    beginning of the input from an input string.
                                * ``NORMALIZE_PATH_WIN``:
                                    This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                                * ``REMOVE_NULLS``:
                                    Remove all NULL bytes from the input.
                                * ``REPLACE_COMMENTS``:
                                    Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                    occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                    However, a standalone termination of a comment (``*/``) is not acted upon.
                                * ``REPLACE_NULLS``:
                                    Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                                * ``SQL_HEX_DECODE``:
                                    Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                                * ``URL_DECODE``:
                                    Decode a URL-encoded value.
                                * ``URL_DECODE_UNI``:
                                    Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                    ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                    only the lower byte is used and the higher byte is zeroed.
                                * ``UTF8_TO_UNICODE``:
                                    Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                    and false-negatives for non-English languages.

                        * SensitivityLevel (*str*):
                            The sensitivity that you want WAF to use to inspect for SQL injection attacks.

                            ``HIGH`` detects more attacks, but might generate more false positives, especially if your web requests frequently
                            contain unusual strings. For information about identifying and mitigating false positives, see Testing and tuning in
                            the WAF Developer Guide.
                            ``LOW`` is generally a better choice for resources that already have other protections against SQL injection attacks
                            or that have a low tolerance for false positives.

                    * XssMatchStatement (*dict, Optional*):
                        A rule statement that inspects for cross-site scripting (XSS) attacks. In XSS attacks, the attacker uses vulnerabilities
                        in a benign website as a vehicle to inject malicious client-site scripts into other legitimate web browsers.

                        * FieldToMatch (*dict*):
                            The part of the web request that you want WAF to inspect.

                            * SingleHeader (*dict, Optional*):
                                Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                                ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                                Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                                * Name (*str*):
                                    The name of the query header to inspect.
                            * SingleQueryArgument (*dict, Optional*):
                                Inspect a single query argument. Provide the name of the query argument to inspect, such as
                                ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                                Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                                * Name (*str*):
                                    The name of the query argument to inspect.
                            * AllQueryArguments (*dict, Optional*):
                                Inspect all query arguments.
                            * UriPath (*dict, Optional*):
                                Inspect the request URI path. This is the part of the web request that identifies a resource,
                                for example, ``/images/daily-ad.jpg``.
                            * QueryString (*dict, Optional*):
                                Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                            * Body (*dict, Optional*):
                                Inspect the request body as plain text. The request body immediately follows the request
                                headers. This is the part of a request that contains any additional data that you want to send
                                to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                                (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                                service. For information about how to handle oversized request bodies, see the Body object
                                configuration.

                                * OversizeHandling (*str, Optional*):
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Method (*dict, Optional*):
                                Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                            * JsonBody (*dict, Optional*):
                                Inspect the request body as JSON. The request body immediately follows the request headers. This
                                is the part of a request that contains any additional data that you want to send to your web
                                server as the HTTP request body, such as data from a form.

                                Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                                For information about how to handle oversized request bodies, see the JsonBody object configuration.

                                * MatchPattern (*dict*):
                                    The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                    * All (*dict, Optional*):
                                        Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                        setting or the ``IncludedPaths`` setting, but not both.
                                    * IncludedPaths (*dict, Optional*):
                                        Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                        paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                        For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                        JavaScript Object Notation (JSON) Pointer.
                                        You must specify either this setting or the ``All`` setting, but not both.

                                        .. note::
                                            Don't use this option to include all paths. Instead, use the ``All`` setting.
                                * MatchScope (*str*):
                                    The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                    against keys and values.
                                * InvalidFallbackBehavior (*str, Optional*):
                                    What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                    * ``EVALUATE_AS_STRING``:
                                        Inspect the body as plain text. WAF applies the text transformations and
                                        inspection criteria that you defined for the JSON inspection to the body text string.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE``:
                                        Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Headers (*dict, Optional*):
                                Inspect the request headers. You must configure scope and pattern matching filters in the
                                Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize header content in the Headers object. WAF applies the pattern matching filters to
                                the headers that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of headers to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                    * All (*dict, Optional*):
                                        Inspect all headers.
                                    * IncludedHeaders (*list, Optional*):
                                        Inspect only the headers that have a key that matches one of the strings specified here.
                                    * ExcludedHeaders (*list, Optional*):
                                        Inspect only the headers whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                    support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                    200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                    of header contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the headers normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                            * Cookies (*dict, Optional*):
                                Inspect the request cookies. You must configure scope and pattern matching filters in the
                                ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                                the cookies that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of cookies to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                    * All (*dict, Optional*):
                                        Inspect all cookies.
                                    * IncludedCookies (*list, Optional*):
                                        Inspect only the cookies that have a key that matches one of the strings specified here.
                                    * ExcludedCookies (*list, Optional*):
                                        Inspect only the cookies whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                    inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                    The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the cookies normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                        * TextTransformations (*list*):
                            Text transformations eliminate some of the unusual formatting that attackers use in web requests
                            in an effort to bypass detection. If you specify one or more transformations in a rule
                            statement, WAF performs all transformations on the content of the request component identified
                            by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                            match.

                            * Priority (*int*):
                                Sets the relative processing order for multiple transformations that are defined for a rule
                                statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                                the transformed content. The priorities don't need to be consecutive, but they must all be
                                different.
                            * Type (*str*):
                                You can specify the following transformation types:

                                * ``BASE64_DECODE``:
                                    Decode a Base64-encoded string.
                                * ``BASE64_DECODE_EXT``:
                                    Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                                * ``CMD_LINE``:
                                    Command-line transformations. These are helpful in reducing effectiveness of
                                    attackers who inject an operating system command-line command and use unusual formatting to
                                    disguise some or all of the command.

                                    * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                    * Delete spaces before the following characters: ``/`` ``(``
                                    * Replace the following characters with a space: ``,`` ``;``
                                    * Replace multiple spaces with one space
                                    * Convert uppercase letters (A-Z) to lowercase (a-z)
                                * ``COMPRESS_WHITE_SPACE``:
                                    Replace these characters with a space character (decimal 32):

                                    * ``\f``, formfeed, decimal 12
                                    * ``\t``, tab, decimal 9
                                    * ``\n``, newline, decimal 10
                                    * ``\r``, carriage return, decimal 13
                                    * ``\v``, vertical tab, decimal 11
                                    * Non-breaking space, decimal 160

                                    ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                                * ``CSS_DECODE``:
                                    Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                    This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                    characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                    It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                    characters. For example, ``ja\vascript`` for ``javascript``.

                                * ``ESCAPE_SEQ_DECODE``:
                                    Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                    Encodings that aren't valid remain in the output.
                                * ``HEX_DECODE``:
                                    Decode a string of hexadecimal characters into a binary.
                                * ``HTML_ENTITY_DECODE``:
                                    Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                    * Replaces ``(ampersand)quot;`` with ``"``
                                    * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                    * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                    * Replaces ``(ampersand)gt;`` with ``>``
                                    * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                    * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                                * ``JS_DECODE``:
                                    Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                    then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                    higher byte is zeroed, causing a possible loss of information.
                                * ``LOWERCASE``:
                                    Convert uppercase letters (A-Z) to lowercase (a-z).
                                * ``MD5``:
                                    Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                                * ``NONE``:
                                    Specify ``NONE`` if you don't want any text transformations.
                                * ``NORMALIZE_PATH``:
                                    Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                    beginning of the input from an input string.
                                * ``NORMALIZE_PATH_WIN``:
                                    This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                                * ``REMOVE_NULLS``:
                                    Remove all NULL bytes from the input.
                                * ``REPLACE_COMMENTS``:
                                    Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                    occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                    However, a standalone termination of a comment (``*/``) is not acted upon.
                                * ``REPLACE_NULLS``:
                                    Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                                * ``SQL_HEX_DECODE``:
                                    Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                                * ``URL_DECODE``:
                                    Decode a URL-encoded value.
                                * ``URL_DECODE_UNI``:
                                    Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                    ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                    only the lower byte is used and the higher byte is zeroed.
                                * ``UTF8_TO_UNICODE``:
                                    Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                    and false-negatives for non-English languages.

                    * SizeConstraintStatement (*dict, Optional*):
                        A rule statement that compares a number of bytes against the size of a request component, using a comparison operator,
                        such as greater than (``>``) or less than (``<``). For example, you can use a size constraint statement to look for query strings
                        that are longer than 100 bytes.

                        If you configure WAF to inspect the request body, WAF inspects only the first 8192 bytes (8 KB). If the request body
                        for your web requests never exceeds 8192 bytes, you could use a size constraint statement to block requests that have a
                        request body greater than 8192 bytes.

                        If you choose URI for the value of Part of the request to filter on, the slash (``/``) in the URI counts as one character.
                        For example, the URI ``/logo.jpg`` is nine characters long.

                        * FieldToMatch (*dict*):
                            The part of the web request that you want WAF to inspect.

                            * SingleHeader (*dict, Optional*):
                                Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                                ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                                Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                                * Name (*str*):
                                    The name of the query header to inspect.
                            * SingleQueryArgument (*dict, Optional*):
                                Inspect a single query argument. Provide the name of the query argument to inspect, such as
                                ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                                Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                                * Name (*str*):
                                    The name of the query argument to inspect.
                            * AllQueryArguments (*dict, Optional*):
                                Inspect all query arguments.
                            * UriPath (*dict, Optional*):
                                Inspect the request URI path. This is the part of the web request that identifies a resource,
                                for example, ``/images/daily-ad.jpg``.
                            * QueryString (*dict, Optional*):
                                Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                            * Body (*dict, Optional*):
                                Inspect the request body as plain text. The request body immediately follows the request
                                headers. This is the part of a request that contains any additional data that you want to send
                                to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                                (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                                service. For information about how to handle oversized request bodies, see the Body object
                                configuration.

                                * OversizeHandling (*str, Optional*):
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Method (*dict, Optional*):
                                Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                            * JsonBody (*dict, Optional*):
                                Inspect the request body as JSON. The request body immediately follows the request headers. This
                                is the part of a request that contains any additional data that you want to send to your web
                                server as the HTTP request body, such as data from a form.

                                Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                                For information about how to handle oversized request bodies, see the JsonBody object configuration.

                                * MatchPattern (*dict*):
                                    The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                    * All (*dict, Optional*):
                                        Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                        setting or the ``IncludedPaths`` setting, but not both.
                                    * IncludedPaths (*dict, Optional*):
                                        Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                        paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                        For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                        JavaScript Object Notation (JSON) Pointer.
                                        You must specify either this setting or the ``All`` setting, but not both.

                                        .. note::
                                            Don't use this option to include all paths. Instead, use the ``All`` setting.
                                * MatchScope (*str*):
                                    The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                    against keys and values.
                                * InvalidFallbackBehavior (*str, Optional*):
                                    What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                    * ``EVALUATE_AS_STRING``:
                                        Inspect the body as plain text. WAF applies the text transformations and
                                        inspection criteria that you defined for the JSON inspection to the body text string.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE``:
                                        Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Headers (*dict, Optional*):
                                Inspect the request headers. You must configure scope and pattern matching filters in the
                                Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize header content in the Headers object. WAF applies the pattern matching filters to
                                the headers that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of headers to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                    * All (*dict, Optional*):
                                        Inspect all headers.
                                    * IncludedHeaders (*list, Optional*):
                                        Inspect only the headers that have a key that matches one of the strings specified here.
                                    * ExcludedHeaders (*list, Optional*):
                                        Inspect only the headers whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                    support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                    200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                    of header contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the headers normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                            * Cookies (*dict, Optional*):
                                Inspect the request cookies. You must configure scope and pattern matching filters in the
                                ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                                the cookies that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of cookies to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                    * All (*dict, Optional*):
                                        Inspect all cookies.
                                    * IncludedCookies (*list, Optional*):
                                        Inspect only the cookies that have a key that matches one of the strings specified here.
                                    * ExcludedCookies (*list, Optional*):
                                        Inspect only the cookies whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                    inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                    The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the cookies normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                        * ComparisonOperator (*str*):
                            The operator to use to compare the request part to the size setting.
                        * Size (*int*):
                            The size, in byte, to compare to the request part, after any transformations.
                        * TextTransformations (*list*):
                            Text transformations eliminate some of the unusual formatting that attackers use in web requests
                            in an effort to bypass detection. If you specify one or more transformations in a rule
                            statement, WAF performs all transformations on the content of the request component identified
                            by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                            match.

                            * Priority (*int*):
                                Sets the relative processing order for multiple transformations that are defined for a rule
                                statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                                the transformed content. The priorities don't need to be consecutive, but they must all be
                                different.
                            * Type (*str*):
                                You can specify the following transformation types:

                                * ``BASE64_DECODE``:
                                    Decode a Base64-encoded string.
                                * ``BASE64_DECODE_EXT``:
                                    Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                                * ``CMD_LINE``:
                                    Command-line transformations. These are helpful in reducing effectiveness of
                                    attackers who inject an operating system command-line command and use unusual formatting to
                                    disguise some or all of the command.

                                    * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                    * Delete spaces before the following characters: ``/`` ``(``
                                    * Replace the following characters with a space: ``,`` ``;``
                                    * Replace multiple spaces with one space
                                    * Convert uppercase letters (A-Z) to lowercase (a-z)
                                * ``COMPRESS_WHITE_SPACE``:
                                    Replace these characters with a space character (decimal 32):

                                    * ``\f``, formfeed, decimal 12
                                    * ``\t``, tab, decimal 9
                                    * ``\n``, newline, decimal 10
                                    * ``\r``, carriage return, decimal 13
                                    * ``\v``, vertical tab, decimal 11
                                    * Non-breaking space, decimal 160

                                    ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                                * ``CSS_DECODE``:
                                    Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                    This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                    characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                    It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                    characters. For example, ``ja\vascript`` for ``javascript``.

                                * ``ESCAPE_SEQ_DECODE``:
                                    Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                    Encodings that aren't valid remain in the output.
                                * ``HEX_DECODE``:
                                    Decode a string of hexadecimal characters into a binary.
                                * ``HTML_ENTITY_DECODE``:
                                    Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                    * Replaces ``(ampersand)quot;`` with ``"``
                                    * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                    * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                    * Replaces ``(ampersand)gt;`` with ``>``
                                    * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                    * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                                * ``JS_DECODE``:
                                    Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                    then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                    higher byte is zeroed, causing a possible loss of information.
                                * ``LOWERCASE``:
                                    Convert uppercase letters (A-Z) to lowercase (a-z).
                                * ``MD5``:
                                    Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                                * ``NONE``:
                                    Specify ``NONE`` if you don't want any text transformations.
                                * ``NORMALIZE_PATH``:
                                    Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                    beginning of the input from an input string.
                                * ``NORMALIZE_PATH_WIN``:
                                    This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                                * ``REMOVE_NULLS``:
                                    Remove all NULL bytes from the input.
                                * ``REPLACE_COMMENTS``:
                                    Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                    occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                    However, a standalone termination of a comment (``*/``) is not acted upon.
                                * ``REPLACE_NULLS``:
                                    Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                                * ``SQL_HEX_DECODE``:
                                    Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                                * ``URL_DECODE``:
                                    Decode a URL-encoded value.
                                * ``URL_DECODE_UNI``:
                                    Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                    ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                    only the lower byte is used and the higher byte is zeroed.
                                * ``UTF8_TO_UNICODE``:
                                    Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                    and false-negatives for non-English languages.

                    * GeoMatchStatement (*dict, Optional*):
                        A rule statement used to identify web requests based on country of origin.

                        * CountryCodes (*list, Optional*):
                            An array of two-character country codes, for example, ``[ "US", "CN" ]``, from the alpha-2 country ISO codes of
                            the ISO 3166 international standard.
                        * ForwardedIPConfig (*dict, Optional*):
                            The configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address
                            that's reported by the web request origin. Commonly, this is the X-Forwarded-For (XFF) header, but you can specify
                            any header name.

                            .. note::
                                If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                            * HeaderName (*str*):
                                The name of the HTTP header to use for the IP address. For example, to use the X-Forwarded-For (XFF) header,
                                set this to ``X-Forwarded-For``.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.
                            * FallbackBehavior (*str*):
                                The match status to assign to the web request if the request doesn't have a valid IP address in the specified position.
                                You can specify the following fallback behaviors:

                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                    * RuleGroupReferenceStatement (*dict, Optional*):
                        A rule statement used to run the rules that are defined in a ``RuleGroup``. To use this, create a rule group with your rules,
                        then provide the ARN of the rule group in this statement.

                        You cannot nest a ``RuleGroupReferenceStatement``, for example for use inside a ``NotStatement`` or ``OrStatement``.
                        You can only use a rule group reference statement at the top level inside a web ACL.

                        * ARN (*str*):
                            The Amazon Resource Name (ARN) of the entity.
                        * ExcludedRules (*list, Optional*):
                            The rules in the referenced rule group whose actions are set to Count. When you exclude a rule,
                            WAF evaluates it exactly as it would if the rule action setting were Count. This is a useful
                            option for testing the rules in a rule group without modifying how they handle your web traffic.

                            * (*dict*):
                                Specifies a single rule in a rule group whose action you want to override to ``Count``.
                                When you exclude a rule, WAF evaluates it exactly as it would if the rule action setting were ``Count``.
                                This is a useful option for testing the rules in a rule group without modifying how they handle your web traffic.

                            * Name (*str*):
                                The name of the rule whose action you want to override to ``Count``.
                    * IPSetReferenceStatement (*dict, Optional*):
                        A rule statement used to detect web requests coming from particular IP addresses or address ranges. To use this,
                        create an IPSet that specifies the addresses you want to detect, then use the ARN of that set in this statement.

                        Each IP set rule statement references an IP set. You create and maintain the set independent of your rules. This allows
                        you to use the single set in multiple rules. When you update the referenced set, WAF automatically updates all rules
                        that reference it.

                        * ARN (*str*):
                            The Amazon Resource Name (ARN) of the IPSet that this statement references.
                        * IPSetForwardedIPConfig (*dict, Optional*):
                            The configuration for inspecting IP addresses in an HTTP header that you specify, instead of
                            using the IP address that's reported by the web request origin. Commonly, this is the
                            X-Forwarded-For (XFF) header, but you can specify any header name.

                            .. note::
                                If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                            * HeaderName (*str*):
                                The name of the HTTP header to use for the IP address. For example, to use the X-Forwarded-For
                                (XFF) header, set this to X-Forwarded-For.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.
                            * FallbackBehavior (*str*):
                                The match status to assign to the web request if the request doesn't have a valid IP address in
                                the specified position.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                                You can specify the following fallback behaviors:

                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.
                        * Position (*str*):
                            The position in the header to search for the IP address. The header can contain IP addresses of
                            the original client and also of proxies. For example, the header value could be ``10.1.1.1``,
                            ``127.0.0.0``, ``10.10.10.10`` where the first IP address identifies the original client and the rest
                            identify proxies that the request went through.

                            The options for this setting are the following:

                            * ``FIRST``:
                                Inspect the first IP address in the list of IP addresses in the header. This is usually the client's original IP.
                            * ``LAST``:
                                Inspect the last IP address in the list of IP addresses in the header.
                            * ``ANY``:
                                Inspect all IP addresses in the header for a match. If the header contains more than 10 IP addresses, WAF inspects the last 10.
                    * RegexPatternSetReferenceStatement (*dict, Optional*):
                        A rule statement used to search web request components for matches with regular expressions. To use this, create
                        a ``RegexPatternSet`` that specifies the expressions that you want to detect, then use the ARN of that set in this
                        statement. A web request matches the pattern set rule statement if the request component matches any of the patterns
                        in the set.

                        Each regex pattern set rule statement references a regex pattern set. You create and maintain the set independent of
                        your rules. This allows you to use the single set in multiple rules. When you update the referenced set, WAF
                        automatically updates all rules that reference it.

                        * ARN (*str*):
                            The Amazon Resource Name (ARN) of the RegexPatternSet that this statement references.
                        * FieldToMatch (*dict*):
                            The part of the web request that you want WAF to inspect.

                            * SingleHeader (*dict, Optional*):
                                Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                                ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                                Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                                * Name (*str*):
                                    The name of the query header to inspect.
                            * SingleQueryArgument (*dict, Optional*):
                                Inspect a single query argument. Provide the name of the query argument to inspect, such as
                                ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                                Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                                * Name (*str*):
                                    The name of the query argument to inspect.
                            * AllQueryArguments (*dict, Optional*):
                                Inspect all query arguments.
                            * UriPath (*dict, Optional*):
                                Inspect the request URI path. This is the part of the web request that identifies a resource,
                                for example, ``/images/daily-ad.jpg``.
                            * QueryString (*dict, Optional*):
                                Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                            * Body (*dict, Optional*):
                                Inspect the request body as plain text. The request body immediately follows the request
                                headers. This is the part of a request that contains any additional data that you want to send
                                to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                                (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                                service. For information about how to handle oversized request bodies, see the Body object
                                configuration.

                                * OversizeHandling (*str, Optional*):
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Method (*dict, Optional*):
                                Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                            * JsonBody (*dict, Optional*):
                                Inspect the request body as JSON. The request body immediately follows the request headers. This
                                is the part of a request that contains any additional data that you want to send to your web
                                server as the HTTP request body, such as data from a form.

                                Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                                For information about how to handle oversized request bodies, see the JsonBody object configuration.

                                * MatchPattern (*dict*):
                                    The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                    * All (*dict, Optional*):
                                        Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                        setting or the ``IncludedPaths`` setting, but not both.
                                    * IncludedPaths (*dict, Optional*):
                                        Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                        paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                        For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                        JavaScript Object Notation (JSON) Pointer.
                                        You must specify either this setting or the ``All`` setting, but not both.

                                        .. note::
                                            Don't use this option to include all paths. Instead, use the ``All`` setting.
                                * MatchScope (*str*):
                                    The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                    against keys and values.
                                * InvalidFallbackBehavior (*str, Optional*):
                                    What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                    * ``EVALUATE_AS_STRING``:
                                        Inspect the body as plain text. WAF applies the text transformations and
                                        inspection criteria that you defined for the JSON inspection to the body text string.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                    the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                    Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                    The options for oversize handling are the following:

                                    * ``CONTINUE``:
                                        Inspect the body normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                                    You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                    settings, so that you block any request whose body is over 8 KB.
                            * Headers (*dict, Optional*):
                                Inspect the request headers. You must configure scope and pattern matching filters in the
                                Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize header content in the Headers object. WAF applies the pattern matching filters to
                                the headers that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of headers to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                    * All (*dict, Optional*):
                                        Inspect all headers.
                                    * IncludedHeaders (*list, Optional*):
                                        Inspect only the headers that have a key that matches one of the strings specified here.
                                    * ExcludedHeaders (*list, Optional*):
                                        Inspect only the headers whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                    support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                    200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                    of header contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the headers normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                            * Cookies (*dict, Optional*):
                                Inspect the request cookies. You must configure scope and pattern matching filters in the
                                ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                                Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                                forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                                any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                                the cookies that it receives from the underlying host service.

                                * MatchPattern (*dict*):
                                    The filter to use to identify the subset of cookies to inspect in a web request.
                                    You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                    * All (*dict, Optional*):
                                        Inspect all cookies.
                                    * IncludedCookies (*list, Optional*):
                                        Inspect only the cookies that have a key that matches one of the strings specified here.
                                    * ExcludedCookies (*list, Optional*):
                                        Inspect only the cookies whose keys don't match any of the strings specified here.
                                * MatchScope (*str*):
                                    The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                    inspects both keys and values.
                                * OversizeHandling (*str, Optional*)
                                    What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                    inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                    The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                    * ``CONTINUE``:
                                        Inspect the cookies normally, according to the rule inspection criteria.
                                    * ``MATCH``:
                                        Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                    * ``NO_MATCH``:
                                        Treat the web request as not matching the rule statement.

                        * TextTransformations (*list*):
                            Text transformations eliminate some of the unusual formatting that attackers use in web requests
                            in an effort to bypass detection. If you specify one or more transformations in a rule
                            statement, WAF performs all transformations on the content of the request component identified
                            by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                            match.

                            * Priority (*int*):
                                Sets the relative processing order for multiple transformations that are defined for a rule
                                statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                                the transformed content. The priorities don't need to be consecutive, but they must all be
                                different.
                            * Type (*str*):
                                You can specify the following transformation types:

                                * ``BASE64_DECODE``:
                                    Decode a Base64-encoded string.
                                * ``BASE64_DECODE_EXT``:
                                    Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                                * ``CMD_LINE``:
                                    Command-line transformations. These are helpful in reducing effectiveness of
                                    attackers who inject an operating system command-line command and use unusual formatting to
                                    disguise some or all of the command.

                                    * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                    * Delete spaces before the following characters: ``/`` ``(``
                                    * Replace the following characters with a space: ``,`` ``;``
                                    * Replace multiple spaces with one space
                                    * Convert uppercase letters (A-Z) to lowercase (a-z)
                                * ``COMPRESS_WHITE_SPACE``:
                                    Replace these characters with a space character (decimal 32):

                                    * ``\f``, formfeed, decimal 12
                                    * ``\t``, tab, decimal 9
                                    * ``\n``, newline, decimal 10
                                    * ``\r``, carriage return, decimal 13
                                    * ``\v``, vertical tab, decimal 11
                                    * Non-breaking space, decimal 160

                                    ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                                * ``CSS_DECODE``:
                                    Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                    This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                    characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                    It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                    characters. For example, ``ja\vascript`` for ``javascript``.

                                * ``ESCAPE_SEQ_DECODE``:
                                    Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                    Encodings that aren't valid remain in the output.
                                * ``HEX_DECODE``:
                                    Decode a string of hexadecimal characters into a binary.
                                * ``HTML_ENTITY_DECODE``:
                                    Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                    * Replaces ``(ampersand)quot;`` with ``"``
                                    * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                    * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                    * Replaces ``(ampersand)gt;`` with ``>``
                                    * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                    * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                                * ``JS_DECODE``:
                                    Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                    then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                    higher byte is zeroed, causing a possible loss of information.
                                * ``LOWERCASE``:
                                    Convert uppercase letters (A-Z) to lowercase (a-z).
                                * ``MD5``:
                                    Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                                * ``NONE``:
                                    Specify ``NONE`` if you don't want any text transformations.
                                * ``NORMALIZE_PATH``:
                                    Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                    beginning of the input from an input string.
                                * ``NORMALIZE_PATH_WIN``:
                                    This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                                * ``REMOVE_NULLS``:
                                    Remove all NULL bytes from the input.
                                * ``REPLACE_COMMENTS``:
                                    Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                    occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                    However, a standalone termination of a comment (``*/``) is not acted upon.
                                * ``REPLACE_NULLS``:
                                    Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                                * ``SQL_HEX_DECODE``:
                                    Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                                * ``URL_DECODE``:
                                    Decode a URL-encoded value.
                                * ``URL_DECODE_UNI``:
                                    Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                    ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                    only the lower byte is used and the higher byte is zeroed.
                                * ``UTF8_TO_UNICODE``:
                                    Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                    and false-negatives for non-English languages.

                    * RateBasedStatement (*dict, Optional*):
                        A rate-based rule tracks the rate of requests for each originating IP address, and triggers the rule action when
                        the rate exceeds a limit that you specify on the number of requests in any 5-minute time span. You can use this to
                        put a temporary block on requests from an IP address that is sending excessive requests.

                        WAF tracks and manages web requests separately for each instance of a rate-based rule that you use. For example, if
                        you provide the same rate-based rule settings in two web ACLs, each of the two rule statements represents a separate
                        instance of the rate-based rule and gets its own tracking and management by WAF. If you define a rate-based rule inside
                        a rule group, and then use that rule group in multiple places, each use creates a separate instance of the rate-based
                        rule that gets its own tracking and management by WAF.

                        When the rule action triggers, WAF blocks additional requests from the IP address until the request rate falls below the limit.

                        You can optionally nest another statement inside the rate-based statement, to narrow the scope of the rule so that it
                        only counts requests that match the nested statement. For example, based on recent requests that you have seen from an
                        attacker, you might create a rate-based rule with a nested AND rule statement that contains the following nested
                        statements:

                        * An IP match statement with an IP set that specified the address 192.0.2.44.
                        * A string match statement that searches in the User-Agent header for the string BadBot.

                        In this rate-based rule, you also define a rate limit. For this example, the rate limit is 1,000. Requests that meet the
                        criteria of both of the nested statements are counted. If the count exceeds 1,000 requests per five minutes, the rule
                        action triggers. Requests that do not meet the criteria of both of the nested statements are not counted towards the
                        rate limit and are not affected by this rule.

                        You cannot nest a ``RateBasedStatement`` inside another statement, for example inside a ``NotStatement`` or ``OrStatement``.
                        You can define a ``RateBasedStatement`` inside a web ACL and inside a rule group.

                        * Limit (*int*):
                            The limit on requests per 5-minute period for a single originating IP address. If the statement
                            includes a ``ScopeDownStatement``, this limit is applied only to the requests that match the statement.
                        * AggregateKeyType (*str*):
                            Setting that indicates how to aggregate the request counts. The options are the following:

                            * ``IP``:
                                Aggregate the request counts on the IP address from the web request origin.
                            * ``FORWARDED_IP``:
                                Aggregate the request counts on the first IP address in an HTTP header. If you use this,
                                configure the ForwardedIPConfig, to specify the header to use.
                        * ScopeDownStatement (*dict, Optional*):
                            An optional nested statement that narrows the scope of the web requests that are evaluated by
                            the rate-based statement. Requests are only tracked by the rate-based statement if they match
                            the scope-down statement. You can use any nestable Statement in the scope-down statement, and
                            you can nest statements at any level, the same as you can for a rule statement.
                        * ForwardedIPConfig (*dict, Optional*):
                            The configuration for inspecting IP addresses in an HTTP header that you specify, instead of
                            using the IP address that's reported by the web request origin. Commonly, this is the
                            X-Forwarded-For (XFF) header, but you can specify any header name.

                            .. note::
                                If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                            This is required if ``AggregateKeyType`` is set to ``FORWARDED_IP``.

                            * HeaderName (*str*):
                                The name of the HTTP header to use for the IP address. For example, to use the X-Forwarded-For (XFF) header,
                                set this to ``X-Forwarded-For``.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.
                            * FallbackBehavior (*str*):
                                The match status to assign to the web request if the request doesn't have a valid IP address in the specified position.
                                You can specify the following fallback behaviors:

                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.

                                .. note::
                                    If the specified header isn't present in the request, WAF doesn't apply the rule to the web request at all.

                    * AndStatement (*dict, Optional*):
                        A logical rule statement used to combine other rule statements with AND logic. You provide more
                        than one Statement within the ``AndStatement``.

                        * Statements (*list*):
                            The statements to combine with AND logic. You can use any statements that can be nested.

                            * (*dict*):
                                The processing guidance for a ``Rule``, used by WAF to determine whether a web request matches the rule.
                    * OrStatement (*dict, Optional*):
                        A logical rule statement used to combine other rule statements with OR logic. You provide more
                        than one Statement within the ``OrStatement``.

                        * Statements (*list*):
                            The statements to combine with OR logic. You can use any statements that can be nested.

                            * (*dict*):
                                The processing guidance for a ``Rule``, used by WAF to determine whether a web request matches the rule.

                    * NotStatement (*dict, Optional*):
                        A logical rule statement used to negate the results of another rule statement. You provide more
                        than one Statement within the ``NotStatement``.

                        * Statements (*list*):
                            The statement to negate. You can use any statements that can be nested.

                            * (*dict*):
                                The processing guidance for a ``Rule``, used by WAF to determine whether a web request matches the rule.

                    * ManagedRuleGroupStatement (*dict, Optional*):
                        A rule statement used to run the rules that are defined in a managed rule group. To use this, provide the vendor\
                        name and the name of the rule group in this statement.

                        You cannot nest a ``ManagedRuleGroupStatement``, for example for use inside a ``NotStatement`` or ``OrStatement``.
                        It can only be referenced as a top-level statement within a rule.

                        * VendorName (*str*):
                            The name of the managed rule group vendor. You use this, along with the rule group name, to identify the rule group.
                        * Name (*str*):
                            The name of the managed rule group. You use this, along with the vendor name, to identify the rule group.
                        * Version (*str*, Optional):
                            The version of the managed rule group to use. If you specify this, the version setting is fixed until you change it.
                            If you don't specify this, WAF uses the vendor's default version, and then keeps the version at the vendor's default
                            when the vendor updates the managed rule group settings.
                        * ExcludedRules (*list*, Optional):
                            The rules in the referenced rule group whose actions are set to ``Count``. When you exclude a rule, WAF evaluates
                            it exactly as it would if the rule action setting were ``Count``. This is a useful option for testing the rules in
                            a rule group without modifying how they handle your web traffic.

                            * (*dict*):
                                Specifies a single rule in a rule group whose action you want to override to ``Count``.
                                When you exclude a rule, WAF evaluates it exactly as it would if the rule action setting were ``Count``.
                                This is a useful option for testing the rules in a rule group without modifying how they handle your web traffic.

                                * Name (*str*):
                                    The name of the rule whose action you want to override to Count .

                        * ScopeDownStatement (*dict, Optional*):
                            An optional nested statement that narrows the scope of the web requests that are evaluated by the managed rule group.
                            Requests are only evaluated by the rule group if they match the scope-down statement. You can use any nestable Statement
                            in the scope-down statement, and you can nest statements at any level, the same as you can for a rule statement.
                        * ManagedRuleGroupConfigs (*list, Optional*):
                            Additional information that's used by a managed rule group. Most managed rule groups don't require this.

                            Use this for the account takeover prevention managed rule group ``AWSManagedRulesATPRuleSet``, to provide information
                            about the sign-in page of your application.

                            You can provide multiple individual ``ManagedRuleGroupConfig`` objects for any rule group configuration, for example
                            ``UsernameField`` and ``PasswordField``. The configuration that you provide depends on the needs of the managed rule group.
                            For the ATP managed rule group, you provide the following individual configuration objects: ``LoginPath``, ``PasswordField``,
                            ``PayloadType`` and ``UsernameField``.

                            * (*dict*):
                                Additional information that's used by a managed rule group. Most managed rule groups don't require this.

                                Use this for the account takeover prevention managed rule group ``AWSManagedRulesATPRuleSet``, to provide information
                                about the sign-in page of your application.

                                You can provide multiple individual ``ManagedRuleGroupConfig`` objects for any rule group configuration,
                                for example ``UsernameField`` and ``PasswordField``. The configuration that you provide depends on the needs
                                of the managed rule group. For the ATP managed rule group, you provide the following individual configuration
                                objects: ``LoginPath``, ``PasswordField``, ``PayloadType`` and ``UsernameField``.

                                * LoginPath (*str, Optional*):
                                    The path of the login endpoint for your application. For example, for the URL ``https://example.com/web/login``,
                                    you would provide the path ``/web/login``.
                                * PayloadType (*str, Optional*):
                                    The payload type for your login endpoint, either JSON or form encoded.
                                * UsernameField (*dict*):
                                    Details about your login page username field.

                                    * Identifier (*str*):
                                        The name of the username field. For example ``/form/username``.
                                * PasswordField (*dict*):
                                    Details about your login page password field.

                                    * Identifier (*str*):
                                        The name of the password field. For example ``/form/password``.
                    * LabelMatchStatement (*dict, Optional*):
                        A rule statement that defines a string match search against labels that have been added to the web request by rules that
                        have already run in the web ACL.

                        The label match statement provides the label or namespace string to search for. The label string can represent a part or
                        all of the fully qualified label name that had been added to the web request. Fully qualified labels have a prefix, optional
                        namespaces, and label name. The prefix identifies the rule group or web ACL context of the rule that added the label. If you
                        do not provide the fully qualified name in your label match string, WAF performs the search for labels that were added in the
                        same context as the label match statement.

                        * Scope (*str*):
                            Specify whether you want to match using the label name or just the namespace.
                        * Key (*str*):
                            The string to match against. The setting you provide for this depends on the match statement's ``Scope`` setting:

                            * If the ``Scope`` indicates ``LABEL``, then this specification must include the name and can include any number
                                of preceding namespace specifications and prefix up to providing the fully qualified label name.
                            * If the ``Scope`` indicates ``NAMESPACE``, then this specification can include any number of contiguous namespace
                                strings, and can include the entire label namespace prefix from the rule group or web ACL where the label originates.

                            Labels are case sensitive and components of a label must be separated by colon, for example ``NS1:NS2:name``.
                * RegexMatchStatement (*dict, Optional*):
                    A rule statement used to search web request components for a match against a single regular expression.

                    * RegexString (*str*):
                        The string representing the regular expression.
                    * FieldToMatch (*dict*):
                        The part of the web request that you want WAF to inspect.

                        * SingleHeader (*dict, Optional*):
                            Inspect a single header. Provide the name of the header to inspect, for example, ``User-Agent`` or
                            ``Referer``. This setting isn't case sensitive. Example JSON: ``"SingleHeader": { "Name": "haystack" }``
                            Alternately, you can filter and inspect all headers with the ``Headers FieldToMatch`` setting.

                            * Name (*str*):
                                The name of the query header to inspect.
                        * SingleQueryArgument (*dict, Optional*):
                            Inspect a single query argument. Provide the name of the query argument to inspect, such as
                            ``UserName`` or ``SalesRegion``. The name can be up to 30 characters long and isn't case sensitive.
                            Example JSON: ``"SingleQueryArgument": { "Name": "myArgument" }``.

                            * Name (*str*):
                                The name of the query argument to inspect.
                        * AllQueryArguments (*dict, Optional*):
                            Inspect all query arguments.
                        * UriPath (*dict, Optional*):
                            Inspect the request URI path. This is the part of the web request that identifies a resource,
                            for example, ``/images/daily-ad.jpg``.
                        * QueryString (*dict, Optional*):
                            Inspect the query string. This is the part of a URL that appears after a ``?`` character, if any.
                        * Body (*dict, Optional*):
                            Inspect the request body as plain text. The request body immediately follows the request
                            headers. This is the part of a request that contains any additional data that you want to send
                            to your web server as the HTTP request body, such as data from a form.  Only the first 8 KB
                            (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host
                            service. For information about how to handle oversized request bodies, see the Body object
                            configuration.

                            * OversizeHandling (*str, Optional*):
                                What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                The options for oversize handling are the following:

                                * ``CONTINUE`` - Inspect the body normally, according to the rule inspection criteria.
                                * ``MATCH`` - Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH`` - Treat the web request as not matching the rule statement.

                                You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                settings, so that you block any request whose body is over 8 KB.
                        * Method (*dict, Optional*):
                            Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
                        * JsonBody (*dict, Optional*):
                            Inspect the request body as JSON. The request body immediately follows the request headers. This
                            is the part of a request that contains any additional data that you want to send to your web
                            server as the HTTP request body, such as data from a form.

                            Only the first 8 KB (8192 bytes) of the request body are forwarded to WAF for inspection by the underlying host service.
                            For information about how to handle oversized request bodies, see the JsonBody object configuration.

                            * MatchPattern (*dict*):
                                The patterns to look for in the JSON body. WAF inspects the results of these pattern matches against the rule inspection criteria.

                                * All (*dict, Optional*):
                                    Match all of the elements. See also MatchScope in ``JsonBody``. You must specify either this
                                    setting or the ``IncludedPaths`` setting, but not both.
                                * IncludedPaths (*dict, Optional*):
                                    Match only the specified include paths. See also ``MatchScope`` in JsonBody. Provide the include
                                    paths using JSON Pointer syntax. For example, "``IncludedPaths": ["/dogs/0/name", "/dogs/1/name"]``.
                                    For information about this syntax, see the Internet Engineering Task Force (IETF) documentation
                                    JavaScript Object Notation (JSON) Pointer.
                                    You must specify either this setting or the ``All`` setting, but not both.

                                    .. note::
                                        Don't use this option to include all paths. Instead, use the ``All`` setting.
                            * MatchScope (*str*):
                                The parts of the JSON to match against using the ``MatchPattern``. If you specify ``All``, WAF matches
                                against keys and values.
                            * InvalidFallbackBehavior (*str, Optional*):
                                What WAF should do if it fails to completely parse the JSON body. The options are the following:

                                * ``EVALUATE_AS_STRING``:
                                    Inspect the body as plain text. WAF applies the text transformations and
                                    inspection criteria that you defined for the JSON inspection to the body text string.
                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.
                            * OversizeHandling (*str, Optional*)
                                What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting
                                the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes).
                                Only the first 8 KB of the request body are forwarded to WAF by the underlying host service.
                                The options for oversize handling are the following:

                                * ``CONTINUE``:
                                    Inspect the body normally, according to the rule inspection criteria.
                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.

                                You can combine the ``MATCH`` or ``NO_MATCH`` settings for oversize handling with your rule and web ACL action
                                settings, so that you block any request whose body is over 8 KB.
                        * Headers (*dict, Optional*):
                            Inspect the request headers. You must configure scope and pattern matching filters in the
                            Headers object, to define the set of headers to and the parts of the headers that WAF inspects.
                            Only the first 8 KB (8192 bytes) of a request's headers and only the first 200 headers are
                            forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                            any oversize header content in the Headers object. WAF applies the pattern matching filters to
                            the headers that it receives from the underlying host service.

                            * MatchPattern (*dict*):
                                The filter to use to identify the subset of headers to inspect in a web request.
                                You must specify exactly one setting: either ``All``, ``IncludedHeaders``, or ``ExcludedHeaders``.

                                * All (*dict, Optional*):
                                    Inspect all headers.
                                * IncludedHeaders (*list, Optional*):
                                    Inspect only the headers that have a key that matches one of the strings specified here.
                                * ExcludedHeaders (*list, Optional*):
                                    Inspect only the headers whose keys don't match any of the strings specified here.
                            * MatchScope (*str*):
                                The parts of the headers to match with the rule inspection criteria. If you specify ``All``, WAF
                                inspects both keys and values.
                            * OversizeHandling (*str, Optional*)
                                What WAF should do if the headers of the request are larger than WAF can inspect. WAF does not
                                support inspecting the entire contents of request headers when they exceed 8 KB (8192 bytes) or
                                200 total headers. The underlying host service forwards a maximum of 200 headers and at most 8 KB
                                of header contents to WAF.

                                * ``CONTINUE``:
                                    Inspect the headers normally, according to the rule inspection criteria.
                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.

                        * Cookies (*dict, Optional*):
                            Inspect the request cookies. You must configure scope and pattern matching filters in the
                            ``Cookies`` object, to define the set of cookies and the parts of the cookies that WAF inspects.
                            Only the first 8 KB (8192 bytes) of a request's cookies and only the first 200 cookies are
                            forwarded to WAF for inspection by the underlying host service. You must configure how to handle
                            any oversize cookie content in the Cookies object. WAF applies the pattern matching filters to
                            the cookies that it receives from the underlying host service.

                            * MatchPattern (*dict*):
                                The filter to use to identify the subset of cookies to inspect in a web request.
                                You must specify exactly one setting: either ``All``, ``IncludedCookies``, or ``ExcludedCookies``.

                                * All (*dict, Optional*):
                                    Inspect all cookies.
                                * IncludedCookies (*list, Optional*):
                                    Inspect only the cookies that have a key that matches one of the strings specified here.
                                * ExcludedCookies (*list, Optional*):
                                    Inspect only the cookies whose keys don't match any of the strings specified here.
                            * MatchScope (*str*):
                                The parts of the cookies to inspect with the rule inspection criteria. If you specify ``All``, WAF
                                inspects both keys and values.
                            * OversizeHandling (*str, Optional*)
                                What WAF should do if the cookies of the request are larger than WAF can inspect. WAF does not support
                                inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies.
                                The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to WAF.

                                * ``CONTINUE``:
                                    Inspect the cookies normally, according to the rule inspection criteria.
                                * ``MATCH``:
                                    Treat the web request as matching the rule statement. WAF applies the rule action to the request.
                                * ``NO_MATCH``:
                                    Treat the web request as not matching the rule statement.

                    * TextTransformations (*list*):
                        Text transformations eliminate some of the unusual formatting that attackers use in web requests
                        in an effort to bypass detection. If you specify one or more transformations in a rule
                        statement, WAF performs all transformations on the content of the request component identified
                        by ``FieldToMatch``, starting from the lowest priority setting, before inspecting the content for a
                        match.

                        * Priority (*int*):
                            Sets the relative processing order for multiple transformations that are defined for a rule
                            statement. WAF processes all transformations, from lowest priority to highest, before inspecting
                            the transformed content. The priorities don't need to be consecutive, but they must all be
                            different.
                        * Type (*str*):
                            You can specify the following transformation types:

                            * ``BASE64_DECODE``:
                                Decode a Base64-encoded string.
                            * ``BASE64_DECODE_EXT``:
                                Decode a Base64-encoded string, but use a forgiving implementation that ignores characters that aren't valid.
                            * ``CMD_LINE``:
                                Command-line transformations. These are helpful in reducing effectiveness of
                                attackers who inject an operating system command-line command and use unusual formatting to
                                disguise some or all of the command.

                                * Delete the following characters: ``\`` ``"`` ``'`` ``^``
                                * Delete spaces before the following characters: ``/`` ``(``
                                * Replace the following characters with a space: ``,`` ``;``
                                * Replace multiple spaces with one space
                                * Convert uppercase letters (A-Z) to lowercase (a-z)
                            * ``COMPRESS_WHITE_SPACE``:
                                Replace these characters with a space character (decimal 32):

                                * ``\f``, formfeed, decimal 12
                                * ``\t``, tab, decimal 9
                                * ``\n``, newline, decimal 10
                                * ``\r``, carriage return, decimal 13
                                * ``\v``, vertical tab, decimal 11
                                * Non-breaking space, decimal 160

                                ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.
                            * ``CSS_DECODE``:
                                Decode characters that were encoded using CSS 2.x escape rules ``syndata.html#characters``.
                                This function uses up to two bytes in the decoding process, so it can help to uncover ASCII
                                characters that were encoded using CSS encoding that wouldn't typically be encoded.
                                It's also useful in countering evasion, which is a combination of a backslash and non-hexadecimal
                                characters. For example, ``ja\vascript`` for ``javascript``.

                            * ``ESCAPE_SEQ_DECODE``:
                                Decode the following ANSI C escape sequences: ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``, ``\v``, ``\\``, ``\?``, ``\'``, ``\"``, ``\xHH`` (hexadecimal), ``\0OOO`` (octal).
                                Encodings that aren't valid remain in the output.
                            * ``HEX_DECODE``:
                                Decode a string of hexadecimal characters into a binary.
                            * ``HTML_ENTITY_DECODE``:
                                Replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs these operations:

                                * Replaces ``(ampersand)quot;`` with ``"``
                                * Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
                                * Replaces ``(ampersand)lt;`` with a "less than" symbol
                                * Replaces ``(ampersand)gt;`` with ``>``
                                * Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;``, with the corresponding characters
                                * Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;``, with the corresponding characters
                            * ``JS_DECODE``:
                                Decode JavaScript escape sequences. If a ``\ u HHHH`` code is in the full-width ASCII code range of ``FF01-FF5E``,
                                then the higher byte is used to detect and adjust the lower byte. If not, only the lower byte is used and the
                                higher byte is zeroed, causing a possible loss of information.
                            * ``LOWERCASE``:
                                Convert uppercase letters (A-Z) to lowercase (a-z).
                            * ``MD5``:
                                Calculate an MD5 hash from the data in the input. The computed hash is in a raw binary form.
                            * ``NONE``:
                                Specify ``NONE`` if you don't want any text transformations.
                            * ``NORMALIZE_PATH``:
                                Remove multiple slashes, directory self-references, and directory back-references that are not at the
                                beginning of the input from an input string.
                            * ``NORMALIZE_PATH_WIN``:
                                This is the same as ``NORMALIZE_PATH``, but first converts backslash characters to forward slashes.
                            * ``REMOVE_NULLS``:
                                Remove all NULL bytes from the input.
                            * ``REPLACE_COMMENTS``:
                                Replace each occurrence of a C-style comment (``/* ... */``) with a single space. Multiple consecutive
                                occurrences are not compressed. Unterminated comments are also replaced with a space (ASCII ``0x20``).
                                However, a standalone termination of a comment (``*/``) is not acted upon.
                            * ``REPLACE_NULLS``:
                                Replace NULL bytes in the input with space characters (ASCII ``0x20``).
                            * ``SQL_HEX_DECODE``:
                                Decode SQL hex data. Example (``0x414243``) will be decoded to (``ABC``).
                            * ``URL_DECODE``:
                                Decode a URL-encoded value.
                            * ``URL_DECODE_UNI``:
                                Like ``URL_DECODE``, but with support for Microsoft-specific ``%u`` encoding. If the code is in the full-width
                                ASCII code range of ``FF01-FF5E``, the higher byte is used to detect and adjust the lower byte. Otherwise,
                                only the lower byte is used and the higher byte is zeroed.
                            * ``UTF8_TO_UNICODE``:
                                Convert all UTF-8 character sequences to Unicode. This helps input normalization, and minimizing false-positives
                                and false-negatives for non-English languages.
            * Action (*dict, Optional*):
                The action that WAF should take on a web request when it matches the rule statement. Settings at the web ACL level can override
                the rule action setting.

                This is used only for rules whose statements do not reference a rule group. Rule statements that reference a rule group include
                ``RuleGroupReferenceStatement`` and ``ManagedRuleGroupStatement``.

                You must specify either this ``Action`` setting or the rule ``OverrideAction`` setting, but not both:

                If the rule statement does not reference a rule group, use this rule action setting and not the rule override action setting.
                If the rule statement references a rule group, use the override action setting and not this action setting.

                * Block (*dict, Optional*):
                    Instructs WAF to block the web request.

                    * CustomResponse (*dict, Optional*):
                        Defines a custom response for the web request.

                        * ResponseCode (*int*):
                            The HTTP status code to return to the client. For a list of status codes that you can use in
                            your custom reqponses, see Supported status codes for custom response in the WAF Developer
                            Guide.
                        * CustomResponseBodyKey (*str, Optional*):
                            References the response body that you want WAF to return to the web request client. You can
                            define a custom response for a rule action or a default web ACL action that is set to block. To
                            do this, you first define the response body key and value in the ``CustomResponseBodies`` setting
                            for the WebACL or RuleGroup where you want to use it. Then, in the rule action or web ACL
                            default action BlockAction setting, you reference the response body using this key.
                        * ResponseHeaders (*list, Optional*):
                            The HTTP headers to use in the response. Duplicate header names are not allowed. For
                            information about the limits on count and size for custom request and response settings, see WAF
                            quotas in the WAF Developer Guide.

                            * (*dict, Optional*):
                                A custom header for custom request and response handling. This is used in CustomResponse and CustomRequestHandling .

                                * Name (*str*):
                                    The name of the custom header. For custom request header insertion, when WAF inserts the header
                                    into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                                    are already in the request. For example, for the header name sample, WAF inserts the header
                                    ``x-amzn-waf-sample``.
                                * Value (*str*):
                                    The value of the custom header.
                * Allow (*dict, Optional*):
                    Instructs WAF to allow the web request.

                    * CustomRequestHandling (*dict, Optional*):
                        Defines custom handling for the web request. For information about customizing web requests and
                        responses, see Customizing web requests and responses in WAF in the WAF Developer Guide.

                        * InsertHeaders (*list*):
                            The HTTP headers to insert into the request. Duplicate header names are not allowed.  For
                            information about the limits on count and size for custom request and response settings, see WAF
                            quotas in the WAF Developer Guide.

                            * (*dict, Optional*):
                                A custom header for custom request and response handling. This is used in CustomResponse and CustomRequestHandling .

                                * Name (*str*):
                                    The name of the custom header. For custom request header insertion, when WAF inserts the header
                                    into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                                    are already in the request. For example, for the header name sample, WAF inserts the header
                                    ``x-amzn-waf-sample``.
                                * Value (*str*):
                                    The value of the custom header.
                * Count (*dict, Optional*):
                    Instructs WAF to count the web request and allow it.

                    * CustomRequestHandling (*dict, Optional*):
                        Defines custom handling for the web request. For information about customizing web requests and
                        responses, see Customizing web requests and responses in WAF in the WAF Developer Guide.

                        * InsertHeaders (*list*):
                            The HTTP headers to insert into the request. Duplicate header names are not allowed.  For
                            information about the limits on count and size for custom request and response settings, see WAF
                            quotas in the WAF Developer Guide.

                            * (*dict, Optional*):
                                A custom header for custom request and response handling. This is used in CustomResponse and CustomRequestHandling .

                                * Name (*str*):
                                    The name of the custom header. For custom request header insertion, when WAF inserts the header
                                    into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                                    are already in the request. For example, for the header name sample, WAF inserts the header
                                    ``x-amzn-waf-sample``.
                                * Value (*str*):
                                    The value of the custom header.
                * Captcha (*dict, Optional*):
                    Instructs WAF to run a ``CAPTCHA`` check against the web request.

                    * CustomRequestHandling (*dict, Optional*):
                        Defines custom handling for the web request. For information about customizing web requests and
                        responses, see Customizing web requests and responses in WAF in the WAF Developer Guide.

                        * InsertHeaders (*list*):
                            The HTTP headers to insert into the request. Duplicate header names are not allowed.  For
                            information about the limits on count and size for custom request and response settings, see WAF
                            quotas in the WAF Developer Guide.

                            * (*dict, Optional*):
                                A custom header for custom request and response handling. This is used in CustomResponse and CustomRequestHandling .

                                * Name (*str*):
                                    The name of the custom header. For custom request header insertion, when WAF inserts the header
                                    into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                                    are already in the request. For example, for the header name sample, WAF inserts the header
                                    ``x-amzn-waf-sample``.
                                * Value (*str*):
                                    The value of the custom header.
            * OverrideAction (*dict, Optional*):
                The action to use in the place of the action that results from the rule group evaluation. Set
                the override action to none to leave the result of the rule group alone. Set it to count to
                override the result to count only.

                You can only use this for rule statements that reference a rule group, like ``RuleGroupReferenceStatement``
                and ``ManagedRuleGroupStatement``.

                .. note::
                    This option is usually set to none. It does not affect how the rules in the rule group are evaluated. If you
                    want the rules in the rule group to only count matches, do not use this and instead exclude
                    those rules in your rule group reference statement settings.

                * Count (*dict, Optional*):
                    Override the rule group evaluation result to count only.

                    .. note::
                        This option is usually set to none. It does not affect how the rules in the rule group are evaluated. If you want
                        the rules in the rule group to only count matches, do not use this and instead exclude those rules in your rule
                        group reference statement settings.

                    * CustomRequestHandling (*dict, Optional*):
                        Defines custom handling for the web request. For information about customizing web requests and
                        responses, see Customizing web requests and responses in WAF in the WAF Developer Guide.

                        * InsertHeaders (*list*):
                            The HTTP headers to insert into the request. Duplicate header names are not allowed.  For
                            information about the limits on count and size for custom request and response settings, see WAF
                            quotas in the WAF Developer Guide.

                            * (*dict, Optional*):
                                A custom header for custom request and response handling. This is used in CustomResponse and CustomRequestHandling .

                                * Name (*str*):
                                    The name of the custom header. For custom request header insertion, when WAF inserts the header
                                    into the request, it prefixes this name ``x-amzn-waf-``, to avoid confusion with the headers that
                                    are already in the request. For example, for the header name sample, WAF inserts the header
                                    ``x-amzn-waf-sample``.
                                * Value (*str*):
                                    The value of the custom header.
                * None (*dict, Optional*):
                    Don't override the rule group evaluation result. This is the most common setting.
            * RuleLabels (*dict, Optional*):
                Labels to apply to web requests that match the rule match statement. WAF applies fully qualified labels to matching web requests.
                A fully qualified label is the concatenation of a label namespace and a rule label. The rule's rule group or web ACL defines the
                label namespace.

                Rules that run after this rule in the web ACL can match against these labels using a ``LabelMatchStatement``.

                For each label, provide a case-sensitive string containing optional namespaces and a label name, according to the following guidelines:

                * Separate each component of the label with a colon.
                * Each namespace or name can have up to 128 characters.
                * You can specify up to 5 namespaces in a label.
                * Don't use the following reserved words in your label specification: ``aws``, ``waf``, ``managed``, ``rulegroup``, ``webacl``, ``regexpatternset``, or ``ipset``.

                For example, ``myLabelName`` or ``nameSpace1:nameSpace2:myLabelName``.

                * (*dict, Optional*):
                    * Name (*str*):
                        The label string.
            * VisibilityConfig (*dict*):
                Defines and enables Amazon CloudWatch metrics and web request sample collection.

                * SampledRequestsEnabled (*bool*):
                    A boolean indicating whether WAF should store a sampling of the web requests that match the rules. You can view the sampled
                    requests through the WAF console.
                * CloudWatchMetricsEnabled (*bool*):
                    A boolean indicating whether the associated resource sends metrics to Amazon CloudWatch. For the list of available metrics,
                    see WAF Metrics.
                * MetricName (*str*):
                    A name of the Amazon CloudWatch metric. The name can contain only the characters: ``A-Z``, ``a-z``, ``0-9``,
                    ``-`` (hyphen), and ``_`` (underscore). The name can be from one to 128 characters long. It can't
                    contain whitespace or metric names reserved for WAF, for example ``All`` and ``Default_Action``.
            * CaptchaConfig (*dict, Optional*):
                Specifies how WAF should handle ``CAPTCHA`` evaluations. If you don't specify this, WAF uses the ``CAPTCHA`` configuration
                that's defined for the web ACL.

                * ImmunityTimeProperty (*dict, Optional*):
                    Determines how long a CAPTCHA token remains valid after the client successfully solves a ``CAPTCHA`` puzzle.

                    * ImmunityTime (*int*):
                        The amount of time, in seconds, that a CAPTCHA token is valid. The default setting is 300.
        custom_response_bodies(dict, Optional):
            A map of custom response keys and content bodies. When you create a rule with a block action, you can send a custom response to the
            web request. You define these for the web ACL, and then use them in the rules and default actions that you define in the web ACL.

            * (*dict*):
                The response body to use in a custom response to a web request. This is referenced by key from CustomResponse CustomResponseBodyKey .

                * ContentType (*str*):
                    The type of content in the payload that you are defining in the Content string.
                * Content (*str*):
                    The payload of the custom response. You can use JSON escape strings in JSON content. To do this, you must specify JSON content in
                    the ContentType setting.
        captcha_config(dict, Optional):
            Specifies how WAF should handle ``CAPTCHA`` evaluations for rules that don't have their own ``CaptchaConfig`` settings.
            If you don't specify this, WAF uses its default settings for ``CaptchaConfig``.

            * ImmunityTimeProperty (*dict, Optional*):
                Determines how long a ``CAPTCHA`` token remains valid after the client successfully solves a ``CAPTCHA`` puzzle.

                * ImmunityTime (*int*):
                    The amount of time, in seconds, that a ``CAPTCHA`` token is valid. The default setting is ``300``.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the web ACL.

            * Key (*str*):
                The key identifier, or name, of the tag.
            * Value (*str*):
                The string value that's associated with the key of the tag.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_wafv2_web_acl]:
          aws.wafv2.web_acl.present:
            - name: 'string'
            - resource_id: 'string'
            - scope: 'CLOUDFRONT|REGIONAL'
            - default_action:
                Block:
                  CustomResponse:
                    ResponseCode: int
                    CustomResponseBodyKey: 'string'
                    ResponseHeaders:
                      - Name: 'string'
                        Value: 'string'
                Allow:
                  CustomRequestHandling:
                    InsertHeaders:
                      - Name: 'string'
                        Value: 'string'
            - visibility_config:
                SampledRequestsEnabled: True|False
                CloudWatchMetricsEnabled: True|False
                MetricName: 'string'
            - description: 'string'
            - rules:
                - Name: 'string'
                  Priority: int
                  Statement:
                    ByteMatchStatement:
                      SearchString: 'string'
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                            IncludedPaths:
                              - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                      PositionalConstraint: 'EXACTLY|STARTS_WITH|ENDS_WITH|CONTAINS|CONTAINS_WORD'
                    SqliMatchStatement:
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                              IncludedPaths:
                                - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                      SensitivityLevel: 'LOW|HIGH'
                    XssMatchStatement:
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                              IncludedPaths:
                                - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                    SizeConstraintStatement:
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                              IncludedPaths:
                                - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      ComparisonOperator: 'EQ|NE|LE|LT|GE|GT'
                      Size: int
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                    GeoMatchStatement:
                      CountryCodes:
                        - 'AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BQ|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CW|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SX|SK|SI|SB|SO|ZA|GS|SS|ES|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW|XK'
                      ForwardedIPConfig:
                        HeaderName: 'string'
                        FallbackBehavior: 'MATCH|NO_MATCH'
                    RuleGroupReferenceStatement:
                      ARN: 'string'
                      ExcludedRules:
                        - 'Name': 'string'
                    IPSetReferenceStatement:
                      ARN: 'string'
                      IPSetForwardedIPConfig:
                        HeaderName: 'string'
                        FallbackBehavior: 'MATCH|NO_MATCH'
                        Position: 'FIRST|LAST|ANY'
                    RegexPatternSetReferenceStatement:
                      ARN: 'string'
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                              IncludedPaths:
                                - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                    RateBasedStatement:
                      Limit: int
                      AggregateKeyType: 'IP|FORWARDED_IP'
                      ScopeDownStatement: '... recursive ...'
                      ForwardedIPConfig:
                        HeaderName: 'string'
                        FallbackBehavior: 'MATCH|NO_MATCH'
                    AndStatement:
                      Statements:
                        - '... recursive ...'
                    OrStatement:
                      Statements:
                        - '... recursive ...'
                    NotStatement:
                      Statement: '... recursive ...'
                    ManagedRuleGroupStatement:
                      VendorName: 'string'
                      Name: 'string'
                      Version: 'string'
                      ExcludedRules:
                        - Name: 'string'
                      ScopeDownStatement: '... recursive ...'
                      ManagedRuleGroupConfigs:
                        - LoginPath: 'string'
                          PayloadType: 'JSON|FORM_ENCODED'
                          UsernameField:
                            Identifier: 'string'
                          PasswordField:
                            Identifier: 'string'
                    LabelMatchStatement:
                      Scope: 'LABEL|NAMESPACE'
                      Key: 'string'
                    RegexMatchStatement:
                      RegexString: 'string'
                      FieldToMatch:
                        SingleHeader:
                          Name: 'string'
                        SingleQueryArgument:
                          Name: 'string'
                        AllQueryArguments:
                        UriPath:
                        QueryString:
                        Body:
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Method:
                        JsonBody:
                          MatchPattern:
                            All:
                              IncludedPaths:
                                - 'string'
                            MatchScope: 'ALL|KEY|VALUE'
                            InvalidFallbackBehavior: 'MATCH|NO_MATCH|EVALUATE_AS_STRING'
                            OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Headers:
                          MatchPattern:
                            All:
                            IncludedHeaders:
                              - 'string'
                            ExcludedHeaders:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                        Cookies:
                          MatchPattern:
                            All:
                            IncludedCookies:
                              - 'string'
                            ExcludedCookies:
                              - 'string'
                          MatchScope: 'ALL|KEY|VALUE'
                          OversizeHandling: 'CONTINUE|MATCH|NO_MATCH'
                      TextTransformations:
                        - Priority: int
                          Type: 'NONE|COMPRESS_WHITE_SPACE|HTML_ENTITY_DECODE|LOWERCASE|CMD_LINE|URL_DECODE|BASE64_DECODE|HEX_DECODE|MD5|REPLACE_COMMENTS|ESCAPE_SEQ_DECODE|SQL_HEX_DECODE|CSS_DECODE|JS_DECODE|NORMALIZE_PATH|NORMALIZE_PATH_WIN|REMOVE_NULLS|REPLACE_NULLS|BASE64_DECODE_EXT|URL_DECODE_UNI|UTF8_TO_UNICODE'
                  Action:
                    Block:
                      CustomResponse:
                        ResponseCode: int
                        CustomResponseBodyKey: 'string'
                        ResponseHeaders:
                          - Name: 'string'
                            Value: 'string'
                    Allow:
                      CustomRequestHandling:
                        InsertHeaders:
                          Name: 'string'
                          Value: 'string'
                    Count:
                      CustomRequestHandling:
                        InsertHeaders:
                          Name: 'string'
                          Value: 'string'
                    Captcha:
                      CustomRequestHandling:
                        InsertHeaders:
                          Name: 'string'
                          Value: 'string'
                  OverrideAction:
                    Count:
                      CustomRequestHandling:
                        InsertHeaders:
                          Name: 'string'
                          Value: 'string'
                    None:
                  RuleLabels:
                    - Name: 'string'
                  VisibilityConfig:
                    SampledRequestsEnabled: True|False
                    CloudWatchMetricsEnabled: True|False
                    MetricName: 'string'
                  CaptchaConfig:
                    ImmunityTimeProperty:
                      ImmunityTime: int
            - custom_response_bodies:
                'string':
                    ContentType: 'TEXT_PLAIN|TEXT_HTML|APPLICATION_JSON'
                    Content: 'string'
            - captcha_config:
                ImmunityTimeProperty:
                    ImmunityTime: int
            - tags:
              - Key: 'string'
                Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_wafv2_web_acl:
              aws.wafv2.web_acl.present:
                - name: 'idem_test_web_acl'
                - scope: 'REGIONAL'
                - default_action:
                    Allow:
                      CustomRequestHandling:
                        InsertHeaders:
                          - Name: 'idem-test-header-name'
                            Value: 'idem-test-header-value'
                - visibility_config:
                    SampledRequestsEnabled: False
                    CloudWatchMetricsEnabled: True
                    MetricName: 'idem-test-metric'
                - description: 'My WAFv2 Web ACL'
                - rules:
                  - Name: 'AWS-AWSManagedRulesBotControlRuleSet'
                    Priority: 1
                    Statement:
                      ManagedRuleGroupStatement:
                        Name: 'AWSManagedRulesBotControlRuleSet'
                        VendorName: 'AWS'
                    Action:
                      OverrideAction:
                        None:
                    VisibilityConfig:
                      SampledRequestsEnabled: False
                      CloudWatchMetricsEnabled: True
                      MetricName: 'idem-test-metric'
                - tags:
                  - Key: 'provider'
                    Value: 'idem'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    lock_token: str = None
    resource_updated: bool = False
    tags_list = None
    tags_dict = None
    if tags is not None:
        if isinstance(tags, Dict):
            tags_list = hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            tags_dict = tags
        else:
            tags_list = tags
            tags_dict = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    resource_parameters = {
        "Name": name,
        "DefaultAction": default_action,
        "VisibilityConfig": visibility_config,
        "Description": description,
        "Rules": rules,
        "CustomResponseBodies": custom_response_bodies,
        "CaptchaConfig": captcha_config,
        "Tags": tags_list,
    }

    if resource_id:
        ret = await hub.exec.boto3.client.wafv2.get_web_acl(
            ctx, Name=name, Scope=scope, Id=resource_id
        )
        if ret["result"]:
            before = ret["ret"]["WebACL"]
            lock_token = ret["ret"]["LockToken"]

    if before:
        convert_ret = await hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_to_present_async(
            ctx, raw_resource=before, idem_resource_name=name, scope=scope
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
        result["old_state"] = convert_ret["ret"]
        plan_state = copy.deepcopy(result["old_state"])

        # Update web acl
        update_ret = await hub.tool.aws.wafv2.web_acl.update(
            ctx,
            name=name,
            raw_resource=before,
            resource_parameters=resource_parameters,
            scope=scope,
            resource_id=resource_id,
            lock_token=lock_token,
        )
        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])

        if update_ret["ret"] and ctx.get("test", False):
            for key in [
                "scope",
                "default_action",
                "visibility_config",
                "description",
                "rules",
                "custom_response_bodies",
                "captcha_config",
            ]:
                if key in update_ret["ret"]:
                    plan_state[key] = update_ret["ret"][key]
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.wafv2.web_acl", name=name
            )
        if (tags_list is not None) and (
            not hub.tool.aws.state_comparison_utils.are_lists_identical(
                tags_list,
                hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    result["old_state"].get("tags")
                ),
            )
        ):
            # Update tags
            update_tag_ret = await hub.tool.aws.wafv2.tag.update_tags(
                ctx=ctx,
                resource_arn=before.get("ARN"),
                old_tags=result["old_state"].get("tags", {}),
                new_tags=tags_dict,
            )
            result["result"] = result["result"] and update_tag_ret["result"]
            result["comment"] += update_tag_ret["comment"]
            resource_updated = resource_updated or bool(update_tag_ret["ret"])

            if ctx.get("test", False) and update_tag_ret["ret"] is not None:
                plan_state["tags"] = update_tag_ret["ret"]

        if not resource_updated:
            result["comment"] += [f"aws.wafv2.web_acl.present '{name}' already exists."]

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "scope": scope,
                    "default_action": default_action,
                    "visibility_config": visibility_config,
                    "description": description,
                    "rules": rules,
                    "custom_response_bodies": custom_response_bodies,
                    "captcha_config": captcha_config,
                    "tags": tags_dict,
                },
            )
            result["comment"] += [f"Would create aws.wafv2.web_acl {name}"]
            return result

        # Create web acl
        ret = await hub.exec.boto3.client.wafv2.create_web_acl(
            ctx, Scope=scope, **resource_parameters
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] += ret["comment"]
            return result
        result["comment"] += [f"Created '{name}'"]
        resource_id = ret["ret"]["Summary"]["Id"]

    if ctx.get("test", False):
        result["new_state"] = plan_state

    elif (not before) or resource_updated:
        resource_ret = await hub.exec.boto3.client.wafv2.get_web_acl(
            ctx, Name=name, Scope=scope, Id=resource_id
        )
        if not result["result"]:
            result["comment"] += ret["comment"]
            return result
        after = resource_ret["ret"]["WebACL"]

        convert_ret = await hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_to_present_async(
            ctx, raw_resource=after, idem_resource_name=name, scope=scope
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
        result["new_state"] = convert_ret["ret"]

    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(
    hub, ctx, name: str, scope: str, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes the specified web ACL.

    .. warning::
        Before deleting any web ACL, first disassociate it from all resources.

    Args:
        name(str):
            The name of the web ACL.
        scope(str):
            Specifies whether this is for an Amazon CloudFront distribution (``CLOUDFRONT``) or for a regional application (``REGIONAL``).
        resource_id(str, Optional):
            The ID of the web ACL in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_wafv2_web_acl]:
          aws.wafv2.web_acl.absent:
            - name: 'string'
            - resource_id: 'string'
            - scope: 'CLOUDFRONT|REGIONAL'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_wafv2_web_acl:
              aws.wafv2.web_acl.absent:
                - name: 'idem_test_web_acl'
                - resource_id: '12345678-1234-1234-1234-123456789012'
                - scope: 'REGIONAL'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    lock_token: str = None

    if resource_id:
        resource = await hub.exec.boto3.client.wafv2.get_web_acl(
            ctx, Name=name, Scope=scope, Id=resource_id
        )
        if resource["result"]:
            before = resource["ret"]["WebACL"]
            lock_token = resource["ret"]["LockToken"]

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            "aws.wafv2.web_acl", name
        )

    elif ctx.get("test", False):
        convert_ret = await hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_to_present_async(
            ctx, raw_resource=before, idem_resource_name=name, scope=scope
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
            return result
        result["old_state"] = convert_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            "aws.wafv2.web_acl", name
        )
        return result

    else:
        convert_ret = await hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_to_present_async(
            ctx, raw_resource=before, idem_resource_name=name, scope=scope
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
            return result
        result["old_state"] = convert_ret["ret"]

        # Delete web acl
        ret = await hub.exec.boto3.client.wafv2.delete_web_acl(
            ctx, Name=name, Scope=scope, Id=resource_id, LockToken=lock_token
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            "aws.wafv2.web_acl", name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS WAF v2 web ACLs in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.wafv2.web_acl
    """
    result = {}
    scope = ["CLOUDFRONT", "REGIONAL"]

    for web_acl_scope in scope:
        ret = await hub.exec.boto3.client.wafv2.list_web_acls(ctx, Scope=web_acl_scope)
        if not ret["result"]:
            hub.log.warning(f"Could not describe web acl {ret['comment']}")
            continue

        for resource in ret["ret"]["WebACLs"]:
            web_acl_name = resource["Name"]
            resource_id = resource["Id"]
            raw_resource = await hub.exec.boto3.client.wafv2.get_web_acl(
                ctx, Name=web_acl_name, Id=resource_id, Scope=web_acl_scope
            )
            if not raw_resource["result"]:
                hub.log.warning(
                    f"Could not get web acl '{web_acl_name}' with error {convert_ret['comment']}"
                )
                continue
            resource_ret = raw_resource["ret"]["WebACL"]
            convert_ret = await hub.tool.aws.wafv2.conversion_utils.convert_raw_web_acl_to_present_async(
                ctx,
                raw_resource=resource_ret,
                idem_resource_name=web_acl_name,
                scope=web_acl_scope,
            )
            if not convert_ret["result"]:
                hub.log.warning(
                    f"Could not describe web acl '{web_acl_name}' with error {convert_ret['comment']}"
                )
                continue
            translated_resource = convert_ret["ret"]
            result[translated_resource["resource_id"]] = {
                "aws.wafv2.web_acl.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in translated_resource.items()
                ]
            }

    return result
