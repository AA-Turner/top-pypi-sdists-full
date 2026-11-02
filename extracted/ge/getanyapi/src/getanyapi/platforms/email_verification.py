# Generated - do not edit. Regenerate with: pnpm generate
"""Generated namespace module for the email_verification platform."""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import NotRequired, Required, TypedDict, Unpack

from ..types import RequestOptions, RunResult

if TYPE_CHECKING:
    from .._async_client import AsyncAnyAPI
    from .._client import AnyAPI


class EmailVerificationAllegrowInput(TypedDict, total=False):
    """Input for Email Verification - Allegrow."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: Required[str]
    """Email address to validate."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerificationBouncebanInput(TypedDict, total=False):
    """Input for Email Verification - BounceBan."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    disableCatchallVerify: NotRequired[bool]
    email: Required[str]
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    mode: NotRequired[Literal["regular", "deepverify"]]
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerificationIcypeasInput(TypedDict, total=False):
    """Input for Email Verification - Icypeas."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: Required[str]
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerificationZerobounceInput(TypedDict, total=False):
    """Input for Email Verification - ZeroBounce."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: Required[str]
    """Email address to validate."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    ipAddress: NotRequired[str]
    """IP address the address signed up from. ZeroBounce uses it to add the geographic fields to the answer."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerificationZerobounceActivityInput(TypedDict, total=False):
    """Input for Email Activity - ZeroBounce."""

    allowFallbacks: NotRequired[bool]
    """Optional, default true. When false, only the sources listed in `source` may serve; the request is refused with no charge if none of them can. When true, the listed sources are tried first and any other source may serve after them, at the normal price. Default: true."""
    email: Required[str]
    """Email address to check for activity."""
    ignoreSources: NotRequired[list[str]]
    """Optional. Source ids to skip for this request, taken from this endpoint's `lanes[].source.id`. The cheapest remaining source serves and the price is that of the dearest remaining source. An id that does not serve this endpoint, or that is also in `source`, is rejected as invalid input with no charge; skipping every source is rejected the same way."""
    preferLatencyUnderMs: NotRequired[int]
    """Optional; omit it and routing is unchanged, with the cheapest source serving. Prefer sources whose typical response time (median over the trailing 30 days, as published on this endpoint's lane health) is under this many milliseconds; among those, the cheapest serves. This can raise your price: when the cheapest source misses the target, a faster and dearer one serves, and you are quoted and charged its price. If no source is that fast the request is still served, by whichever source offers the best speed for its price - it is never refused for being slow. Sources we have not timed are tried last. This is a preference, not a guarantee: the median describes past requests and is not a ceiling on this one, and it excludes any wait this request itself asks for. On a paginated walk it applies to the first page only: later pages stay with the source that page chose, at the price it was quoted. Minimum: 1."""
    source: NotRequired[list[str]]
    """Optional. Source ids to prefer, in order, taken from this endpoint's `lanes[].source.id` in /catalog or /apis. Omit it and the cheapest source serves, with automatic failover. Listed sources are tried first in the order given, then the others, unless `allowFallbacks` is false. A single source with `allowFallbacks` false is served only by that source at its price, quoted and charged exactly, with no failover. The price is that of the dearest source that may serve. An id that does not serve this endpoint is rejected as invalid input with no charge; a listed source that is not serving right now is refused with no charge, so omit `source` to be served by another. On a paginated walk, later pages must include the source that served page one, or omit `source`."""


class EmailVerificationAllegrowData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    allegrow_status: str | None = Field(
        default=None,
        alias="allegrowStatus",
        description="The Allegrow dataset's own verdict field, returned verbatim as the source spells it (safe in the captured response). It duplicates status in the same response and is not remapped into the good/risky/bad vocabulary email.verify uses.",
    )
    domain: str | None = Field(default=None, description="Email domain.")
    email: str | None = Field(description="Validated email address.")
    is_catch_all: bool | None = Field(
        default=None,
        alias="isCatchAll",
        description="Whether the domain accepts mail for arbitrary recipients.",
    )
    is_role_account: bool | None = Field(
        default=None,
        alias="isRoleAccount",
        description="Whether the mailbox appears to be a role account.",
    )
    mx_provider: str | None = Field(
        default=None, alias="mxProvider", description="Detected mail provider."
    )
    mx_records: list[str] | None = Field(
        default=None,
        alias="mxRecords",
        description="MX record hosts published by the email domain.",
    )
    provider_request_id: str | None = Field(
        default=None,
        alias="providerRequestId",
        description="The source's own identifier for this validation, surfaced so a result can be traced back to the record the source created.",
    )
    status: (
        Literal[
            "safe",
            "do_not_mail_abuse",
            "some_risk",
            "block_bounce_risk",
            "dead_email",
            "spamtrap",
            "more_time_required",
            "missing_email",
            "null",
        ]
        | None
    ) = Field(
        description="Deliverability verdict; negative verdicts are successful billable results."
    )
    sub_status: str | None = Field(
        default=None,
        alias="subStatus",
        description="More specific validation result when available.",
    )
    validated_utc: float | None = Field(
        default=None,
        alias="validatedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )


class EmailVerificationBouncebanData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email: str | None
    is_catch_all: bool | None = Field(default=None, alias="isCatchAll")
    is_disposable: bool | None = Field(default=None, alias="isDisposable")
    is_free: bool | None = Field(default=None, alias="isFree")
    is_role: bool | None = Field(default=None, alias="isRole")
    mode: str | None = None
    mx_records: list[str] | None = Field(default=None, alias="mxRecords")
    reason: str | None = None
    result: str | None = Field(
        description="Deliverability verdict; negative verdicts are successful results."
    )
    score: float | None = None
    smtp_provider: str | None = Field(default=None, alias="smtpProvider")
    verified_at: str | None = Field(default=None, alias="verifiedAt")


class EmailVerificationIcypeasData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    certainty: str | None = Field(
        default=None,
        description="Confidence rating for the address, returned verbatim as the source spells it (ultra_sure in the captured response). It is not remapped to another verdict vocabulary.",
    )
    created_utc: float | None = Field(
        default=None,
        alias="createdUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    email: str | None = Field(
        default=None,
        description="The verified email address as the source returned it.",
    )
    firstname: str | None = Field(
        default=None,
        description="First name carried by the source's scan record. Present only when that record holds identity data, which the verification path usually does not.",
    )
    fullname: str | None = Field(
        default=None,
        description="Full name carried by the source's scan record. Present only when that record holds identity data, which the verification path usually does not.",
    )
    gender: str | None = Field(
        default=None,
        description="Gender carried by the source's scan record, returned verbatim. Present only when that record holds identity data, which the verification path usually does not; the source's UNKNOWN sentinel is reported as absent.",
    )
    lastname: str | None = Field(
        default=None,
        description="Last name carried by the source's scan record. Present only when that record holds identity data, which the verification path usually does not.",
    )
    linkedin_url: str | None = Field(
        default=None,
        alias="linkedinUrl",
        description="LinkedIn profile URL carried by the source's scan record. Present only when that record holds identity data, which the verification path usually does not.",
    )
    modified_utc: float | None = Field(
        default=None,
        alias="modifiedUtc",
        description="UTC epoch timestamp in seconds (Unix time). Multiply by 1000 for a JS Date in milliseconds.",
    )
    mx_provider: str | None = Field(
        default=None,
        alias="mxProvider",
        description="Mail provider detected from the address domain's MX records.",
    )
    mx_records: list[str] | None = Field(
        default=None,
        alias="mxRecords",
        description="MX record hosts published by the address domain.",
    )
    phones: Any | None = Field(
        default=None,
        description="Phone numbers carried by the source's scan record, passed through in whatever shape the source returns them. Empty in the captured response and absent when the source holds none, so this field is not type-constrained.",
    )
    saas_services: Any | None = Field(
        default=None,
        alias="saasServices",
        description="SaaS services carried by the source's scan record, passed through in whatever shape the source returns them. Empty in the captured response and absent when the source holds none, so this field is not type-constrained.",
    )
    scan_id: str | None = Field(
        default=None,
        alias="scanId",
        description="The source's own identifier for the scan record behind this verification, surfaced so a result can be traced back to it at the source.",
    )
    scan_name: str | None = Field(
        default=None,
        alias="scanName",
        description="The source's own label for the kind of scan record it created, returned verbatim (__icypeas__individual in the captured response). It is not a person's name.",
    )
    scan_order: int | None = Field(
        default=None,
        alias="scanOrder",
        description="Position the source assigned to this record within the scan it belongs to; 0 for a single-address verification.",
    )
    scan_user: str | None = Field(
        default=None,
        alias="scanUser",
        description="The source's own identifier for the account that ran the scan.",
    )
    status: str | None = Field(
        description="Scan outcome for the address, returned verbatim as the source spells it (FOUND in the captured response; the scan also reports NOT_FOUND). This is not the good/risky/bad vocabulary used by email.verify."
    )


class EmailVerificationZerobounceData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    account: str | None = Field(
        default=None, description="Local part of the address, before the @."
    )
    catchall_domain: bool | None = Field(
        default=None,
        alias="catchallDomain",
        description="True when the domain accepts mail to any local part, so no address on it can be individually confirmed.",
    )
    city: str | None = Field(
        default=None, description="City from the supplied signup IP."
    )
    country: str | None = Field(
        default=None, description="Country from the supplied signup IP."
    )
    did_you_mean: str | None = Field(
        default=None,
        alias="didYouMean",
        description="Corrected address when ZeroBounce spots a likely typo.",
    )
    domain: str | None = Field(default=None, description="Domain part of the address.")
    domain_age_days: int | None = Field(
        default=None,
        alias="domainAgeDays",
        description="How long the domain has been registered, in days.",
    )
    email: str | None = Field(description="The address that was validated.")
    first_name: str | None = Field(
        default=None,
        alias="firstName",
        description="First name ZeroBounce associates with the address.",
    )
    free_email: bool | None = Field(
        default=None,
        alias="freeEmail",
        description="True for a free consumer mailbox such as gmail.com.",
    )
    gender: str | None = Field(
        default=None, description="Gender ZeroBounce associates with the address."
    )
    last_name: str | None = Field(
        default=None,
        alias="lastName",
        description="Last name ZeroBounce associates with the address.",
    )
    mx_found: bool | None = Field(
        default=None,
        alias="mxFound",
        description="True when the domain publishes MX records.",
    )
    mx_record: str | None = Field(
        default=None, alias="mxRecord", description="The domain's primary MX host."
    )
    processed_utc: float | None = Field(
        default=None,
        alias="processedUtc",
        description="UTC epoch timestamp in seconds (Unix time) ZeroBounce ran the check. Multiply by 1000 for a JS Date in milliseconds.",
    )
    region: str | None = Field(
        default=None, description="Region from the supplied signup IP."
    )
    smtp_provider: str | None = Field(
        default=None,
        alias="smtpProvider",
        description="Mailbox provider behind the domain, e.g. g-suite.",
    )
    status: str | None = Field(
        description="Deliverability verdict: valid, invalid, catch-all, unknown, spamtrap, abuse or do_not_mail."
    )
    sub_status: str | None = Field(
        default=None,
        alias="subStatus",
        description="Why that verdict was reached, e.g. mailbox_not_found, role_based, disposable.",
    )
    zipcode: str | None = Field(
        default=None, description="Postal code from the supplied signup IP."
    )


class EmailVerificationZerobounceActivityData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    active_in_days: int | None = Field(
        default=None,
        alias="activeInDays",
        description="How recently the address was active, in days. ZeroBounce buckets this rather than giving an exact figure.",
    )
    email: str | None = Field(description="The address that was checked.")
    first_seen_utc: float | None = Field(
        default=None,
        alias="firstSeenUtc",
        description="UTC epoch timestamp in seconds (Unix time) ZeroBounce first saw activity from the address. Multiply by 1000 for a JS Date in milliseconds.",
    )
    has_activity: bool | None = Field(
        alias="hasActivity",
        description="True when ZeroBounce has seen engagement from this address.",
    )


class EmailVerificationNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AnyAPI") -> None:
        self._client = client

    def allegrow(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationAllegrowInput],
    ) -> RunResult[EmailVerificationAllegrowData]:
        """Email Verification - Allegrow

        Validate an email address and return its deliverability verdict and mailbox
        signals.

        Price: $0.0144 per request.

        Example:
            res = client.email_verification.allegrow(email="tim@apollo.io")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.allegrow", dict(input), options
        )
        return RunResult[EmailVerificationAllegrowData].model_validate(raw)

    def bounceban(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationBouncebanInput],
    ) -> RunResult[EmailVerificationBouncebanData]:
        """Email Verification - BounceBan

        Verify an email address, including catch-all handling. Completion uses the
        durable Request lifecycle; a negative verdict is a successful result.

        Price: $0.0072 per request.

        Example:
            res = client.email_verification.bounceban(email="tim@apollo.io", mode="regular")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.bounceban", dict(input), options
        )
        return RunResult[EmailVerificationBouncebanData].model_validate(raw)

    def icypeas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationIcypeasInput],
    ) -> RunResult[EmailVerificationIcypeasData]:
        """Email Verification - Icypeas

        Verify an email address. A valid negative verdict is a successful, billable
        result.

        Price: $0.0024 per request.

        Example:
            res = client.email_verification.icypeas(email="support@stripe.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.icypeas", dict(input), options
        )
        return RunResult[EmailVerificationIcypeasData].model_validate(raw)

    def zerobounce(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationZerobounceInput],
    ) -> RunResult[EmailVerificationZerobounceData]:
        """Email Verification - ZeroBounce

        Validate one email address against ZeroBounce, with the deliverability
        verdict, why it was reached, the mailbox provider, and any owner details
        ZeroBounce holds. A negative verdict is a successful, billable result.

        Price: $0.0336 per request.

        Example:
            res = client.email_verification.zerobounce(email="tim@apollo.io")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.zerobounce", dict(input), options
        )
        return RunResult[EmailVerificationZerobounceData].model_validate(raw)

    def zerobounce_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationZerobounceActivityInput],
    ) -> RunResult[EmailVerificationZerobounceActivityData]:
        """Email Activity - ZeroBounce

        Check whether an email address has shown recent activity across ZeroBounce's
        engagement network before you re-engage it. A no-activity answer is a
        successful, billable result.

        Price: $0.0336 per request.

        Example:
            res = client.email_verification.zerobounce_activity(email="dshah@hubspot.com")
        """
        raw = self._client._run_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.zerobounce_activity", dict(input), options
        )
        return RunResult[EmailVerificationZerobounceActivityData].model_validate(raw)


class AsyncEmailVerificationNamespace:
    """Typed methods for this platform. Attached lazily to the client."""

    def __init__(self, client: "AsyncAnyAPI") -> None:
        self._client = client

    async def allegrow(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationAllegrowInput],
    ) -> RunResult[EmailVerificationAllegrowData]:
        """Email Verification - Allegrow

        Validate an email address and return its deliverability verdict and mailbox
        signals.

        Price: $0.0144 per request.

        Example:
            res = client.email_verification.allegrow(email="tim@apollo.io")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.allegrow", dict(input), options
        )
        return RunResult[EmailVerificationAllegrowData].model_validate(raw)

    async def bounceban(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationBouncebanInput],
    ) -> RunResult[EmailVerificationBouncebanData]:
        """Email Verification - BounceBan

        Verify an email address, including catch-all handling. Completion uses the
        durable Request lifecycle; a negative verdict is a successful result.

        Price: $0.0072 per request.

        Example:
            res = client.email_verification.bounceban(email="tim@apollo.io", mode="regular")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.bounceban", dict(input), options
        )
        return RunResult[EmailVerificationBouncebanData].model_validate(raw)

    async def icypeas(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationIcypeasInput],
    ) -> RunResult[EmailVerificationIcypeasData]:
        """Email Verification - Icypeas

        Verify an email address. A valid negative verdict is a successful, billable
        result.

        Price: $0.0024 per request.

        Example:
            res = client.email_verification.icypeas(email="support@stripe.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.icypeas", dict(input), options
        )
        return RunResult[EmailVerificationIcypeasData].model_validate(raw)

    async def zerobounce(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationZerobounceInput],
    ) -> RunResult[EmailVerificationZerobounceData]:
        """Email Verification - ZeroBounce

        Validate one email address against ZeroBounce, with the deliverability
        verdict, why it was reached, the mailbox provider, and any owner details
        ZeroBounce holds. A negative verdict is a successful, billable result.

        Price: $0.0336 per request.

        Example:
            res = client.email_verification.zerobounce(email="tim@apollo.io")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.zerobounce", dict(input), options
        )
        return RunResult[EmailVerificationZerobounceData].model_validate(raw)

    async def zerobounce_activity(
        self,
        *,
        options: RequestOptions | None = None,
        **input: Unpack[EmailVerificationZerobounceActivityInput],
    ) -> RunResult[EmailVerificationZerobounceActivityData]:
        """Email Activity - ZeroBounce

        Check whether an email address has shown recent activity across ZeroBounce's
        engagement network before you re-engage it. A no-activity answer is a
        successful, billable result.

        Price: $0.0336 per request.

        Example:
            res = client.email_verification.zerobounce_activity(email="dshah@hubspot.com")
        """
        raw = await self._client._arun_raw(  # pyright: ignore[reportPrivateUsage]
            "email_verification.zerobounce_activity", dict(input), options
        )
        return RunResult[EmailVerificationZerobounceActivityData].model_validate(raw)
