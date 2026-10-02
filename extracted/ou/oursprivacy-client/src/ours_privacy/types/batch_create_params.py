# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["BatchCreateParams", "Event", "EventDefaultProperties", "EventIdentityContext", "EventUserProperties"]


class BatchCreateParams(TypedDict, total=False):
    token: Required[str]
    """The token for your Source. You can find this in the dashboard."""

    events: Required[Iterable[Event]]
    """A list of `/track`-shaped events to validate and enqueue together."""


class EventDefaultProperties(TypedDict, total=False):
    """
    These properties are used throughout the Ours app to pass known values onto destinations
    """

    _ef_transaction_id: Optional[str]
    """
    The Everflow affiliate Click (Transaction) ID, captured from the
    `_ef_transaction_id` URL parameter. Ex: ef_click_abc123
    """

    active_duration: Annotated[Optional[float], PropertyInfo(alias="activeDuration")]
    """The active time in milliseconds that the user had this tab active"""

    ad_id: Optional[str]
    """The ad id for detected in the session.

    This is set by the web sdk automatically.
    """

    admitad_uid: Optional[str]
    """The Admitad (Mitgo) affiliate Click ID. Ex: admitad_uid_abc123"""

    adset_id: Optional[str]
    """The adset id for detected in the session.

    This is set by the web sdk automatically.
    """

    alart: Optional[str]
    """The AppLovin alart query parameter. Ex: alart123"""

    aleid: Optional[str]
    """The AppLovin aleid query parameter. Ex: aleid123"""

    axwrt: Optional[str]
    """The AppLovin pixel cookie value (\\__axwrt). Web-only."""

    basis_cid: Optional[str]
    """The Basis DSP Click ID. Ex: basis_cid123"""

    beeswax_auction_id: Optional[str]
    """
    The Beeswax (FreeWheel Buyer Cloud) auction ID, captured from the
    `{{AUCTION_ID}}` macro on creative click URLs. Ex: bx-auc-abc123
    """

    browser_language: Optional[str]
    """The language of the browser. Ex: en-US"""

    browser_name: Optional[str]
    """The name of the browser. Ex: Chrome"""

    browser_version: Optional[str]
    """The version of the browser. Ex: 114.0"""

    campaign_id: Optional[str]
    """The campaign id for detected in the session.

    This is set by the web sdk automatically.
    """

    clickid: Optional[str]
    """The Click ID. Ex: clickid123"""

    clid: Optional[str]
    """The Generic Click ID. Ex: clid123"""

    cpu_architecture: Optional[str]
    """The architecture of the CPU. Ex: x64"""

    current_url: Optional[str]
    """The full url (including query params) of the current page"""

    dclid: Optional[str]
    """The DoubleClick Click ID. Ex: dclid123"""

    device_model: Optional[str]
    """The model of the device. Ex: iPhone 13"""

    device_type: Optional[str]
    """The type of device the user is using. Ex: mobile"""

    device_vendor: Optional[str]
    """The vendor of the device. Ex: Apple"""

    duration: Optional[float]
    """The time in milliseconds since the page was loaded // script was loaded"""

    encoding: Optional[str]
    """The browsers encoding. Ex: UTF-8"""

    engine_name: Optional[str]
    """The name of the browser engine. Ex: Blink"""

    engine_version: Optional[str]
    """The version of the browser engine. Ex: 114.0"""

    epik: Optional[str]
    """The Pinterest Click ID. Ex: epik456"""

    fbc: Optional[str]
    """Facebook Click ID with prefix format for Conversions API tracking.

    Ex: fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
    """

    fbclid: Optional[str]
    """Raw Facebook Click ID query parameter without prefix from ad clicks.

    Ex: AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
    """

    fbp: Optional[str]
    """Facebook Browser ID parameter for identifying browsers and attributing events.

    Ex: fb.1.1554763741205.1098115397
    """

    fv: Optional[bool]
    """Deprecated"""

    gad_source: Optional[str]
    """The Google Ad Source. Ex: google"""

    gbraid: Optional[str]
    """The Google Braid ID. Ex: gbraid123"""

    gclid: Optional[str]
    """The Google Click ID. Ex: gclid123"""

    host: Optional[str]
    """The host of the current page. Ex: example.com"""

    iframe: Optional[bool]
    """Whether the user is in an iframe. Ex: true"""

    im_ref: Optional[str]
    """The Impact Click ID reference. Ex: im_ref123"""

    ip: Optional[str]
    """The IP address of the user. Ex: 127.0.0.1"""

    irclickid: Optional[str]
    """The Impact Click ID. Ex: irclickid123"""

    is_bot: Optional[str]
    """Whether we have detected that the user is a bot.

    This is set automatically by the Ours server primarily for events tracked
    through the web SDK.
    """

    li_fat_id: Optional[str]
    """The LinkedIn Click ID. Ex: li_fat_id123"""

    msclkid: Optional[str]
    """The Microsoft Click ID. Ex: msclkid123"""

    ndclid: Optional[str]
    """The NextDoor Click ID. Ex: ndclid123"""

    new_s: Optional[bool]
    """Deprecated"""

    ob_click_id: Optional[str]
    """
    The Outbrain click ID, captured from the `ob_click_id` URL parameter (Outbrain
    `{{ob_click_id}}` macro) on the landing page. Ex: ob_click_abc123
    """

    oppref: Optional[str]
    """
    The OpenAI Ads privacy-preserving reference, captured from the `oppref` URL
    parameter on landing pages (the OpenAI Pixel also stores it in a `__oppref`
    cookie). Sent to OpenAI Ads on Conversions API events for attribution. Ex:
    oppref_abc
    """

    os_name: Optional[str]
    """The name of the operating system. Ex: Windows"""

    os_version: Optional[str]
    """The version of the operating system. Ex: 10.0"""

    page_hash: Optional[float]
    """A random set of numbers for the page load"""

    pathname: Optional[str]
    """The pathname of the current page. Ex: /home"""

    qclid: Optional[str]
    """The Quora Click ID. Ex: qclid123"""

    rdt_cid: Optional[str]
    """The Reddit Click ID. Ex: rdt_cid123"""

    received_at: Optional[str]
    """The time the event was received by an Ours server in ISO format"""

    referrer: Optional[str]
    """The referrer URL of the current page"""

    referring_domain: Optional[str]
    """The referring domain of the current page"""

    sacid: Optional[str]
    """The StackAdapt Tracking ID. Ex: sacid123"""

    sccid: Optional[str]
    """The SnapChat Click ID. Ex: sccid123"""

    screen_height: Optional[float]
    """The height of the screen. Ex: 1080"""

    screen_width: Optional[float]
    """The width of the screen. Ex: 1920"""

    session_count: Annotated[Optional[float], PropertyInfo(alias="sessionCount")]
    """The number of sessions the user has had. Ex: 3"""

    sid: Optional[str]
    """The session ID as assigned automatically by the web SDK.

    This is required for session replay
    """

    sr: Optional[str]

    title: Optional[str]
    """The title of the current page"""

    ttclid: Optional[str]
    """The TikTok Click ID. Ex: ttclid123"""

    twclid: Optional[str]
    """The Twitter Click ID. Ex: twclid123"""

    uafvl: Optional[str]
    """User agent as a full list of strings."""

    user_agent: Optional[str]
    """The user agent of the browser"""

    utm_campaign: Optional[str]
    """The UTM Campaign.

    The web SDK automatically captures this from the query params.
    """

    utm_content: Optional[str]
    """The UTM Content. The web SDK automatically captures this from the query params."""

    utm_medium: Optional[str]
    """The UTM Medium. The web SDK automatically captures this from the query params."""

    utm_name: Optional[str]
    """The UTM Name. The web SDK automatically captures this from the query params."""

    utm_source: Optional[str]
    """The UTM Source. The web SDK automatically captures this from the query params."""

    utm_term: Optional[str]
    """The UTM Term. The web SDK automatically captures this from the query params."""

    version: Optional[str]
    """The SDK version (e.g., web SDK or ingest-sdk-\\** via Stainless headers)"""

    viant_click_id: Optional[str]
    """
    The Viant (Adelphic) Click ID, captured from the `viant_click_id` URL parameter
    (Viant `${ADELPHIC_CLICKID}` macro). Sent as `xid` on Viant postbacks. Ex:
    viant_click_abc123
    """

    viant_impression_id: Optional[str]
    """
    The Viant (Adelphic) Impression ID, captured from the `viant_impression_id` URL
    parameter (Viant `${ADELPHIC_IMPRESSIONID}` macro). Sent as `imp_id` on Viant
    postbacks for post-view attribution. Ex: viant_imp_abc123
    """

    wbraid: Optional[str]
    """The WBRAID Identifier.

    The web SDK automatically captures this from the query params.
    """

    webview: Optional[bool]
    """Whether the user is in a webview. Ex: true"""


class EventIdentityContext(TypedDict, total=False):
    """End-user network context for server-side calls.

    Required for probabilistic identity resolution when the caller is a backend server rather than an end-user browser.
    """

    ip: Required[str]
    """The end-user IP address (not the server IP)."""

    user_agent: Required[Annotated[str, PropertyInfo(alias="userAgent")]]
    """The end-user User-Agent string (not the server UA)."""


class EventUserProperties(TypedDict, total=False):
    """Properties to set on the visitor.

    (optional) You can also update these properties via the identify endpoint.
    """

    _ef_transaction_id: Optional[str]

    ad_id: Optional[str]

    admitad_uid: Optional[str]

    adset_id: Optional[str]

    alart: Optional[str]

    aleid: Optional[str]

    axwrt: Optional[str]

    basis_cid: Optional[str]

    beeswax_auction_id: Optional[str]

    campaign_id: Optional[str]

    city: Optional[str]

    clickid: Optional[str]

    clid: Optional[str]

    company_name: Optional[str]

    consent: Optional[Dict[str, Optional[str]]]

    country: Optional[str]

    custom_properties: Optional[Dict[str, Optional[str]]]

    date_of_birth: Optional[str]

    dclid: Optional[str]

    email: Optional[str]

    epik: Optional[str]

    external_id: Optional[str]

    fbc: Optional[str]

    fbclid: Optional[str]

    fbp: Optional[str]

    first_name: Optional[str]

    gad_source: Optional[str]

    gbraid: Optional[str]

    gclid: Optional[str]

    gender: Optional[str]

    im_ref: Optional[str]

    ip: Optional[str]
    """The IP address of the user"""

    irclickid: Optional[str]

    is_bot: Optional[str]

    job_title: Optional[str]

    last_name: Optional[str]

    li_fat_id: Optional[str]

    msclkid: Optional[str]

    ndclid: Optional[str]

    ob_click_id: Optional[str]

    oppref: Optional[str]

    phone_number: Optional[str]

    qclid: Optional[str]

    rdt_cid: Optional[str]

    referrer: Optional[str]

    referring_domain: Optional[str]

    sacid: Optional[str]

    sccid: Optional[str]

    sid: Optional[str]

    state: Optional[str]

    ttclid: Optional[str]

    twclid: Optional[str]

    user_agent: Optional[str]

    user_agent_full_list: Optional[str]

    utm_campaign: Optional[str]

    utm_content: Optional[str]

    utm_medium: Optional[str]

    utm_name: Optional[str]

    utm_source: Optional[str]

    utm_term: Optional[str]

    viant_click_id: Optional[str]

    viant_impression_id: Optional[str]

    wbraid: Optional[str]

    zip: Optional[str]


class Event(TypedDict, total=False):
    distinct_id: Required[Annotated[str, PropertyInfo(alias="distinctId")]]
    """A unique identifier for this event used for deduplication.

    Highly recommended — if omitted, Ours will generate one for you, but supplying
    your own gives you stronger idempotency guarantees (e.g. a Stripe payment intent
    ID or your internal order ID).
    """

    event: Required[str]
    """The name of the event you're tracking.

    This must be whitelisted in the Ours dashboard.
    """

    default_properties: Annotated[Optional[EventDefaultProperties], PropertyInfo(alias="defaultProperties")]
    """
    These properties are used throughout the Ours app to pass known values onto
    destinations
    """

    email: Optional[str]
    """The email address of a user.

    When userId is absent and externalId does not resolve a visitor, we search your
    account for a visitor with this email. If no match is found, we try
    userProperties.phone_number before creating a new visitor.
    """

    event_properties: Annotated[Optional[Dict[str, Optional[str]]], PropertyInfo(alias="eventProperties")]
    """Any additional event properties you want to pass along."""

    external_id: Annotated[Optional[str], PropertyInfo(alias="externalId")]
    """Your system's unique identifier for this user.

    When userId is absent, we search your account for an existing visitor with this
    externalId. If no match is found, we try email and then
    userProperties.phone_number before creating a new visitor. If you also have the
    userId from cookies or local storage, send both — it removes the lookup
    round-trip.
    """

    identity_context: Annotated[Optional[EventIdentityContext], PropertyInfo(alias="identityContext")]
    """End-user network context for server-side calls.

    Required for probabilistic identity resolution when the caller is a backend
    server rather than an end-user browser.
    """

    time: Optional[float]
    """The time at which the event occurred in milliseconds since UTC epoch.

    The time must be in the past and within the last 7 days.
    """

    user_id: Annotated[Optional[str], PropertyInfo(alias="userId")]
    """The Ours Visitor ID stored in local storage and cookies on your web properties.

    When present, this is used directly — no lookup by externalId, email, or phone
    is performed. If you have both a userId and an externalId, send both so the
    event is attached to the right visitor without any lookup overhead.
    """

    user_properties: Annotated[Optional[EventUserProperties], PropertyInfo(alias="userProperties")]
    """Properties to set on the visitor.

    (optional) You can also update these properties via the identify endpoint.
    """
