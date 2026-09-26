# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ProfileUpdateParams"]


class ProfileUpdateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier"""

    address: str
    """Street address line 1."""

    address2: str
    """Street address line 2 (apt, suite, etc.)."""

    billing_email: str
    """Primary billing email address."""

    buying_rate_plan: str
    """Rate plan being purchased right after profile setup."""

    captcha_challenge_jwt: str
    """Captcha challenge JWT issued during onboarding."""

    cf_turnstile_response: str
    """Cloudflare Turnstile response."""

    city: str
    """City on the billing profile."""

    company: str
    """Company name on the billing profile."""

    country: str
    """ISO 3166-1 alpha-2 country code."""

    first_name: str
    """First name on the billing profile."""

    h_captcha_response: str
    """hCaptcha response."""

    last_name: str
    """Last name on the billing profile."""

    preferred_locale: str
    """Preferred locale for invoice rendering (BCP 47)."""

    secondary_billing_email: str
    """Secondary billing email address for CC on invoices."""

    state: str
    """State or region on the billing profile."""

    tax_id_type: str
    """Type of tax ID provided."""

    telephone: str
    """Contact phone number."""

    vat: str
    """VAT identifier."""

    zipcode: str
    """ZIP or postal code."""
