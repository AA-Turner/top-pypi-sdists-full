"""State module for managing Amazon Cloudfront Distribution."""
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
    origins: make_dataclass(
        "Origins",
        [
            ("Quantity", int),
            (
                "Items",
                List[
                    make_dataclass(
                        "Origin",
                        [
                            ("Id", str),
                            ("DomainName", str),
                            ("OriginPath", str, field(default=None)),
                            (
                                "CustomHeaders",
                                make_dataclass(
                                    "CustomHeaders",
                                    [
                                        ("Quantity", int),
                                        (
                                            "Items",
                                            List[
                                                make_dataclass(
                                                    "OriginCustomHeader",
                                                    [
                                                        ("HeaderName", str),
                                                        ("HeaderValue", str),
                                                    ],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "S3OriginConfig",
                                make_dataclass(
                                    "S3OriginConfig", [("OriginAccessIdentity", str)]
                                ),
                                field(default=None),
                            ),
                            (
                                "CustomOriginConfig",
                                make_dataclass(
                                    "CustomOriginConfig",
                                    [
                                        ("HTTPPort", int),
                                        ("HTTPSPort", int),
                                        ("OriginProtocolPolicy", str),
                                        (
                                            "OriginSslProtocols",
                                            make_dataclass(
                                                "OriginSslProtocols",
                                                [
                                                    ("Quantity", int),
                                                    ("Items", List[str]),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        ("OriginReadTimeout", int, field(default=None)),
                                        (
                                            "OriginKeepaliveTimeout",
                                            int,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("ConnectionAttempts", int, field(default=None)),
                            ("ConnectionTimeout", int, field(default=None)),
                            (
                                "OriginShield",
                                make_dataclass(
                                    "OriginShield",
                                    [
                                        ("Enabled", bool),
                                        (
                                            "OriginShieldRegion",
                                            str,
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
            ),
        ],
    ),
    default_cache_behaviour: make_dataclass(
        "DefaultCacheBehavior",
        [
            ("TargetOriginId", str),
            ("ViewerProtocolPolicy", str),
            (
                "TrustedSigners",
                make_dataclass(
                    "TrustedSigners",
                    [
                        ("Enabled", bool),
                        ("Quantity", int),
                        ("Items", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "TrustedKeyGroups",
                make_dataclass(
                    "TrustedKeyGroups",
                    [
                        ("Enabled", bool),
                        ("Quantity", int),
                        ("Items", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "AllowedMethods",
                make_dataclass(
                    "AllowedMethods",
                    [
                        ("Quantity", int),
                        ("Items", List[str]),
                        (
                            "CachedMethods",
                            make_dataclass(
                                "CachedMethods",
                                [("Quantity", int), ("Items", List[str])],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            ("SmoothStreaming", bool, field(default=None)),
            ("Compress", bool, field(default=None)),
            (
                "LambdaFunctionAssociations",
                make_dataclass(
                    "LambdaFunctionAssociations",
                    [
                        ("Quantity", int),
                        (
                            "Items",
                            List[
                                make_dataclass(
                                    "LambdaFunctionAssociation",
                                    [
                                        ("LambdaFunctionARN", str),
                                        ("EventType", str),
                                        ("IncludeBody", bool, field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "FunctionAssociations",
                make_dataclass(
                    "FunctionAssociations",
                    [
                        ("Quantity", int),
                        (
                            "Items",
                            List[
                                make_dataclass(
                                    "FunctionAssociation",
                                    [("FunctionARN", str), ("EventType", str)],
                                )
                            ],
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            ("FieldLevelEncryptionId", str, field(default=None)),
            ("RealtimeLogConfigArn", str, field(default=None)),
            ("CachePolicyId", str, field(default=None)),
            ("OriginRequestPolicyId", str, field(default=None)),
            ("ResponseHeadersPolicyId", str, field(default=None)),
            (
                "ForwardedValues",
                make_dataclass(
                    "ForwardedValues",
                    [
                        ("QueryString", bool),
                        (
                            "Cookies",
                            make_dataclass(
                                "CookiePreference",
                                [
                                    ("Forward", str),
                                    (
                                        "WhitelistedNames",
                                        make_dataclass(
                                            "CookieNames",
                                            [
                                                ("Quantity", int),
                                                (
                                                    "Items",
                                                    List[str],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                        ),
                        (
                            "Headers",
                            make_dataclass(
                                "Headers",
                                [
                                    ("Quantity", int),
                                    ("Items", List[str], field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "QueryStringCacheKeys",
                            make_dataclass(
                                "QueryStringCacheKeys",
                                [
                                    ("Quantity", int),
                                    ("Items", List[str], field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            ("MinTTL", int, field(default=None)),
            ("DefaultTTL", int, field(default=None)),
            ("MaxTTL", int, field(default=None)),
        ],
    ),
    enabled: bool,
    comment: str = "",
    caller_reference: str = "",
    logging: make_dataclass(
        "LoggingConfig",
        [("Enabled", bool), ("IncludeCookies", bool), ("Bucket", str), ("Prefix", str)],
    ) = None,
    viewer_certificate: make_dataclass(
        "ViewerCertificate",
        [
            ("CloudFrontDefaultCertificate", bool, field(default=None)),
            ("IAMCertificateId", str, field(default=None)),
            ("ACMCertificateArn", str, field(default=None)),
            ("SSLSupportMethod", str, field(default=None)),
            ("MinimumProtocolVersion", str, field(default=None)),
            ("Certificate", str, field(default=None)),
            ("CertificateSource", str, field(default=None)),
        ],
    ) = None,
    aliases: make_dataclass(
        "Aliases", [("Quantity", int), ("Items", List[str], field(default=None))]
    ) = None,
    price_class: str = None,
    default_root_object: str = None,
    origin_groups: make_dataclass(
        "OriginGroups",
        [
            ("Quantity", int),
            (
                "Items",
                List[
                    make_dataclass(
                        "OriginGroup",
                        [
                            ("Id", str),
                            (
                                "FailoverCriteria",
                                make_dataclass(
                                    "OriginGroupFailoverCriteria",
                                    [
                                        (
                                            "StatusCodes",
                                            make_dataclass(
                                                "StatusCodes",
                                                [
                                                    ("Quantity", int),
                                                    ("Items", List[int]),
                                                ],
                                            ),
                                        )
                                    ],
                                ),
                            ),
                            (
                                "Members",
                                make_dataclass(
                                    "OriginGroupMembers",
                                    [
                                        ("Quantity", int),
                                        (
                                            "Items",
                                            List[
                                                make_dataclass(
                                                    "OriginGroupMember",
                                                    [("OriginId", str)],
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    cache_behaviors: make_dataclass(
        "CacheBehaviors",
        [
            ("Quantity", int),
            (
                "Items",
                List[
                    make_dataclass(
                        "CacheBehavior",
                        [
                            ("PathPattern", str),
                            ("TargetOriginId", str),
                            ("ViewerProtocolPolicy", str),
                            (
                                "TrustedSigners",
                                make_dataclass(
                                    "TrustedSigners",
                                    [
                                        ("Enabled", bool),
                                        ("Quantity", int),
                                        ("Items", List[str], field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "TrustedKeyGroups",
                                make_dataclass(
                                    "TrustedKeyGroups",
                                    [
                                        ("Enabled", bool),
                                        ("Quantity", int),
                                        ("Items", List[str], field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "AllowedMethods",
                                make_dataclass(
                                    "AllowedMethods",
                                    [
                                        ("Quantity", int),
                                        ("Items", List[str]),
                                        (
                                            "CachedMethods",
                                            make_dataclass(
                                                "CachedMethods",
                                                [
                                                    ("Quantity", int),
                                                    ("Items", List[str]),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("SmoothStreaming", bool, field(default=None)),
                            ("Compress", bool, field(default=None)),
                            (
                                "LambdaFunctionAssociations",
                                make_dataclass(
                                    "LambdaFunctionAssociations",
                                    [
                                        ("Quantity", int),
                                        (
                                            "Items",
                                            List[
                                                make_dataclass(
                                                    "LambdaFunctionAssociation",
                                                    [
                                                        ("LambdaFunctionARN", str),
                                                        ("EventType", str),
                                                        (
                                                            "IncludeBody",
                                                            bool,
                                                            field(default=None),
                                                        ),
                                                    ],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "FunctionAssociations",
                                make_dataclass(
                                    "FunctionAssociations",
                                    [
                                        ("Quantity", int),
                                        (
                                            "Items",
                                            List[
                                                make_dataclass(
                                                    "FunctionAssociation",
                                                    [
                                                        ("FunctionARN", str),
                                                        ("EventType", str),
                                                    ],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("FieldLevelEncryptionId", str, field(default=None)),
                            ("RealtimeLogConfigArn", str, field(default=None)),
                            ("CachePolicyId", str, field(default=None)),
                            ("OriginRequestPolicyId", str, field(default=None)),
                            ("ResponseHeadersPolicyId", str, field(default=None)),
                            (
                                "ForwardedValues",
                                make_dataclass(
                                    "ForwardedValues",
                                    [
                                        ("QueryString", bool),
                                        (
                                            "Cookies",
                                            make_dataclass(
                                                "CookiePreference",
                                                [
                                                    ("Forward", str),
                                                    (
                                                        "WhitelistedNames",
                                                        make_dataclass(
                                                            "CookieNames",
                                                            [
                                                                ("Quantity", int),
                                                                (
                                                                    "Items",
                                                                    List[str],
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                        ),
                                        (
                                            "Headers",
                                            make_dataclass(
                                                "Headers",
                                                [
                                                    ("Quantity", int),
                                                    (
                                                        "Items",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        (
                                            "QueryStringCacheKeys",
                                            make_dataclass(
                                                "QueryStringCacheKeys",
                                                [
                                                    ("Quantity", int),
                                                    (
                                                        "Items",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("MinTTL", int, field(default=None)),
                            ("DefaultTTL", int, field(default=None)),
                            ("MaxTTL", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    custom_error_responses: make_dataclass(
        "CustomErrorResponses",
        [
            ("Quantity", int),
            (
                "Items",
                List[
                    make_dataclass(
                        "CustomErrorResponse",
                        [
                            ("ErrorCode", int),
                            ("ResponsePagePath", str, field(default=None)),
                            ("ResponseCode", str, field(default=None)),
                            ("ErrorCachingMinTTL", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    restrictions: make_dataclass(
        "Restrictions",
        [
            (
                "GeoRestriction",
                make_dataclass(
                    "GeoRestriction",
                    [
                        ("RestrictionType", str),
                        ("Quantity", int),
                        ("Items", List[str], field(default=None)),
                    ],
                ),
            )
        ],
    ) = None,
    web_acl_id: str = None,
    http_version: str = None,
    is_ipv6_enabled: bool = True,
    resource_id: str = None,
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=60)),
                        ("max_attempts", int, field(default=35)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=60)),
                        ("max_attempts", int, field(default=35)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates a new web distribution.

    You create a CloudFront distribution to tell CloudFront where you want content
    to be delivered from, and the details about how to track and manage content delivery. Send a POST request to the
    /CloudFront API version/distribution/distribution ID resource.

    .. Warning::
        When you update a distribution, there are more
        required fields than when you create a distribution. When you update your distribution by using
        UpdateDistribution, follow the steps included in the documentation to get the current configuration and then
        make your updates. This helps to make sure that you include all the required fields. To view a summary, see
        Required Fields for Create Distribution and Update Distribution in the Amazon CloudFront Developer Guide.

    Args:
        name(str):
            An Idem name of the resource.

        caller_reference (str, Optional):
            A unique value (for example, a date-time stamp) that ensures that the request can't be replayed.

            If the value of CallerReference is new (regardless of the content of the DistributionConfig
            object), CloudFront creates a new distribution.

            If CallerReference is a value that you already sent in a previous request to create a distribution,
            CloudFront returns a DistributionAlreadyExists error.

        resource_id(str, Optional):
            AWS cloudfront distribution ID.

        aliases(dict, Optional):
            A complex type that contains information about CNAME (alternate domain names),
            if any, for this distribution.

            * Quantity (int):
              The number of CNAME aliases, if any, that you want to associate with this distribution.
            * Items (list[str], Optional):
              A complex type that contains the CNAME aliases, if any, that you want to associate with this

        default_root_object (str, Optional):
            The object that you want CloudFront to request from your origin (for example, index.html) when a
            viewer requests the root URL for your distribution (http://www.example.com) instead of an object
            in your distribution (http://www.example.com/product-description.html).
            Specifying a default root object avoids exposing the contents of your distribution.

            Specify only the object name, for example, index.html. Don't add a / before the object name.

            If you don't want to specify a default root object when you create a distribution,
            include an empty DefaultRootObject element.

            To delete the default root object from an existing distribution, update the distribution
            configuration and include an empty DefaultRootObject element.

            To replace the default root object, update the distribution configuration and specify the new object.

            For more information about the default root object, see Creating a Default Root Object in the
            Amazon CloudFront Developer Guide.

        origins(dict):
            A complex type that contains information about origins for this distribution.
                * Quantity (int): The number of origins for this distribution.
                * Items (list[dict[str, Any]]): A list of origins.
                    * Id (str): A unique identifier for the origin. This value must be unique within the distribution.
                      Use this value to specify the TargetOriginId in a CacheBehavior or DefaultCacheBehavior.
                    * DomainName (str): The domain name for the origin.
                      For more information, see Origin Domain Name in the Amazon CloudFront Developer Guide.
                    * OriginPath (str, Optional):
                      An optional path that CloudFront appends to the origin domain name when CloudFront requests
                      content from the origin. For more information, see Origin Path in the Amazon CloudFront
                      Developer Guide.
                    * CustomHeaders (dict[str, Any], Optional):
                      A list of HTTP header names and values that CloudFront adds to the requests that it sends to the
                      origin.

                      For more information, see Adding Custom Headers to Origin Requests in the Amazon
                      CloudFront Developer Guide.

                      * Quantity (int): The number of custom headers, if any, for this distribution.
                      * Items (list[dict[str, Any]], Optional):
                          Optional: A list that contains one OriginCustomHeader element for each custom header that you
                          want CloudFront to forward to the origin. If Quantity is 0, omit Items.

                          * HeaderName (str): The name of a header that you want CloudFront to send to your origin.
                            For more information, see Adding Custom Headers to Origin Requests in the  Amazon
                            CloudFront Developer Guide.
                          * HeaderValue (str): The value for the header that you specified in the HeaderName field.

                    * S3OriginConfig (dict[str, Any], Optional):
                      Use this type to specify an origin that is an Amazon S3 bucket that is not configured with
                      static website hosting. To specify any other type of origin, including an Amazon S3 bucket that
                      is configured with static website hosting, use the CustomOriginConfig type instead.

                      * OriginAccessIdentity (str):
                        The CloudFront origin access identity to associate with the origin. Use an origin access
                        identity to configure the origin so that viewers can only access objects in an Amazon S3 bucket
                        through CloudFront. The format of the value is:

                        origin-access-identity/cloudfront/ID-of-origin-access-identity
                        where  ID-of-origin-access-identity  is the value that CloudFront returned in
                        the ID element when you created the origin access identity.

                        If you want viewers to be able to access objects using either the CloudFront URL or
                        the Amazon S3 URL, specify an empty OriginAccessIdentity element.

                        To delete the origin access identity from an existing distribution, update the distribution
                        configuration and include an empty OriginAccessIdentity element.

                        To replace the origin access identity, update the distribution configuration and
                        specify the new origin access identity.

                        For more information about the origin access identity,
                        see Serving Private Content through CloudFront in the Amazon CloudFront Developer Guide.

                    * CustomOriginConfig (dict[str, Any], Optional):
                      Use this type to specify an origin that is not an Amazon S3 bucket, with one exception. If the
                      Amazon S3 bucket is configured with static website hosting, use this type. If the Amazon S3
                      bucket is not configured with static website hosting, use the S3OriginConfig type instead.

                      * HTTPPort (int):
                        The HTTP port that CloudFront uses to connect to the origin. Specify the HTTP port that the
                        origin listens on.
                      * HTTPSPort (int):
                        The HTTPS port that CloudFront uses to connect to the origin. Specify the HTTPS port that the
                        origin listens on.
                      * OriginProtocolPolicy (str):
                        Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Valid
                        values are:

                        * http-only – CloudFront always uses HTTP to connect to the origin.
                        * match-viewer –
                          CloudFront connects to the origin using the same protocol that the viewer used to
                          connect to CloudFront.
                        * https-only – CloudFront always uses HTTPS to connect to the origin.

                      * OriginSslProtocols (dict[str, Any], Optional):
                        Specifies the minimum SSL/TLS protocol that CloudFront uses when connecting to your
                        origin over HTTPS. Valid values include SSLv3, TLSv1, TLSv1.1, and TLSv1.2.

                        For more information, see Minimum Origin SSL Protocol in the Amazon CloudFront Developer Guide.

                        * Quantity (int): The number of SSL/TLS protocols that you want to allow CloudFront to use
                          when establishing an HTTPS connection with this origin.
                        * Items (list[str]): A list that contains allowed SSL/TLS protocols for this distribution.

                      * OriginReadTimeout (int, Optional):
                        Specifies how long, in seconds, CloudFront waits for a response from the origin. This is also
                        known as the origin response timeout. The minimum timeout is 1 second, the maximum is 60
                        seconds, and the default (if you don’t specify otherwise) is 30 seconds.

                        For more information, see Origin Response Timeout in the Amazon CloudFront Developer Guide.

                      * OriginKeepaliveTimeout (int, Optional):
                        Specifies how long, in seconds, CloudFront persists its connection to the origin. The minimum
                        timeout is 1 second, the maximum is 60 seconds, and the default
                        (if you don’t specify otherwise) is 5 seconds.

                        For more information, see Origin Keep-alive Timeout in the Amazon CloudFront Developer Guide.

                    * ConnectionAttempts (int, Optional):
                      The number of times that CloudFront attempts to connect to the origin. The minimum number is 1,
                      the maximum is 3, and the default (if you don’t specify otherwise) is 3.

                      For a custom origin (including an Amazon S3 bucket that’s configured with static website hosting),
                      this value also specifies the number of times that CloudFront attempts to get a response from
                      the origin, in the case of an Origin Response Timeout.

                      For more information, see Origin Connection Attempts in the Amazon CloudFront Developer Guide.

                    * ConnectionTimeout (int, Optional):
                      The number of seconds that CloudFront waits when trying to establish a connection to the origin.
                      The minimum timeout is 1 second, the maximum is 10 seconds, and the default (if you don’t
                      specify otherwise) is 10 seconds.

                      For more information, see Origin Connection Timeout in the Amazon CloudFront Developer Guide.

                    * OriginShield (dict[str, Any], Optional):
                      CloudFront Origin Shield. Using Origin Shield can help reduce the load on your origin.

                      For more information, see Using Origin Shield in the Amazon CloudFront Developer Guide.

                      * Enabled (bool): A flag that specifies whether Origin Shield is enabled.

                        When it’s enabled, CloudFront routes all requests through Origin Shield,
                        which can help protect your origin. When it’s disabled, CloudFront might send requests directly
                        to your origin from multiple edge locations or regional edge caches.
                      * OriginShieldRegion (str, Optional): The Amazon Web Services Region for Origin Shield.

                        Specify the Amazon Web Services Region that has the lowest latency to your origin.
                        To specify a region, use the region code, not the region name.
                        For example, specify the US East (Ohio) region as us-east-2.

                        When you enable CloudFront
                        Origin Shield, you must specify the Amazon Web Services Region for Origin Shield. For the list
                        of Amazon Web Services Regions that you can specify, and for help choosing the best Region for
                        your origin, see Choosing the Amazon Web Services Region for Origin Shield in the Amazon
                        CloudFront Developer Guide.

        origin_groups (dict, Optional):
            A complex type that contains information about origin groups for this distribution.

            * Quantity (int): The number of origin groups.
            * Items (list[Dict[str, Any]], Optional):
              The items (origin groups) in a distribution.

              * Id (str): The origin group's ID.
              * FailoverCriteria (dict[str, Any]):
                A complex type that contains information about the failover criteria for an origin group.

                * StatusCodes (dict[str, Any]):
                  The status codes that, when returned from the primary origin, will trigger CloudFront to
                  failover to the second origin.

                  * Quantity (int): The number of status codes.
                  * Items (list[int]): The items (status codes) for an origin group.

              * Members (dict[str, Any]): A complex type that contains information about the origins in an origin group.

                * Quantity (int): The number of origins in an origin group.
                * Items (list[dict[str, Any]]): Items (origins) in an origin group.

                  * OriginId (str): The ID for an origin in an origin group.

        default_cache_behaviour(dict):
            A complex type that describes the default cache behavior if you don't specify a CacheBehavior
            element or if files don't match any of the values of PathPattern in CacheBehavior elements. You
            must create exactly one default cache behavior.

            * TargetOriginId (str):
              The value of ID for the origin that you want CloudFront to route requests to when they use the
              default cache behavior.
            * TrustedSigners (dict[str, Any], Optional):
              AWS recommend using TrustedKeyGroups instead of TrustedSigners.

              A list of Amazon Web Services account IDs whose public keys CloudFront can use to validate signed
              URLs or signed cookies.

              When a cache behavior contains trusted signers, CloudFront requires signed URLs or signed cookies for
              all requests that match the cache behavior. The URLs or cookies must be signed with the private
              key of a CloudFront key pair in a trusted signer’s Amazon Web Services account. The signed URL
              or cookie contains information about which public key CloudFront should use to verify the
              signature. For more information, see Serving private content in the Amazon CloudFront Developer Guide.

              * Enabled (bool):
                This field is true if any of the Amazon Web Services accounts have public keys that CloudFront
                can use to verify the signatures of signed URLs and signed cookies. If not, this field is false.
              * Quantity (int): The number of Amazon Web Services accounts in the list.
              * Items (list[str], Optional): A list of Amazon Web Services account identifiers.

            * TrustedKeyGroups (dict[str, Any], Optional):
              A list of key groups that CloudFront can use to validate signed URLs or signed cookies.

              When a cache behavior contains trusted key groups, CloudFront requires signed URLs or signed cookies
              for all requests that match the cache behavior. The URLs or cookies must be signed with a
              private key whose corresponding public key is in the key group. The signed URL or cookie
              contains information about which public key CloudFront should use to verify the signature. For
              more information, see Serving private content in the Amazon CloudFront Developer Guide.

              * Enabled (bool):
                This field is true if any of the key groups in the list have public keys that CloudFront can use
                to verify the signatures of signed URLs and signed cookies. If not, this field is false.
              * Quantity (int): The number of key groups in the list.
              * Items (list[str], Optional): A list of key groups identifiers.

            * ViewerProtocolPolicy (str):
              The protocol that viewers can use to access the files in the origin specified by TargetOriginId
              when a request matches the path pattern in PathPattern. You can specify the following options:

              * allow-all: Viewers can use HTTP or HTTPS.
              * redirect-to-https: If a viewer submits an HTTP request, CloudFront returns an HTTP status code of 301
                (Moved Permanently) to the viewer along with the HTTPS URL.
                The viewer then resubmits the request using the new URL.
              * https-only:
                If a viewer sends an HTTP request, CloudFront returns an HTTP status code of 403 (Forbidden).

              For more information about requiring the HTTPS protocol, see Requiring HTTPS Between Viewers and
              CloudFront in the Amazon CloudFront Developer Guide.

              .. Note::
                  The only way to guarantee that viewers
                  retrieve an object that was fetched from the origin using HTTPS is never to use any other
                  protocol to fetch the object. If you have recently changed from HTTP to HTTPS, we recommend that
                  you clear your objects’ cache because cached objects are protocol agnostic. That means that an
                  edge location will return an object from the cache regardless of whether the current request
                  protocol matches the protocol used previously. For more information, see Managing Cache
                  Expiration in the Amazon CloudFront Developer Guide.

            * AllowedMethods (dict[str, Any], Optional):
              A complex type that controls which HTTP methods CloudFront processes and forwards to your Amazon
              S3 bucket or your custom origin. There are three choices:
              * CloudFront forwards only GET and HEAD requests.
              * CloudFront forwards only GET, HEAD, and OPTIONS requests.
              * CloudFront forwards GET, HEAD, OPTIONS, PUT, PATCH, POST, and DELETE requests.

              If you pick the third choice, you may need to restrict access to your Amazon S3 bucket or to your custom
              origin so users can't perform operations that you don't want them to. For example, you might not want
              users to have permissions to delete objects from your origin.

              * Quantity (int):
                The number of HTTP methods that you want CloudFront to forward to your origin. Valid values are
                2 (for GET and HEAD requests), 3 (for GET, HEAD, and OPTIONS requests) and 7 (for GET, HEAD,
                OPTIONS, PUT, PATCH, POST, and DELETE requests).
              * Items (list[str]):
                A complex type that contains the HTTP methods that you want CloudFront to process and forward to
                your origin.
              * CachedMethods (dict[str, Any], Optional):
                A complex type that controls whether CloudFront caches the response to requests using the
                specified HTTP methods. There are two choices:
                * CloudFront caches responses to GET and HEAD requests.
                * CloudFront caches responses to GET, HEAD, and OPTIONS requests.
                If you pick the second choice for your Amazon S3 Origin, you may need to forward
                Access-Control-Request-Method, Access-Control-Request-Headers, and Origin headers for the responses to
                be cached correctly.

                * Quantity (int):
                  The number of HTTP methods for which you want CloudFront to cache responses. Valid values are 2
                  (for caching responses to GET and HEAD requests) and 3 (for caching responses to GET, HEAD, and
                  OPTIONS requests).
                * Items (list[str]):
                  A complex type that contains the HTTP methods that you want CloudFront to cache responses to.

            * SmoothStreaming (bool, Optional):
              Indicates whether you want to distribute media files in the Microsoft Smooth Streaming format
              using the origin that is associated with this cache behavior. If so, specify true; if not,
              specify false. If you specify true for SmoothStreaming, you can still distribute other content
              using this cache behavior if the content matches the value of PathPattern.

            * Compress (bool, Optional):
              Whether you want CloudFront to automatically compress certain files for this cache behavior. If
              so, specify true; if not, specify false. For more information, see Serving Compressed Files in
              the Amazon CloudFront Developer Guide.

            * LambdaFunctionAssociations (dict[str, Any], Optional):
              A complex type that contains zero or more Lambda@Edge function associations for a cache behavior.

              * Quantity (int): The number of Lambda@Edge function associations for this cache behavior.
              * Items (list[dict[str, Any]], Optional):
                A complex type that contains LambdaFunctionAssociation items for this cache behavior.
                If Quantity is 0, you can omit Items.

                * LambdaFunctionARN (str):
                  The ARN of the Lambda@Edge function. You must specify the ARN of a function version; you can't
                  specify an alias or $LATEST.

                * EventType (str):
                  Specifies the event type that triggers a Lambda@Edge function invocation. You can specify the
                  following values:

                  * viewer-request: The function executes when CloudFront receives a request
                    from a viewer and before it checks to see whether the requested object is in the edge cache.
                  * origin-request: The function executes only when CloudFront sends a request to your origin. When
                    the requested object is in the edge cache, the function doesn't execute.
                  * origin-response: The function executes after CloudFront receives a response from the origin and
                    before it caches the object in the response. When the requested object is in the edge cache,
                    the function doesn't execute.
                  * viewer-response: The function executes before CloudFront returns the requested
                    object to the viewer. The function executes regardless of whether the object was already in the
                    edge cache. If the origin returns an HTTP status code other than HTTP 200 (OK), the function
                    doesn't execute.

                * IncludeBody (bool, Optional):
                  A flag that allows a Lambda@Edge function to have read access to the body content. For more
                  information, see Accessing the Request Body by Choosing the Include Body Option in the Amazon
                  CloudFront Developer Guide.

            * FunctionAssociations (dict[str, Any], Optional):
              A list of CloudFront functions that are associated with this cache behavior. CloudFront
              functions must be published to the LIVE stage to associate them with a cache behavior.

              * Quantity (int): The number of CloudFront functions in the list.
              * Items (list[dict[str, Any]], Optional):
                The CloudFront functions that are associated with a cache behavior in a CloudFront distribution.
                CloudFront functions must be published to the LIVE stage to associate them with a cache behavior.

                * FunctionARN (str): The Amazon Resource Name (ARN) of the function.
                * EventType (str): The event type of the function, either viewer-request or viewer-response.
                  You cannot use origin-facing event types (origin-request and origin-response)
                  with a CloudFront function.

            * FieldLevelEncryptionId (str, Optional):
              The value of ID for the field-level encryption configuration that you want CloudFront to use for
              encrypting specific fields of data for the default cache behavior.

            * RealtimeLogConfigArn (str, Optional):
              The Amazon Resource Name (ARN) of the real-time log configuration that is attached to this cache
              behavior. For more information, see Real-time logs in the Amazon CloudFront Developer Guide.

            * CachePolicyId (str, Optional):
              The unique identifier of the cache policy that is attached to the default cache behavior. For
              more information, see Creating cache policies or Using the managed cache policies in the Amazon
              CloudFront Developer Guide.

              A DefaultCacheBehavior must include either a CachePolicyId or ForwardedValues.
              We recommend that you use a CachePolicyId.

            * OriginRequestPolicyId (str, Optional):
              The unique identifier of the origin request policy that is attached to the default cache
              behavior. For more information, see Creating origin request policies or Using the managed origin
              request policies in the Amazon CloudFront Developer Guide.

            * ResponseHeadersPolicyId (str, Optional): The identifier for a response headers policy.

            * ForwardedValues (dict[str, Any], Optional):
              This field is deprecated. We recommend that you use a cache policy or an origin request policy
              instead of this field. For more information, see Working with policies in the Amazon CloudFront
              Developer Guide.

              If you want to include values in the cache key, use a cache policy. For more
              information, see Creating cache policies or Using the managed cache policies in the Amazon
              CloudFront Developer Guide.

              If you want to send values to the origin but not include them in the
              cache key, use an origin request policy. For more information, see Creating origin request
              policies or Using the managed origin request policies in the Amazon CloudFront Developer Guide.

              A DefaultCacheBehavior must include either a CachePolicyId or ForwardedValues. We recommend that
              you use a CachePolicyId. A complex type that specifies how CloudFront handles query strings,
              cookies, and HTTP headers.

              * QueryString (bool):
                This field is deprecated. We recommend that you use a cache policy or an origin request policy
                instead of this field.

                If you want to include query strings in the cache key, use a cache
                policy. For more information, see Creating cache policies in the Amazon CloudFront Developer Guide.

                If you want to send query strings to the origin but not include them in the cache key,
                use an origin request policy. For more information, see Creating origin request policies in the
                Amazon CloudFront Developer Guide.

                Indicates whether you want CloudFront to forward query
                strings to the origin that is associated with this cache behavior and cache based on the query
                string parameters. CloudFront behavior depends on the value of QueryString and on the values
                that you specify for QueryStringCacheKeys, if any:

                If you specify true for QueryString and you
                don't specify any values for QueryStringCacheKeys, CloudFront forwards all query string
                parameters to the origin and caches based on all query string parameters. Depending on how many
                query string parameters and values you have, this can adversely affect performance because
                CloudFront must forward more requests to the origin.

                If you specify true for QueryString and you
                specify one or more values for QueryStringCacheKeys, CloudFront forwards all query string
                parameters to the origin, but it only caches based on the query string parameters that you
                specify.

                If you specify false for QueryString, CloudFront doesn't forward any query string
                parameters to the origin, and doesn't cache based on query string parameters.

                For more information, see Configuring CloudFront to Cache Based on Query String Parameters in
                the Amazon CloudFront Developer Guide.

              * Cookies (dict[str, Any]):
                This field is deprecated. We recommend that you use a cache policy or an origin request policy
                instead of this field.

                If you want to include cookies in the cache key, use a cache policy. For
                more information, see Creating cache policies in the Amazon CloudFront Developer Guide.

                If you want to send cookies to the origin but not include them in the cache key, use an origin request
                policy. For more information, see Creating origin request policies in the Amazon CloudFront
                Developer Guide.

                A complex type that specifies whether you want CloudFront to forward cookies to
                the origin and, if so, which ones. For more information about forwarding cookies to the origin,
                see How CloudFront Forwards, Caches, and Logs Cookies in the Amazon CloudFront Developer Guide.

                * Forward (str):
                  This field is deprecated. We recommend that you use a cache policy or an origin request policy
                  instead of this field.

                  If you want to include cookies in the cache key, use a cache policy. For
                  more information, see Creating cache policies in the Amazon CloudFront Developer Guide.

                  If you want to send cookies to the origin but not include them in the cache key, use origin request
                  policy. For more information, see Creating origin request policies in the Amazon CloudFront
                  Developer Guide.

                  Specifies which cookies to forward to the origin for this cache behavior: all,
                  none, or the list of cookies specified in the WhitelistedNames complex type.

                  Amazon S3 doesn't  process cookies. When the cache behavior is forwarding requests to an
                  Amazon S3 origin, specify none for the Forward element.

                * WhitelistedNames (dict[str, Any], Optional):
                  This field is deprecated. We recommend that you use a cache policy or an origin request policy
                  instead of this field.

                  If you want to include cookies in the cache key, use a cache policy. For
                  more information, see Creating cache policies in the Amazon CloudFront Developer Guide.

                  If you want to send cookies to the origin but not include them in the cache key, use an origin request
                  policy. For more information, see Creating origin request policies in the Amazon CloudFront
                  Developer Guide.

                  Required if you specify whitelist for the value of Forward. A complex type that
                  specifies how many different cookies you want CloudFront to forward to the origin for this cache
                  behavior and, if you want to forward selected cookies, the names of those cookies.

                  If you specify all or none for the value of Forward, omit WhitelistedNames. If you change the value of
                  Forward from whitelist to all or none and you don't delete the WhitelistedNames element and its
                  child elements, CloudFront deletes them automatically.

                  For the current limit on the number of cookie names that you can whitelist for each cache behavior,
                  see  CloudFront Limits in the Amazon Web Services General Reference.

                  * Quantity (int): The number of cookie names in the Items list.
                  * Items (list[str], Optional): A list of cookie names.

                * Headers (dict[str, Any], Optional):
                  This field is deprecated. We recommend that you use a cache policy or an origin request policy
                  instead of this field.

                  If you want to include headers in the cache key, use a cache policy. For
                  more information, see Creating cache policies in the Amazon CloudFront Developer Guide.

                  If you want to send headers to the origin but not include them in the cache key, use an origin request
                  policy. For more information, see Creating origin request policies in the Amazon CloudFront
                  Developer Guide.

                  A complex type that specifies the Headers, if any, that you want CloudFront to
                  forward to the origin for this cache behavior (whitelisted headers). For the headers that you
                  specify, CloudFront also caches separate versions of a specified object that is based on the
                  header values in viewer requests.

                  For more information, see  Caching Content Based on Request Headers in the Amazon CloudFront Developer Guide.

                  * Quantity (int): The number of header names in the Items list.
                  * Items (list[str], Optional): A list of HTTP header names.

                * QueryStringCacheKeys (dict[str, Any], Optional):
                  This field is deprecated. We recommend that you use a cache policy or an origin request policy
                  instead of this field.

                  If you want to include query strings in the cache key, use a cache
                  policy. For more information, see Creating cache policies in the Amazon CloudFront Developer
                  Guide.

                  If you want to send query strings to the origin but not include them in the cache key,
                  use an origin request policy. For more information, see Creating origin request policies in the
                  Amazon CloudFront Developer Guide.

                  A complex type that contains information about the query
                  string parameters that you want CloudFront to use for caching for this cache behavior.

                  * Quantity (int): The number of whitelisted query string parameters for a cache behavior.
                  * Items (list[str], Optional):
                    A list that contains the query string parameters that you want CloudFront to use as a basis for
                    caching for a cache behavior. If Quantity is 0, you can omit Items.

            * MinTTL (int, Optional):
              This field is deprecated. We recommend that you use the MinTTL field in a cache policy instead
              of this field. For more information, see Creating cache policies or Using the managed cache
              policies in the Amazon CloudFront Developer Guide.

              The minimum amount of time that you want
              objects to stay in CloudFront caches before CloudFront forwards another request to your origin
              to determine whether the object has been updated. For more information, see Managing How Long
              Content Stays in an Edge Cache (Expiration) in the Amazon CloudFront Developer Guide.

              You must specify 0 for MinTTL if you configure CloudFront to forward all headers to your origin (under
              Headers, if you specify 1 for Quantity and * for Name).

            * DefaultTTL (int, Optional):
              This field is deprecated. We recommend that you use the DefaultTTL field in a cache policy
              instead of this field. For more information, see Creating cache policies or Using the managed
              cache policies in the Amazon CloudFront Developer Guide.

              The default amount of time that you
              want objects to stay in CloudFront caches before CloudFront forwards another request to your
              origin to determine whether the object has been updated. The value that you specify applies only
              when your origin does not add HTTP headers such as Cache-Control max-age, Cache-Control
              s-maxage, and Expires to objects. For more information, see Managing How Long Content Stays in
              an Edge Cache (Expiration) in the Amazon CloudFront Developer Guide.

            * MaxTTL (int, Optional):
              This field is deprecated. We recommend that you use the MaxTTL field in a cache policy instead
              of this field. For more information, see Creating cache policies or Using the managed cache
              policies in the Amazon CloudFront Developer Guide.

              The maximum amount of time that you want
              objects to stay in CloudFront caches before CloudFront forwards another request to your origin
              to determine whether the object has been updated. The value that you specify applies only when
              your origin adds HTTP headers such as Cache-Control max-age, Cache-Control s-maxage, and Expires
              to objects. For more information, see Managing How Long Content Stays in an Edge Cache
              (Expiration) in the Amazon CloudFront Developer Guide.

        cache_behaviors(dict, Optional):
            A complex type that contains zero or more CacheBehavior elements.

            * Quantity (int): The number of cache behaviors for this distribution.
            * Items (list[dict[str, Any]], Optional):
              A complex type that contains cache behaviors for this distribution. If Quantity is 0, you can omit Items.

              * PathPattern (str):
                The pattern (for example, images/*.jpg) that specifies which requests to apply the behavior to.
                When CloudFront receives a viewer request, the requested path is compared with path patterns in
                the order in which cache behaviors are listed in the distribution.

                You can optionally include a slash (/) at the beginning of the path pattern. For example, /images/*.jpg.
                CloudFront behavior is the same with or without the leading /.

                The path pattern for the default cache behavior is * and cannot be changed. If the request for an object
                does not match the path pattern for any cache behaviors, CloudFront applies the behavior in the
                default cache behavior.

                For more information, see Path Pattern in the  Amazon CloudFront Developer Guide.

              * TargetOriginId (str):
                The value of ID for the origin that you want CloudFront to route requests to when they match
                this cache behavior.

              * TrustedSigners ('TrustedSigners', Optional):
                AWS recommend using TrustedKeyGroups instead of TrustedSigners.

                A list of Amazon Web Services account IDs whose public keys CloudFront can use to validate signed URLs
                or signed cookies.

                When a cache behavior contains trusted signers, CloudFront requires signed URLs or signed cookies for
                all requests that match the cache behavior. The URLs or cookies must be signed with the private
                key of a CloudFront key pair in the trusted signer’s Amazon Web Services account. The signed URL
                or cookie contains information about which public key CloudFront should use to verify the
                signature. For more information, see Serving private content in the Amazon CloudFront Developer
                Guide.

              * TrustedKeyGroups ('TrustedKeyGroups', Optional):
                A list of key groups that CloudFront can use to validate signed URLs or signed cookies.

                When a cache behavior contains trusted key groups, CloudFront requires signed URLs or signed cookies
                for all requests that match the cache behavior. The URLs or cookies must be signed with a
                private key whose corresponding public key is in the key group. The signed URL or cookie
                contains information about which public key CloudFront should use to verify the signature. For
                more information, see Serving private content in the Amazon CloudFront Developer Guide.

              * ViewerProtocolPolicy (str):
                The protocol that viewers can use to access the files in the origin specified by TargetOriginId
                when a request matches the path pattern in PathPattern. You can specify the following options:

                * allow-all: Viewers can use HTTP or HTTPS.

                * redirect-to-https: If a viewer submits an HTTP request, CloudFront returns an HTTP status code of
                  301 (Moved Permanently) to the viewer along with the HTTPS URL. The viewer then resubmits the request
                  using the new URL.

                * https-only:
                  If a viewer sends an HTTP request, CloudFront returns an HTTP status code of 403 (Forbidden).

                For more information about requiring the HTTPS protocol, see Requiring HTTPS Between Viewers and
                CloudFront in the Amazon CloudFront Developer Guide.  The only way to guarantee that viewers
                retrieve an object that was fetched from the origin using HTTPS is never to use any other
                protocol to fetch the object. If you have recently changed from HTTP to HTTPS, we recommend that
                you clear your objects’ cache because cached objects are protocol agnostic. That means that an
                edge location will return an object from the cache regardless of whether the current request
                protocol matches the protocol used previously. For more information, see Managing Cache
                Expiration in the Amazon CloudFront Developer Guide.

              * AllowedMethods ('AllowedMethods', Optional):
                A complex type that controls which HTTP methods CloudFront processes and forwards to your Amazon
                S3 bucket or your custom origin. There are three choices:

                * CloudFront forwards only GET and HEAD requests.
                * CloudFront forwards only GET, HEAD, and OPTIONS requests.
                * CloudFront forwards GET, HEAD, OPTIONS, PUT, PATCH, POST, and DELETE requests.

                If you pick the third choice, you may need to restrict access to your Amazon S3 bucket or to your
                custom origin so users can't perform operations that you don't want them to.
                For example, you might not want users to have permissions to delete objects from your origin.

              * SmoothStreaming (bool, Optional):
                Indicates whether you want to distribute media files in the Microsoft Smooth Streaming format
                using the origin that is associated with this cache behavior. If so, specify true; if not,
                specify false. If you specify true for SmoothStreaming, you can still distribute other content
                using this cache behavior if the content matches the value of PathPattern.

              * Compress (bool, Optional):
                Whether you want CloudFront to automatically compress certain files for this cache behavior. If
                so, specify true; if not, specify false. For more information, see Serving Compressed Files in
                the Amazon CloudFront Developer Guide.

              * LambdaFunctionAssociations ('LambdaFunctionAssociations', Optional):
                A complex type that contains zero or more Lambda@Edge function associations for a cache
                behavior.

              * FunctionAssociations ('FunctionAssociations', Optional):
                A list of CloudFront functions that are associated with this cache behavior. CloudFront
                functions must be published to the LIVE stage to associate them with a cache behavior.

              * FieldLevelEncryptionId (str, Optional):
                The value of ID for the field-level encryption configuration that you want CloudFront to use for
                encrypting specific fields of data for this cache behavior.

              * RealtimeLogConfigArn (str, Optional):
                The Amazon Resource Name (ARN) of the real-time log configuration that is attached to this cache
                behavior. For more information, see Real-time logs in the Amazon CloudFront Developer Guide.

              * CachePolicyId (str, Optional):
                The unique identifier of the cache policy that is attached to this cache behavior. For more
                information, see Creating cache policies or Using the managed cache policies in the Amazon
                CloudFront Developer Guide. A CacheBehavior must include either a CachePolicyId or
                ForwardedValues. We recommend that you use a CachePolicyId.

              * OriginRequestPolicyId (str, Optional):
                The unique identifier of the origin request policy that is attached to this cache behavior. For
                more information, see Creating origin request policies or Using the managed origin request
                policies in the Amazon CloudFront Developer Guide.

              * ResponseHeadersPolicyId (str, Optional): The identifier for a response headers policy.

              * ForwardedValues ('ForwardedValues', Optional):
                This field is deprecated. We recommend that you use a cache policy or an origin request policy
                instead of this field. For more information, see Working with policies in the Amazon CloudFront
                Developer Guide.

                If you want to include values in the cache key, use a cache policy. For more
                information, see Creating cache policies or Using the managed cache policies in the Amazon
                CloudFront Developer Guide.

                If you want to send values to the origin but not include them in the
                cache key, use an origin request policy. For more information, see Creating origin request
                policies or Using the managed origin request policies in the Amazon CloudFront Developer Guide.

                A CacheBehavior must include either a CachePolicyId or ForwardedValues. We recommend that you
                use a CachePolicyId.

                A complex type that specifies how CloudFront handles query strings, cookies, and HTTP headers.

              * MinTTL (int, Optional):
                This field is deprecated. We recommend that you use the MinTTL field in a cache policy instead
                of this field. For more information, see Creating cache policies or Using the managed cache
                policies in the Amazon CloudFront Developer Guide.

                The minimum amount of time that you want
                objects to stay in CloudFront caches before CloudFront forwards another request to your origin
                to determine whether the object has been updated. For more information, see  Managing How Long
                Content Stays in an Edge Cache (Expiration) in the  Amazon CloudFront Developer Guide.

                You must specify 0 for MinTTL if you configure CloudFront to forward all headers to your origin (under
                Headers, if you specify 1 for Quantity and * for Name).

              * DefaultTTL (int, Optional):
                This field is deprecated. We recommend that you use the DefaultTTL field in a cache policy
                instead of this field. For more information, see Creating cache policies or Using the managed
                cache policies in the Amazon CloudFront Developer Guide.

                The default amount of time that you
                want objects to stay in CloudFront caches before CloudFront forwards another request to your
                origin to determine whether the object has been updated. The value that you specify applies only
                when your origin does not add HTTP headers such as Cache-Control max-age, Cache-Control
                s-maxage, and Expires to objects. For more information, see Managing How Long Content Stays in
                an Edge Cache (Expiration) in the Amazon CloudFront Developer Guide.

              * MaxTTL (int, Optional):
                This field is deprecated. We recommend that you use the MaxTTL field in
                a cache policy instead of this field. For more information, see Creating cache policies or
                Using the managed cache policies in the Amazon CloudFront Developer Guide.

                The maximum amount of time that you want objects to stay in CloudFront caches before CloudFront
                forwards another request to your origin to determine whether the object has been updated.
                The value that you specify applies only when your origin adds HTTP headers such as
                Cache-Control max-age, Cache-Control s-maxage, and Expires to objects.
                For more information, see Managing How Long Content Stays in an Edge Cache (Expiration) in
                the Amazon CloudFront Developer Guide.

        custom_error_responses(dict, Optional):
            A complex type that controls the following:

            * Whether CloudFront replaces HTTP status codes in
              the 4xx and 5xx range with custom error messages before returning the response to the viewer.
            * How long CloudFront caches HTTP status codes in the 4xx and 5xx range.

            For more information about custom error pages, see Customizing Error Responses in the Amazon CloudFront Developer
            Guide.

            * Quantity (int):
              The number of HTTP status codes for which you want to specify a custom error page and/or a
              caching duration. If Quantity is 0, you can omit Items.

            * Items (list[dict[str, Any]], Optional):
              A complex type that contains a CustomErrorResponse element for each HTTP status code for which
              you want to specify a custom error page and/or a caching duration.

              * ErrorCode (int):
                The HTTP status code for which you want to specify a custom error page and/or a caching
                duration.

              * ResponsePagePath (str, Optional):
                The path to the custom error page that you want CloudFront to return to a viewer when your
                origin returns the HTTP status code specified by ErrorCode, for example, /4xx-
                errors/403-forbidden.html. If you want to store your objects and your custom error pages in
                different locations, your distribution must include a cache behavior for which the following is
                true:

                * The value of PathPattern matches the path to your custom error messages. For example,
                  suppose you saved custom error pages for 4xx errors in an Amazon S3 bucket in a directory named
                  /4xx-errors. Your distribution must include a cache behavior for which the path pattern routes
                  requests for your custom error pages to that location, for example, /4xx-errors/*.

                * The value of TargetOriginId specifies the value of the ID element for the origin that contains
                  your custom error pages.

                If you specify a value for ResponsePagePath, you must also specify a value for
                ResponseCode. We recommend that you store custom error pages in an Amazon S3 bucket. If you
                store custom error pages on an HTTP server and the server starts to return 5xx errors,
                CloudFront can't get the files that you want to return to viewers because the origin server is
                unavailable.

              * ResponseCode (str, Optional):
                The HTTP status code that you want CloudFront to return to the viewer along with the custom
                error page. There are a variety of reasons that you might want CloudFront to return a status
                code different from the status code that your origin returned to CloudFront, for example:

                * Some Internet devices (some firewalls and corporate proxies, for example) intercept HTTP 4xx and 5xx
                  and prevent the response from being returned to the viewer. If you substitute 200, the response
                  typically won't be intercepted.

                * If you don't care about distinguishing among different client
                  errors or server errors, you can specify 400 or 500 as the ResponseCode for all 4xx or 5xx errors.

                * You might want to return a 200 status code (OK) and static website so your customers don't know
                  that your website is down. If you specify a value for ResponseCode, you must also specify
                  a value for ResponsePagePath.

              * ErrorCachingMinTTL (int, Optional):
                The minimum amount of time, in seconds, that you want CloudFront to cache the HTTP status code specified
                in ErrorCode. When this time period has elapsed, CloudFront queries your origin to see whether
                the problem that caused the error has been resolved and the requested object is now available.

                For more information, see Customizing Error Responses in the Amazon CloudFront Developer Guide.

        comment(str, Optional):
                An optional comment to describe the distribution. The comment cannot be longer than 128 characters.

        logging(dict, Optional):
            A complex type that controls whether access logs are written for the distribution.

            For more information about logging, see Access Logs in the Amazon CloudFront Developer Guide.

            * Enabled (bool): Specifies whether you want CloudFront to save access logs to an Amazon S3 bucket.
              If you don't want to enable logging when you create a distribution or if you want to disable logging
              for an existing distribution, specify false for Enabled, and specify empty Bucket and Prefix elements.
              If you specify false for Enabled but you specify values for Bucket, prefix, and IncludeCookies,
              the values are automatically deleted.

            * IncludeCookies (bool): Specifies whether you want CloudFront to include cookies in access logs,
              specify true for IncludeCookies. If you choose to include cookies in logs, CloudFront logs all
              cookies regardless of how you configure the cache behaviors for this distribution.
              If you don't want to include cookies when you create a distribution or if you want to disable include
              cookies for an existing distribution, specify false for IncludeCookies.

            * Bucket (str): The Amazon S3 bucket to store the access logs in,
              for example, myawslogbucket.s3.amazonaws.com.

            * Prefix (str): An optional string that you want CloudFront to prefix to the access log filenames for this
              distribution, for example, myprefix/. If you want to enable logging, but you don't want to
              specify a prefix, you still must include an empty Prefix element in the Logging element.

        price_class (str, Optional):
            The price class that corresponds with the maximum price that you want to pay for CloudFront
            service. If you specify PriceClass_All, CloudFront responds to requests for your objects from
            all CloudFront edge locations.

            If you specify a price class other than PriceClass_All,
            CloudFront serves your objects from the CloudFront edge location that has the lowest latency
            among the edge locations in your price class. Viewers who are in or near regions that are
            excluded from your specified price class may encounter slower performance.

            For more information
            about price classes, see Choosing the Price Class for a CloudFront Distribution in the Amazon
            CloudFront Developer Guide. For information about CloudFront pricing, including how price
            classes (such as Price Class 100) map to CloudFront regions, see Amazon CloudFront Pricing.

        enabled(bool):
            From this field, you can enable or disable the selected distribution.

        viewer_certificate(dict, Optional):
            complex type that determines the distribution’s SSL/TLS configuration for communicating with viewers.

            * CloudFrontDefaultCertificate (bool, Optional):
              If the distribution uses the CloudFront domain name such as d111111abcdef8.cloudfront.net, set
              this field to true. If the distribution uses Aliases (alternate domain names or CNAMEs), set
              this field to false and specify values for the following fields:

              * ACMCertificateArn or IAMCertificateId (specify a value for one, not both)
              * MinimumProtocolVersion
              * SSLSupportMethod

            * IAMCertificateId (str, Optional):
              If the distribution uses Aliases (alternate domain names or CNAMEs) and the SSL/TLS certificate
              is stored in Identity and Access Management (IAM), provide the ID of the IAM certificate.

              If you specify an IAM certificate ID, you must also specify values for MinimumProtocolVersion and
              SSLSupportMethod.

            * ACMCertificateArn (str, Optional):
              If the distribution uses Aliases (alternate domain names or CNAMEs) and the SSL/TLS certificate
              is stored in Certificate Manager (ACM), provide the Amazon Resource Name (ARN) of the ACM
              certificate. CloudFront only supports ACM certificates in the US East (N. Virginia) Region (us-east-1).

              If you specify an ACM certificate ARN, you must also specify values for MinimumProtocolVersion and SSLSupportMethod.

            * SSLSupportMethod (str, Optional):
              If the distribution uses Aliases (alternate domain names or CNAMEs), specify which viewers the
              distribution accepts HTTPS connections from.

              * sni-only – The distribution accepts HTTPS connections from only viewers that support server name
                indication (SNI). This is recommended. Most browsers and clients support SNI.

              * vip – The distribution accepts HTTPS connections from all viewers including those that don’t
                support SNI. This is not recommended, and results in additional monthly charges from CloudFront.

              * static-ip - Do not specify this value unless your distribution has been enabled for this feature by
                the CloudFront team. If you have a use case that requires static IP addresses for a distribution,
                contact CloudFront through the Amazon Web Services Support Center.

              If the distribution uses the CloudFront domain name such as d111111abcdef8.cloudfront.net,
              don’t set a value for this field.

            * MinimumProtocolVersion (str, Optional):
              If the distribution uses Aliases (alternate domain names or CNAMEs), specify the security policy
              that you want CloudFront to use for HTTPS connections with viewers. The security policy
              determines two settings:

              * The minimum SSL/TLS protocol that CloudFront can use to communicate with viewers.
              * The ciphers that CloudFront can use to encrypt the content that it returns to viewers.

              For more information, see Security Policy and Supported Protocols and Ciphers Between Viewers and
              CloudFront in the Amazon CloudFront Developer Guide.

              .. Note::
                  On the CloudFront console, this setting is called Security Policy.

              When you’re using SNI only (you set SSLSupportMethod to sni-only), you must specify TLSv1 or higher.

              If the distribution uses the CloudFront domain name such as d111111abcdef8.cloudfront.net
              (you set CloudFrontDefaultCertificate to true), CloudFront automatically sets the security policy to
              TLSv1 regardless of the value that you set here.

            * Certificate (str, Optional):
              This field is deprecated. Use one of the following fields instead:

              * ACMCertificateArn
              * IAMCertificateId
              * CloudFrontDefaultCertificate

            * CertificateSource (str, Optional):
              This field is deprecated. Use one of the following fields instead:

              * ACMCertificateArn
              * IAMCertificateId
              * CloudFrontDefaultCertificate

        restrictions(dict, Optional):
            A complex type that identifies ways in which you want to restrict distribution of your content.

            * GeoRestriction (dict[str, Any]):
              A complex type that controls the countries in which your content is distributed.
              CloudFront determines the location of your users using MaxMind GeoIP databases.

              * RestrictionType (str): The method that you want to use to restrict distribution of your content
                by country:

                * none: No geo restriction is enabled, meaning access to content is not restricted by client geo location.

                * blacklist: The Location elements specify the countries in which you don't want
                  CloudFront to distribute your content.

                * whitelist: The Location elements specify the countries in which you want CloudFront to
                  distribute your content.

              * Quantity (int): When geo restriction is enabled, this is the number of countries in your whitelist or
                blacklist. Otherwise, when it is not enabled, Quantity is 0, and you can omit Items.

              * Items (list[str], Optional):
                A complex type that contains a Location element for each country in which you want CloudFront
                either to distribute your content (whitelist) or not distribute your content (blacklist).

                The Location element is a two-letter, uppercase country code for a country that you want to include
                in your blacklist or whitelist. Include one Location element for each country.

                CloudFront and MaxMind both use ISO 3166 country codes. For the current list of countries and
                the corresponding codes, see ISO 3166-1-alpha-2 code on the International Organization for
                Standardization website.
                You can also refer to the country list on the CloudFront console, which includes both
                country names and codes.

        web_acl_id (str, Optional):
            A unique identifier that specifies the WAF web ACL, if any, to associate with this distribution.
            To specify a web ACL created using the latest version of WAF, use the ACL ARN, for example
            arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a.
            To specify a web ACL created using WAF Classic, use the ACL ID,
            for example 473e64fd-f30b-4765-81a0-62ad96dd167a.

            WAF is a web application firewall that lets you monitor
            the HTTP and HTTPS requests that are forwarded to CloudFront, and lets you control access to
            your content. Based on conditions that you specify, such as the IP addresses that requests
            originate from or the values of query strings, CloudFront responds to requests either with the
            requested content or with an HTTP 403 status code (Forbidden). You can also configure CloudFront
            to return a custom error page when a request is blocked. For more information about WAF, see the
            WAF Developer Guide.

        http_version(str, Optional):
            Specify the maximum HTTP version that you want viewers to use to communicate with
            CloudFront. The default value for new web distributions is http2. Viewers that don't support
            HTTP/2 automatically use an earlier HTTP version.

            For viewers and CloudFront to use HTTP/2,
            viewers must support TLS 1.2 or later, and must support Server Name Identification (SNI). In
            general, configuring CloudFront to communicate with viewers using HTTP/2 reduces latency. You
            can improve performance by optimizing for HTTP/2. For more information, do an Internet search
            for "http/2 optimization."

        is_ipv6_enabled (bool, Optional):
            If you want CloudFront to respond to IPv6 DNS requests with an IPv6 address for your
            distribution, specify true. If you specify false, CloudFront responds to IPv6 DNS requests with
            the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second
            request, for an IPv4 address for your distribution.

            In general, you should enable IPv6 if you
            have users on IPv6 networks who want to access your content. However, if you're using signed
            URLs or signed cookies to restrict access to your content, and if you're using a custom policy
            that includes the IpAddress parameter to restrict the IP addresses that can access your content,
            don't enable IPv6. If you want to restrict access to some content by IP address and not restrict
            access to other content (or restrict access but not by IP address), you can create two
            distributions. For more information, see Creating a Signed URL Using a Custom Policy in the
            Amazon CloudFront Developer Guide.

            If you're using an Route 53 Amazon Web Services Integration
            alias resource record set to route traffic to your CloudFront distribution, you need to create a
            second alias resource record set when both of the following are true:

            * You enable IPv6 for the distribution
            * You're using alternate domain names in the URLs for your objects
            For more information, see Routing Traffic to an Amazon CloudFront Web Distribution by Using Your Domain
            Name in the Route 53 Amazon Web Services Integration Developer Guide.

            If you created a CNAME resource record set, either with Route 53
            Amazon Web Services Integration or with another DNS
            service, you don't need to make any changes. A CNAME record will route traffic to your
            distribution regardless of the IP address format of the viewer request.

        tags(dict, Optional):
            Dict in the format of {tag-key: tag-value}

        timeout(dict, Optional):
            Timeout configuration for create/update/deletion of AWS IAM Policy.

            * create (dict): Timeout configuration for creating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.
            * update(dict, Optional): Timeout configuration for updating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [distribution-name]:
             aws.cloudfront.distribution.present:
               - name: 'string'
               - resource_id: 'string'
               - caller_reference: 'string'
               - comment: ''
               - origins:
                   Items:
                   - ConnectionAttempts: 'integer'
                     ConnectionTimeout: 'integer'
                     CustomHeaders:
                       Quantity: 'integer'
                     DomainName: 'string'
                     Id: 'string'
                     OriginPath: 'string'
                     OriginShield:
                       Enabled: 'Boolean'
                     S3OriginConfig:
                      OriginAccessIdentity: ''
                   Quantity: 'integer'
               - default_cache_behaviour:
                   AllowedMethods:
                     CachedMethods:
                       Items: 'List'
                       Quantity: 'integer'
                     Items: 'List'
                     Quantity: 'integer'
                   CachePolicyId: 'string'
                   Compress: 'Boolean'
                   FieldLevelEncryptionId: ''
                   FunctionAssociations:
                     Quantity: 'integer'
                   LambdaFunctionAssociations:
                     Quantity: 'integer'
                   SmoothStreaming: 'Boolean'
                   TargetOriginId: 'string'
                   TrustedKeyGroups:
                     Enabled: 'Boolean'
                     Quantity: 'integer'
                   TrustedSigners:
                     Enabled: 'Boolean'
                     Quantity: 'integer'
                   ViewerProtocolPolicy: 'string'
               - enabled: 'Boolean'
               - logging:
                   Enabled: 'Boolean'
                   IncludeCookies: 'Boolean'
                   Bucket: 'string'
                   Prefix: 'string'
               - viewer_certificate:
                   CertificateSource: 'string'
                   CloudFrontDefaultCertificate: 'Boolean'
                   MinimumProtocolVersion: 'string'
                   SSLSupportMethod: 'string'
               - aliases:
                   Quantity: 'integer'
               - price_class: 'string'
               - origin_groups:
                   Quantity: 'integer'
               - cache_behaviors:
                   Quantity: 'integer'
               - custom_error_responses:
                   Quantity: 'integer'
               - restrictions:
                   GeoRestriction:
                     Quantity: 'integer'
                     RestrictionType: 'string'
               - web_acl_id: 'string'
               - http_version: 'string'
               - is_ipv6_enabled: 'Boolean'
               - tags:
                   'string': 'string'
               - timeout:
                 create:
                   delay: 'integer'
                   max_attempts: 'integer'
                 update:
                   delay: 'integer'
                   max_attempts: 'integer'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            E2QWRUHAPOMQZL:
              aws.cloudfront.distribution.present:
              - name: E2QWRUHAPOMQZL
              - resource_id: E2QWRUHAPOMQZL
              - caller_reference: 7c0ca447-479b-48b2-9260-bc7a4de63478
              - comment: ''
              - origins:
                  Items:
                  - ConnectionAttempts: 3
                    ConnectionTimeout: 10
                    CustomHeaders:
                      Quantity: 0
                    DomainName: idem-test-distribution-bucket.s3.us-east-1.amazonaws.com
                    Id: idem-test-distribution-bucket.s3.us-east-1.amazonaws.com
                    OriginPath: ''
                    OriginShield:
                      Enabled: false
                    S3OriginConfig:
                      OriginAccessIdentity: ''
                  Quantity: 1
              - default_cache_behaviour:
                  AllowedMethods:
                    CachedMethods:
                      Items:
                      - HEAD
                      - GET
                      Quantity: 2
                    Items:
                    - HEAD
                    - GET
                    Quantity: 2
                  CachePolicyId: 6583eea-f89d-4fab-e63d-7e88ee58f6
                  Compress: true
                  FieldLevelEncryptionId: ''
                  FunctionAssociations:
                    Quantity: 0
                  LambdaFunctionAssociations:
                    Quantity: 0
                  SmoothStreaming: false
                  TargetOriginId: idem-test-distribution-bucket.s3.us-east-1.amazonaws.com
                  TrustedKeyGroups:
                    Enabled: false
                    Quantity: 0
                  TrustedSigners:
                    Enabled: false
                    Quantity: 0
                  ViewerProtocolPolicy: redirect-to-https
              - enabled: false
              - logging:
                  Enabled: true
                  IncludeCookies: true
                  Bucket: idem-test-distribution-bucket
                  Prefix: distribution
              - viewer_certificate:
                  CertificateSource: cloudfront
                  CloudFrontDefaultCertificate: true
                  MinimumProtocolVersion: TLSv1
                  SSLSupportMethod: vip
              - aliases:
                  Quantity: 0
              - price_class: PriceClass_All
              - origin_groups:
                  Quantity: 0
              - cache_behaviors:
                  Quantity: 0
              - custom_error_responses:
                  Quantity: 0
              - restrictions:
                  GeoRestriction:
                    Quantity: 0
                    RestrictionType: none
              - web_acl_id: ''
              - http_version: http2
              - is_ipv6_enabled: true
              - tags:
                  Name: idem-test
              - timeout:
                  create:
                    delay: 60
                    max_attempts: 35
                  update:
                    delay: 60
                    max_attempts: 35
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    plan_state = None
    if resource_id:
        before = await hub.exec.aws.cloudfront.distribution.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.cloudfront.distribution.update_distribution(
            ctx=ctx,
            name=name,
            before=result["old_state"],
            resource_id=resource_id,
            caller_reference=caller_reference,
            origins=origins,
            default_cache_behaviour=default_cache_behaviour,
            comment=comment,
            logging=logging,
            enabled=enabled,
            viewer_certificate=viewer_certificate,
            aliases=aliases,
            price_class=price_class,
            default_root_object=default_root_object,
            origin_groups=origin_groups,
            cache_behaviors=cache_behaviors,
            custom_error_responses=custom_error_responses,
            restrictions=restrictions,
            web_acl_id=web_acl_id,
            http_version=http_version,
            is_ipv6_enabled=is_ipv6_enabled,
            if_match=before["ret"].get("ETag"),
            timeout=timeout,
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.cloudfront.distribution", name=name
            )

        # update tags
        if tags is not None and tags != result["old_state"].get("tags"):
            update_tags_ret = await hub.tool.aws.cloudfront.tag.update_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = result["result"] and update_tags_ret["result"]
            resource_updated = resource_updated or bool(update_tags_ret["ret"])

            if ctx.get("test", False) and update_tags_ret["ret"]:
                plan_state["tags"] = update_tags_ret["ret"]

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "caller_reference": caller_reference,
                    "origins": origins,
                    "default_cache_behaviour": default_cache_behaviour,
                    "comment": comment,
                    "logging": logging,
                    "enabled": enabled,
                    "viewer_certificate": viewer_certificate,
                    "aliases": aliases,
                    "price_class": price_class,
                    "default_root_object": default_root_object,
                    "origin_groups": origin_groups,
                    "cache_behaviors": cache_behaviors,
                    "custom_error_responses": custom_error_responses,
                    "restrictions": restrictions,
                    "web_acl_id": web_acl_id,
                    "http_version": http_version,
                    "is_ipv6_enabled": is_ipv6_enabled,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.cloudfront.distribution", name=name
            )
            return result

        distribution_config = {
            "CallerReference": caller_reference,
            "Origins": origins,
            "DefaultCacheBehavior": default_cache_behaviour,
            "Comment": comment,
            "Logging": logging,
            "Enabled": enabled,
            "ViewerCertificate": viewer_certificate,
            "Aliases": aliases,
            "PriceClass": price_class,
            "DefaultRootObject": default_root_object,
            "OriginGroups": origin_groups,
            "CacheBehaviors": cache_behaviors,
            "CustomErrorResponses": custom_error_responses,
            "Restrictions": restrictions,
            "WebACLId": web_acl_id,
            "HttpVersion": http_version,
            "IsIPV6Enabled": is_ipv6_enabled,
        }
        distribution_config = (
            hub.tool.aws.cloudfront.distribution_utils.sanitize_distribution_config(
                distribution_config
            )
        )
        ret = await hub.exec.boto3.client.cloudfront.create_distribution_with_tags(
            ctx,
            DistributionConfigWithTags={
                "DistributionConfig": distribution_config,
                "Tags": {
                    "Items": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                },
            },
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["Distribution"]["Id"]

        waiter_ret = await hub.tool.aws.cloudfront.distribution.distribution_waiter(
            ctx, name, resource_id, timeout, "create"
        )
        if not waiter_ret["result"]:
            result["result"] = False
            result["comment"] += waiter_ret["comment"]

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.cloudfront.distribution", name=name
        )

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.cloudfront.distribution.get(
                ctx, name=name, resource_id=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=60)),
                        ("max_attempts", int, field(default=35)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=60)),
                        ("max_attempts", int, field(default=35)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Deletes a specified cloudfront distribution.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            AWS Cloudfront distribution ID.
            Idem automatically considers this resource being absent if this field is not specified.

        timeout(dict, Optional):
            Timeout configuration for create/update/deletion of AWS IAM Policy.

            * create (dict): Timeout configuration for creating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.
            * update(dict, Optional): Timeout configuration for updating AWS IAM Policy
                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [distribution-name]:
                  aws.cloudfront.distribution.absent:
                  - name: 'string'
                  - resource_id: 'string'
                  - timeout:
                      create:
                        delay: int
                        max_attempts: int
                      update:
                        delay: int
                        max_attempts: int

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            E2QWRUHAPOMQZL:
              aws.cloudfront.distribution.absent:
              - name: E2QWRUHAPOMQZL
              - resource_id: E2QWRUHAPOMQZL
              - timeout:
                  create:
                    delay: 60
                    max_attempts: 35
                  update:
                    delay: 60
                    max_attempts: 35
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.distribution", name=name
        )
        return result
    before = await hub.exec.aws.cloudfront.distribution.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.distribution", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.cloudfront.distribution", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        # we have to disable the distribution first for it to be deleted.
        # send an update request to disable, once disabled send delete request.

        disable_ret = await hub.tool.aws.cloudfront.distribution.disable_distribution(
            ctx=ctx,
            name=name,
            resource_id=resource_id,
            before=result["old_state"],
            if_match=before["ret"]["ETag"],
            timeout=timeout,
        )
        if not disable_ret["result"]:
            result["comment"] = disable_ret["comment"]
            result["result"] = False
            return result

        # once disabled get the latest Etag/IfMatch
        distribution_info_ret = await hub.exec.aws.cloudfront.distribution.get(
            ctx, name=name, resource_id=resource_id
        )
        if not distribution_info_ret["result"]:
            result["comment"] += distribution_info_ret["comment"]
            result["result"] = False
            return result

        ret = await hub.exec.boto3.client.cloudfront.delete_distribution(
            ctx, Id=resource_id, IfMatch=distribution_info_ret["ret"]["ETag"]
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.cloudfront.distribution", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """List CloudFront distributions.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.cloudfront.distribution
    """
    result = {}
    ret = await hub.exec.boto3.client.cloudfront.list_distributions(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe distribution {ret['comment']}")
        return {}

    for distribution in ret["ret"]["DistributionList"]["Items"]:
        resource_id = distribution.get("Id")
        # This is required to get caller reference
        distribution_config_ret = (
            await hub.exec.boto3.client.cloudfront.get_distribution(ctx, Id=resource_id)
        )
        if not distribution_config_ret["result"] or not distribution_config_ret[
            "ret"
        ].get("Distribution"):
            hub.log.warning(
                f"Could not describe distribution {resource_id} {distribution_config_ret['comment']}"
            )
            continue
        # This is required to get tags
        before_tag = await hub.exec.boto3.client.cloudfront.list_tags_for_resource(
            ctx, Resource=distribution_config_ret["ret"]["Distribution"]["ARN"]
        )
        if before_tag["result"] and before_tag["ret"].get("Tags"):
            distribution_config_ret["ret"]["Distribution"]["Tags"] = (
                before_tag["ret"].get("Tags").get("Items", [])
            )
        else:
            hub.log.debug(
                f"Could not get tags for distribution {resource_id} {before_tag['comment']}"
            )

        resource_translated = hub.tool.aws.cloudfront.conversion_utils.convert_raw_distribution_to_present(
            ctx,
            raw_resource=distribution_config_ret["ret"]["Distribution"],
            idem_resource_name=resource_id,
        )
        result[resource_id] = {
            "aws.cloudfront.distribution.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
