"""Attribution captured by chatty_pixel (v6+).

v5 sent only the URL at click time, so UTMs and click IDs survived only while
they were still in the address bar — one internal navigation destroyed them.
v6 persists them in a first-party cookie and sends the whole picture along with
the browser cookies the ad platforms use as match keys.

Everything here is optional. Storage can be blocked (private mode, ITP), the
visitor may have consented out via `chattyPixelConfig.disableStorage`, and older
pixel versions send no `attribution` at all — in every one of those cases the
field is simply absent and the rest of the contact point still works.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AttributionTouch(BaseModel):
    """One inbound touch: the campaign params present when the visitor arrived."""

    timestamp: Optional[int] = Field(default=None, description="UNIX time in MILLISECONDS, as the browser reports it")
    last_timestamp: Optional[int] = Field(default=None, description="Most recent arrival through this same ad; equals timestamp when it only happened once")
    count: int = Field(default=1, description="Arrivals collapsed into this entry — a retargeting audience re-clicking the same ad is one touch seen N times, not N touches")
    landing_url: Optional[str] = Field(default=None)
    referrer: Optional[str] = Field(default=None)
    utm: Dict[str, str] = Field(default_factory=dict)
    click_ids: Dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(extra="ignore")

    @property
    def ad_identity(self) -> Optional[str]:
        """Best-effort identity of the ad behind this touch, most specific first.

        `utm_id` is Meta's `{{ad.id}}`, so it names the ad exactly, and it also
        outranks campaign matching on the Chatty side — the ad-id checker runs
        before the campaign one. Campaign is the coarser fallback; a bare click
        ID can only identify the click, not the ad.
        """
        utm_id = self.utm.get("utm_id")
        if utm_id:
            return f"ad:{utm_id}"
        campaign = self.utm.get("utm_campaign")
        if campaign:
            return f"campaign:{campaign}"
        for platform, value in sorted(self.click_ids.items()):
            return f"{platform}:{value}"
        return None


class ClickIdRecord(BaseModel):
    """A click ID with its own capture time.

    Kept separately from the touches because ad platforms want the freshest ID
    regardless of first/last touch logic.
    """

    value: Optional[str] = Field(default=None)
    timestamp: Optional[int] = Field(default=None, description="UNIX time in MILLISECONDS")

    model_config = ConfigDict(extra="ignore")


class PixelAttribution(BaseModel):
    """The full `attribution` block posted by chatty_pixel v6.

    `fbc` and `fbp` are the two that matter for Meta's Conversions API: they are
    the highest-quality match keys we can obtain, and neither can be derived
    server-side — they only exist as cookies in the visitor's browser.

    `fbc` here is authoritative in a way a synthesized one is not: when the real
    `_fbc` cookie exists it carries the true click time, where anything we build
    ourselves can only substitute the conversion time.
    """

    pixel_version: Optional[str] = Field(default=None)
    visitor_id: Optional[str] = Field(default=None, description="Stable per browser, 90 days")
    session_id: Optional[str] = Field(default=None, description="Rotates after 30 min of inactivity")

    first_touch: Optional[AttributionTouch] = Field(default=None, description="Written once, never overwritten")
    last_touch: Optional[AttributionTouch] = Field(default=None, description="Overwritten on each new inbound touch")
    touches: List[AttributionTouch] = Field(
        default_factory=list,
        description=(
            "The chain of DISTINCT ads that brought this visitor, oldest first, capped by "
            "what fits in the browser cookie. Empty for pixel v6.0 and older, which kept "
            "only the first and last touch and discarded everything in between."
        ),
    )
    click_ids: Dict[str, ClickIdRecord] = Field(default_factory=dict)

    fbc: Optional[str] = Field(default=None, description="Meta _fbc cookie, or synthesized by the pixel from an fbclid")
    fbp: Optional[str] = Field(default=None, description="Meta _fbp browser id cookie")
    ga_client_id: Optional[str] = Field(default=None, description="Parsed out of the _ga cookie")
    platform_cookies: Dict[str, str] = Field(default_factory=dict, description="Raw _fbp/_ga/_gcl_au/_ttp as read from the page")

    page_url: Optional[str] = Field(default=None)
    referrer: Optional[str] = Field(default=None)

    # Forward compatible on purpose: a newer pixel may add keys, and an older
    # backend should keep the ones it knows rather than reject the whole payload.
    model_config = ConfigDict(extra="ignore")

    @property
    def first_touch_utm_source(self) -> Optional[str]:
        if self.first_touch is None:
            return None
        return self.first_touch.utm.get("utm_source")

    def click_id(self, name: str) -> Optional[str]:
        """Freshest value for a click ID, e.g. `fbclid` or `gclid`."""
        record = self.click_ids.get(name)
        return record.value if record is not None else None
