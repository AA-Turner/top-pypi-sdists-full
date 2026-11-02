# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the company_identify platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class CompanyIdentifyCrustdataV3Input(TypedDict, total=False):
    """Input for Company Identify - Crustdata v3."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    companyDomain: NotRequired[str]
    """Company website domain without a scheme or path, e.g. stripe.com. Send exactly one of companyDomain, companyLinkedinUrl, companyId, or companyName."""
    companyId: NotRequired[int]
    """Crustdata company id, as returned in companyId by this or another Crustdata v3 endpoint. Minimum: 1."""
    companyLinkedinUrl: NotRequired[str]
    """LinkedIn company page URL, e.g. https://www.linkedin.com/company/stripe."""
    companyName: NotRequired[str]
    """Full company name, including any legal suffix. A name match is a best guess; confirm it against the returned domain or LinkedIn page before relying on it."""
    exactMatch: NotRequired[bool]
    """Require an exact match on the identifier instead of letting Crustdata decide. Leave unset for automatic matching."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class CompanyIdentifyCrustdataV3Data(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    company_id: str | None = Field(
        alias="companyId",
        description="Crustdata company id. Send it as companyId to identify the same company again.",
    )
    company_type: str | None = Field(
        default=None,
        alias="companyType",
        description="Ownership type, e.g. Privately Held or Public Company.",
    )
    confidence_score: float | None = Field(
        default=None,
        alias="confidenceScore",
        description="Match confidence from 0 to 1. Treat a low score on a name match as a guess.",
    )
    description: str | None = Field(default=None, description="Company description.")
    domain: str | None = Field(
        description="Primary website domain, or null when Crustdata holds none for this company."
    )
    domains: list[str] | None = Field(
        default=None, description="Every website domain Crustdata links to the company."
    )
    employee_range: str | None = Field(
        default=None,
        alias="employeeRange",
        description="Employee count band, e.g. 5001-10000.",
    )
    founded_year: int | None = Field(
        default=None, alias="foundedYear", description="Year the company was founded."
    )
    image: str | None = Field(default=None, description="Company logo URL.")
    industries: list[str] | None = Field(
        default=None, description="Industries the company operates in."
    )
    linkedin_company_id: str | None = Field(
        default=None,
        alias="linkedinCompanyId",
        description="LinkedIn numeric company id.",
    )
    linkedin_profile_name: str | None = Field(
        default=None,
        alias="linkedinProfileName",
        description="Company name as shown on its LinkedIn page.",
    )
    linkedin_url: str | None = Field(
        default=None, alias="linkedinUrl", description="LinkedIn company page URL."
    )
    markets: list[str] | None = Field(
        default=None,
        description="Markets the company is listed in, e.g. PRIVATE or NASDAQ.",
    )
    match_type: str | None = Field(
        default=None,
        alias="matchType",
        description="Which kind of identifier produced the match, e.g. domain.",
    )
    name: str | None = Field(default=None, description="Company name.")
    website: str | None = Field(default=None, description="Company website URL.")


class CompanyIdentifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyIdentifyCrustdataV3Input],
    ) -> RunResult[CompanyIdentifyCrustdataV3Data]:
        """Company Identify - Crustdata v3

        Resolve one company from its domain, LinkedIn company page, Crustdata
        company id, or name to its Crustdata id, primary domain, LinkedIn page, and
        basic profile. Identify a company for $1 per 1,000 requests before paying to
        enrich it.

        Price: $0.001 per request.

        Example:
            res = client.company_identify.crustdata_v3(companyDomain="stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "company_identify.crustdata_v3", dict(input), options
        )
        return RunResult[CompanyIdentifyCrustdataV3Data].model_validate(raw)


class AsyncCompanyIdentifyNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def crustdata_v3(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[CompanyIdentifyCrustdataV3Input],
    ) -> RunResult[CompanyIdentifyCrustdataV3Data]:
        """Company Identify - Crustdata v3

        Resolve one company from its domain, LinkedIn company page, Crustdata
        company id, or name to its Crustdata id, primary domain, LinkedIn page, and
        basic profile. Identify a company for $1 per 1,000 requests before paying to
        enrich it.

        Price: $0.001 per request.

        Example:
            res = client.company_identify.crustdata_v3(companyDomain="stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "company_identify.crustdata_v3", dict(input), options
        )
        return RunResult[CompanyIdentifyCrustdataV3Data].model_validate(raw)
