# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Mapping, Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["VisitorUpsertParams", "UserProperties", "DefaultProperties", "IdentityContext"]


class VisitorUpsertParams(TypedDict, total=False):
    token: Required[str]
    """The token for your Source.

    You can find this in the dashboard. Leading and trailing whitespace is removed
    before validation.
    """

    user_properties: Required[Annotated[UserProperties, PropertyInfo(alias="userProperties")]]
    """User properties to associate with this user.

    The existing user properties will be updated. And all future events will have
    these properties associated with them.
    """

    default_properties: Annotated[Optional[DefaultProperties], PropertyInfo(alias="defaultProperties")]
    """
    These properties are used throughout the Ours app to pass known values onto
    destinations
    """

    email: Optional[str]
    """The email address of a user.

    When userId is absent and externalId does not resolve a visitor, we search your
    account for a visitor with this email. If no match is found, we try
    userProperties.phone_number before creating a new visitor. Leading and trailing
    whitespace is removed before validation.
    """

    external_id: Annotated[Optional[str], PropertyInfo(alias="externalId")]
    """Your system's unique identifier for this user.

    When userId is absent, we search your account for an existing visitor with this
    externalId. If no match is found, we try email and then
    userProperties.phone_number before creating a new visitor. If you also have the
    userId from cookies or local storage, send both — it removes the lookup
    round-trip. Non-string input is converted to text before validation; clients
    should send a string. Leading and trailing whitespace is removed before
    validation.
    """

    identity_context: Annotated[Optional[IdentityContext], PropertyInfo(alias="identityContext")]
    """End-user network context for server-side calls.

    Required for probabilistic identity resolution when the caller is a backend
    server rather than an end-user browser.
    """

    user_id: Annotated[Optional[str], PropertyInfo(alias="userId")]
    """The Ours Visitor ID stored in local storage and cookies on your web properties.

    When present, this is used directly — no lookup by externalId, email, or phone
    is performed. If you have both a userId and an externalId, send both so the
    event is attached to the right visitor without any lookup overhead. Leading and
    trailing whitespace is removed before validation.
    """


class UserProperties(TypedDict, total=False):
    """User properties to associate with this user.

    The existing user properties will be updated. And all future events will have these properties associated with them.
    """

    _ef_transaction_id: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    ad_id: Optional[str]

    admitad_uid: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    adset_id: Optional[str]

    alart: Optional[str]

    aleid: Optional[str]

    axwrt: Optional[str]

    basis_cid: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    beeswax_auction_id: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    campaign_id: Optional[str]

    city: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    clickid: Optional[str]

    clid: Optional[str]

    company_name: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    consent: Optional[
        Mapping[
            str,
            Union[
                Optional[str],
                float,
                bool,
                SequenceNotStr[Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]],
                Mapping[
                    str,
                    Union[
                        Optional[str],
                        float,
                        bool,
                        SequenceNotStr[
                            Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
                        ],
                        Mapping[
                            str,
                            Union[
                                Optional[str],
                                float,
                                bool,
                                SequenceNotStr[
                                    Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
                                ],
                                Mapping[
                                    str,
                                    Union[
                                        Optional[str],
                                        float,
                                        bool,
                                        SequenceNotStr[
                                            Union[
                                                Optional[str],
                                                float,
                                                bool,
                                                Iterable[object],
                                                Mapping[str, object],
                                                int,
                                                None,
                                            ]
                                        ],
                                        Mapping[
                                            str,
                                            Union[
                                                Optional[str],
                                                float,
                                                bool,
                                                SequenceNotStr[
                                                    Union[
                                                        Optional[str],
                                                        float,
                                                        bool,
                                                        Iterable[object],
                                                        Mapping[str, object],
                                                        int,
                                                        None,
                                                    ]
                                                ],
                                                int,
                                                None,
                                            ],
                                        ],
                                        int,
                                        None,
                                    ],
                                ],
                                int,
                                None,
                            ],
                        ],
                        int,
                        None,
                    ],
                ],
                int,
                None,
            ],
        ]
    ]
    """Use at most 200 nonempty property keys and five object levels.

    Array contents do not count toward the object-depth limit. Empty keys are
    removed recursively, arrays are truncated to 250 entries, and top-level numbers
    outside the safe integer range become strings. After normalization, the
    serialized JSON must be shorter than 1,048,576 UTF-16 code units.
    """

    country: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    custom_properties: Optional[
        Mapping[
            str,
            Union[
                Optional[str],
                float,
                bool,
                SequenceNotStr[Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]],
                Mapping[
                    str,
                    Union[
                        Optional[str],
                        float,
                        bool,
                        SequenceNotStr[
                            Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
                        ],
                        Mapping[
                            str,
                            Union[
                                Optional[str],
                                float,
                                bool,
                                SequenceNotStr[
                                    Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
                                ],
                                Mapping[
                                    str,
                                    Union[
                                        Optional[str],
                                        float,
                                        bool,
                                        SequenceNotStr[
                                            Union[
                                                Optional[str],
                                                float,
                                                bool,
                                                Iterable[object],
                                                Mapping[str, object],
                                                int,
                                                None,
                                            ]
                                        ],
                                        Mapping[
                                            str,
                                            Union[
                                                Optional[str],
                                                float,
                                                bool,
                                                SequenceNotStr[
                                                    Union[
                                                        Optional[str],
                                                        float,
                                                        bool,
                                                        Iterable[object],
                                                        Mapping[str, object],
                                                        int,
                                                        None,
                                                    ]
                                                ],
                                                int,
                                                None,
                                            ],
                                        ],
                                        int,
                                        None,
                                    ],
                                ],
                                int,
                                None,
                            ],
                        ],
                        int,
                        None,
                    ],
                ],
                int,
                None,
            ],
        ]
    ]
    """Use at most 200 nonempty property keys and five object levels.

    Array contents do not count toward the object-depth limit. Empty keys are
    removed recursively, arrays are truncated to 250 entries, and top-level numbers
    outside the safe integer range become strings. After normalization, the
    serialized JSON must be shorter than 1,048,576 UTF-16 code units.
    """

    date_of_birth: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    dclid: Optional[str]

    email: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    epik: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    external_id: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    fbc: Optional[str]

    fbclid: Optional[str]

    fbp: Optional[str]

    first_name: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    gad_source: Optional[str]

    gbraid: Optional[str]

    gclid: Optional[str]

    gender: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    graid: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    grclid: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    im_ref: Optional[str]

    ip: Optional[str]
    """
    The IP address of the user Leading and trailing whitespace is removed before
    validation.
    """

    irclickid: Optional[str]

    is_bot: Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
    """Any JSON value: string, number, boolean, array, object, or null."""

    job_title: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    last_name: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    li_fat_id: Optional[str]

    msclkid: Optional[str]

    ndclid: Optional[str]

    ob_click_id: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    oppref: Optional[str]

    phone_number: Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
    """Any JSON value: string, number, boolean, array, object, or null."""

    qclid: Optional[str]

    rdt_cid: Optional[str]

    referrer: Optional[str]

    referring_domain: Optional[str]

    sacid: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    sccid: Optional[str]

    sid: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    state: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string. Leading and trailing whitespace is removed before validation.
    """

    ttclid: Optional[str]

    twclid: Optional[str]

    user_agent: Optional[str]

    user_agent_full_list: Optional[str]

    utm_campaign: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    utm_content: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    utm_medium: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    utm_name: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    utm_source: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    utm_term: Optional[str]
    """
    Non-string input is converted to text before validation; clients should send a
    string.
    """

    viant_click_id: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    viant_impression_id: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    wbraid: Optional[str]

    zip: Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
    """Any JSON value: string, number, boolean, array, object, or null."""


class DefaultProperties(TypedDict, total=False):
    """
    These properties are used throughout the Ours app to pass known values onto destinations
    """

    _ef_transaction_id: Optional[str]
    """
    The Everflow affiliate Click (Transaction) ID, captured from the
    `_ef_transaction_id` URL parameter. Ex: ef_click_abc123 Leading and trailing
    whitespace is removed before validation.
    """

    active_duration: Annotated[Optional[float], PropertyInfo(alias="activeDuration")]
    """The active time in milliseconds that the user had this tab active"""

    ad_id: Optional[str]
    """The ad id for detected in the session.

    This is set by the web sdk automatically. Leading and trailing whitespace is
    removed before validation.
    """

    admitad_uid: Optional[str]
    """The Admitad (Mitgo) affiliate Click ID.

    Ex: admitad_uid_abc123 Leading and trailing whitespace is removed before
    validation.
    """

    adset_id: Optional[str]
    """The adset id for detected in the session.

    This is set by the web sdk automatically. Leading and trailing whitespace is
    removed before validation.
    """

    alart: Optional[str]
    """The AppLovin alart query parameter.

    Ex: alart123 Leading and trailing whitespace is removed before validation.
    """

    aleid: Optional[str]
    """The AppLovin aleid query parameter.

    Ex: aleid123 Leading and trailing whitespace is removed before validation.
    """

    axwrt: Optional[str]
    """The AppLovin pixel cookie value (\\__axwrt).

    Web-only. Leading and trailing whitespace is removed before validation.
    """

    basis_cid: Optional[str]
    """The Basis DSP Click ID.

    Ex: basis_cid123 Leading and trailing whitespace is removed before validation.
    """

    beeswax_auction_id: Optional[str]
    """
    The Beeswax (FreeWheel Buyer Cloud) auction ID, captured from the
    `{{AUCTION_ID}}` macro on creative click URLs. Ex: bx-auc-abc123 Leading and
    trailing whitespace is removed before validation.
    """

    browser_language: Optional[str]
    """The language of the browser.

    Ex: en-US Leading and trailing whitespace is removed before validation.
    """

    browser_name: Optional[str]
    """The name of the browser.

    Ex: Chrome Leading and trailing whitespace is removed before validation.
    """

    browser_version: Optional[str]
    """The version of the browser.

    Ex: 114.0 Leading and trailing whitespace is removed before validation.
    """

    campaign_id: Optional[str]
    """The campaign id for detected in the session.

    This is set by the web sdk automatically. Leading and trailing whitespace is
    removed before validation.
    """

    clickid: Optional[str]
    """The Click ID.

    Ex: clickid123 Leading and trailing whitespace is removed before validation.
    """

    clid: Optional[str]
    """The Generic Click ID.

    Ex: clid123 Leading and trailing whitespace is removed before validation.
    """

    cpu_architecture: Optional[str]
    """The architecture of the CPU.

    Ex: x64 Leading and trailing whitespace is removed before validation.
    """

    current_url: Optional[str]
    """
    The full url (including query params) of the current page Leading and trailing
    whitespace is removed before validation.
    """

    dclid: Optional[str]
    """The DoubleClick Click ID.

    Ex: dclid123 Leading and trailing whitespace is removed before validation.
    """

    device_model: Optional[str]
    """The model of the device.

    Ex: iPhone 13 Leading and trailing whitespace is removed before validation.
    """

    device_type: Optional[str]
    """The type of device the user is using.

    Ex: mobile Leading and trailing whitespace is removed before validation.
    """

    device_vendor: Optional[str]
    """The vendor of the device.

    Ex: Apple Leading and trailing whitespace is removed before validation.
    """

    duration: Optional[float]
    """The time in milliseconds since the page was loaded // script was loaded"""

    encoding: Optional[str]
    """The browsers encoding.

    Ex: UTF-8 Leading and trailing whitespace is removed before validation.
    """

    engine_name: Optional[str]
    """The name of the browser engine.

    Ex: Blink Leading and trailing whitespace is removed before validation.
    """

    engine_version: Optional[str]
    """The version of the browser engine.

    Ex: 114.0 Leading and trailing whitespace is removed before validation.
    """

    epik: Optional[str]
    """The Pinterest Click ID.

    Ex: epik456 Leading and trailing whitespace is removed before validation.
    """

    fbc: Optional[str]
    """Facebook Click ID with prefix format for Conversions API tracking.

    Ex: fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890 Leading and trailing
    whitespace is removed before validation.
    """

    fbclid: Optional[str]
    """Raw Facebook Click ID query parameter without prefix from ad clicks.

    Ex: AbCdEfGhIjKlMnOpQrStUvWxYz1234567890 Leading and trailing whitespace is
    removed before validation.
    """

    fbp: Optional[str]
    """Facebook Browser ID parameter for identifying browsers and attributing events.

    Ex: fb.1.1554763741205.1098115397 Leading and trailing whitespace is removed
    before validation.
    """

    fv: Optional[bool]
    """Deprecated"""

    gad_source: Optional[str]
    """The Google Ad Source.

    Ex: google Leading and trailing whitespace is removed before validation.
    """

    gbraid: Optional[str]
    """The Google Braid ID.

    Ex: gbraid123 Leading and trailing whitespace is removed before validation.
    """

    gclid: Optional[str]
    """The Google Click ID.

    Ex: gclid123 Leading and trailing whitespace is removed before validation.
    """

    graid: Optional[str]
    """
    The Gravity attribution ID, captured from the `graid` URL parameter on the
    landing page. Gravity resolves it to the campaign, publisher, and ad IDs
    server-side. Ex: graid-abc123 Leading and trailing whitespace is removed before
    validation.
    """

    grclid: Optional[str]
    """
    The Gravity click ID, captured from the `grclid` URL parameter that Gravity
    (trygravity.com) appends to ad click-through URLs on the landing page. Ex:
    grclid-abc123 Leading and trailing whitespace is removed before validation.
    """

    host: Optional[str]
    """The host of the current page.

    Ex: example.com Leading and trailing whitespace is removed before validation.
    """

    iframe: Optional[bool]
    """Whether the user is in an iframe. Ex: true"""

    im_ref: Optional[str]
    """The Impact Click ID reference.

    Ex: im_ref123 Leading and trailing whitespace is removed before validation.
    """

    ip: Optional[str]
    """The IP address of the user.

    Ex: 127.0.0.1 Leading and trailing whitespace is removed before validation.
    """

    irclickid: Optional[str]
    """The Impact Click ID.

    Ex: irclickid123 Leading and trailing whitespace is removed before validation.
    """

    is_bot: Union[Optional[str], float, bool, Iterable[object], Mapping[str, object], int, None]
    """Any JSON value: string, number, boolean, array, object, or null."""

    li_fat_id: Optional[str]
    """The LinkedIn Click ID.

    Ex: li_fat_id123 Leading and trailing whitespace is removed before validation.
    """

    msclkid: Optional[str]
    """The Microsoft Click ID.

    Ex: msclkid123 Leading and trailing whitespace is removed before validation.
    """

    ndclid: Optional[str]
    """The NextDoor Click ID.

    Ex: ndclid123 Leading and trailing whitespace is removed before validation.
    """

    new_s: Optional[bool]
    """Deprecated"""

    ob_click_id: Optional[str]
    """
    The Outbrain click ID, captured from the `ob_click_id` URL parameter (Outbrain
    `{{ob_click_id}}` macro) on the landing page. Ex: ob_click_abc123 Leading and
    trailing whitespace is removed before validation.
    """

    oppref: Optional[str]
    """
    The OpenAI Ads privacy-preserving reference, captured from the `oppref` URL
    parameter on landing pages (the OpenAI Pixel also stores it in a `__oppref`
    cookie). Sent to OpenAI Ads on Conversions API events for attribution. Ex:
    oppref_abc Leading and trailing whitespace is removed before validation.
    """

    os_name: Optional[str]
    """The name of the operating system.

    Ex: Windows Leading and trailing whitespace is removed before validation.
    """

    os_version: Optional[str]
    """The version of the operating system.

    Ex: 10.0 Leading and trailing whitespace is removed before validation.
    """

    page_hash: Optional[float]
    """A random set of numbers for the page load"""

    pathname: Optional[str]
    """The pathname of the current page.

    Ex: /home Leading and trailing whitespace is removed before validation.
    """

    qclid: Optional[str]
    """The Quora Click ID.

    Ex: qclid123 Leading and trailing whitespace is removed before validation.
    """

    rdt_cid: Optional[str]
    """The Reddit Click ID.

    Ex: rdt_cid123 Leading and trailing whitespace is removed before validation.
    """

    received_at: Optional[str]
    """The time the event was received by an Ours server in ISO format"""

    referrer: Optional[str]
    """
    The referrer URL of the current page Leading and trailing whitespace is removed
    before validation.
    """

    referring_domain: Optional[str]
    """
    The referring domain of the current page Leading and trailing whitespace is
    removed before validation.
    """

    sacid: Optional[str]
    """The StackAdapt Tracking ID.

    Ex: sacid123 Leading and trailing whitespace is removed before validation.
    """

    sccid: Optional[str]
    """The SnapChat Click ID.

    Ex: sccid123 Leading and trailing whitespace is removed before validation.
    """

    screen_height: Optional[float]
    """The height of the screen. Ex: 1080"""

    screen_width: Optional[float]
    """The width of the screen. Ex: 1920"""

    session_count: Annotated[Optional[float], PropertyInfo(alias="sessionCount")]
    """The number of sessions the user has had. Ex: 3"""

    sid: Optional[str]
    """The session ID as assigned automatically by the web SDK.

    This is required for session replay Leading and trailing whitespace is removed
    before validation.
    """

    sr: Optional[str]
    """Leading and trailing whitespace is removed before validation."""

    title: Optional[str]
    """
    The title of the current page Leading and trailing whitespace is removed before
    validation.
    """

    ttclid: Optional[str]
    """The TikTok Click ID.

    Ex: ttclid123 Leading and trailing whitespace is removed before validation.
    """

    twclid: Optional[str]
    """The Twitter Click ID.

    Ex: twclid123 Leading and trailing whitespace is removed before validation.
    """

    uafvl: Optional[str]
    """User agent as a full list of strings.

    Leading and trailing whitespace is removed before validation.
    """

    user_agent: Optional[str]
    """
    The user agent of the browser Leading and trailing whitespace is removed before
    validation.
    """

    utm_campaign: Optional[str]
    """The UTM Campaign.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    utm_content: Optional[str]
    """The UTM Content.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    utm_medium: Optional[str]
    """The UTM Medium.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    utm_name: Optional[str]
    """The UTM Name.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    utm_source: Optional[str]
    """The UTM Source.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    utm_term: Optional[str]
    """The UTM Term.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    version: Optional[str]
    """
    The SDK version (e.g., web SDK or ingest-sdk-\\** via generated SDK headers)
    Leading and trailing whitespace is removed before validation.
    """

    viant_click_id: Optional[str]
    """
    The Viant (Adelphic) Click ID, captured from the `viant_click_id` URL parameter
    (Viant `${ADELPHIC_CLICKID}` macro). Sent as `xid` on Viant postbacks. Ex:
    viant_click_abc123 Leading and trailing whitespace is removed before validation.
    """

    viant_impression_id: Optional[str]
    """
    The Viant (Adelphic) Impression ID, captured from the `viant_impression_id` URL
    parameter (Viant `${ADELPHIC_IMPRESSIONID}` macro). Sent as `imp_id` on Viant
    postbacks for post-view attribution. Ex: viant_imp_abc123 Leading and trailing
    whitespace is removed before validation.
    """

    wbraid: Optional[str]
    """The WBRAID Identifier.

    The web SDK automatically captures this from the query params. Leading and
    trailing whitespace is removed before validation.
    """

    webview: Optional[bool]
    """Whether the user is in a webview. Ex: true"""


class IdentityContext(TypedDict, total=False):
    """End-user network context for server-side calls.

    Required for probabilistic identity resolution when the caller is a backend server rather than an end-user browser.
    """

    ip: Required[str]
    """The end-user IP address (not the server IP)."""

    user_agent: Required[Annotated[str, PropertyInfo(alias="userAgent")]]
    """The end-user User-Agent string (not the server UA)."""
