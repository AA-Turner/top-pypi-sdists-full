# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import Base64FileInput
from ..._utils import PropertyInfo

__all__ = [
    "TransferInCreateParams",
    "Contacts",
    "ContactsAdministrator",
    "ContactsAdministratorPostalInfo",
    "ContactsAdministratorPostalInfoAddress",
    "ContactsBilling",
    "ContactsBillingPostalInfo",
    "ContactsBillingPostalInfoAddress",
    "ContactsRegistrant",
    "ContactsRegistrantPostalInfo",
    "ContactsRegistrantPostalInfoAddress",
    "ContactsTechnical",
    "ContactsTechnicalPostalInfo",
    "ContactsTechnicalPostalInfoAddress",
]


class TransferInCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier."""

    auth_code: Annotated[Union[str, Base64FileInput], PropertyInfo(format="base64")]
    """
    The EPP/authorization code from your current registrar, base64-encoded per RFC
    4648 §4. Obtain this from your current registrar's control panel. Required for
    all extensions, except for UK.
    """

    auto_renew: bool
    """Enable or disable automatic renewal after transfer.

    Defaults to `false` if omitted.
    """

    contact_extensions: Dict[str, object]
    """
    Registry-specific contact extension values for the registrant.
    `GET /accounts/{account_id}/registrar/extensions/{extension}` documents the
    required keys and allowed values for each extension in the
    `transfer_schema.properties.contact_extensions` object.

    Examples include `.us` nexus fields, `.uk` registrant type fields, and `.ca`
    legal type fields. Include this object only when the extension's transfer schema
    defines `contact_extensions`.
    """

    contacts: Contacts
    """Provides contact data for the registration request.

    The per-extension schema from
    `GET /accounts/{account_id}/registrar/extensions/{extension}` defines the
    accepted contact roles. Every currently supported extension requires only
    `contacts.registrant` from API callers. Callers may provide additional roles
    such as `technical`, `administrator`, and `billing` when the extension schema
    includes them. When a registry requires an omitted role, Cloudflare may derive
    that contact from `contacts.registrant`.

    When the request omits either the entire `contacts` object or
    `contacts.registrant`, the system uses the account's default address book entry
    as the registrant contact. The account owner must configure this default at
    `https://dash.cloudflare.com/{account_id}/domains/registrations`, where they can
    create or update the address book entry and accept the required agreement.
    Dashboard settings currently provide the only way to manage address book
    entries.

    Without either a default address book entry or a registrant contact, the
    registration request fails validation.
    """

    privacy_mode: Literal["off", "redaction"]
    """WHOIS privacy mode to apply after transfer completes.

    Defaults to the extension's default privacy mode (typically `redaction`).
    """

    prefer: Annotated[str, PropertyInfo(alias="Prefer")]


class ContactsAdministratorPostalInfoAddress(TypedDict, total=False):
    """Physical mailing address for the registrant contact."""

    city: Required[str]
    """City or locality name."""

    country_code: Required[str]
    """Two-letter country code per ISO 3166-1 alpha-2 (e.g., `US`, `GB`, `CA`, `DE`)."""

    postal_code: Required[str]
    """Postal or ZIP code."""

    state: Required[str]
    """State, province, or region.

    Use the standard abbreviation where applicable (e.g., `TX` for Texas, `ON` for
    Ontario).
    """

    street: Required[str]
    """Street address including building/suite number."""


class ContactsAdministratorPostalInfo(TypedDict, total=False):
    """Postal/mailing information for the contact.

    The `name` field is the
    complete contact name in one string. Some registries require a complete
    personal name, including a family or last name where applicable, but this
    API does not accept separate first-name and last-name fields for
    registration contacts.
    """

    address: Required[ContactsAdministratorPostalInfoAddress]
    """Physical mailing address for the registrant contact."""

    name: Required[str]
    """
    Full legal name of the contact, including all required name components for an
    individual or authorized representative. Some registries require a complete
    personal name that includes a family or last name where applicable. Provide the
    complete name in this single field, for example `Ada Lovelace`; do not send
    separate first-name or last-name fields.
    """

    organization: str
    """Organization or company name. Optional for individual registrants."""


class ContactsAdministrator(TypedDict, total=False):
    """Optional administrator contact.

    Accepted only when the extension
    schema includes this role. When the registry requires an omitted
    contact, Cloudflare may derive it from `contacts.registrant`.
    """

    email: Required[str]
    """Email address for the registrant.

    Used for domain-related communications from the registry, including ownership
    verification and renewal notices.
    """

    phone: Required[str]
    """
    Phone number in E.164 format: `+{country_code}.{number}` without spaces or
    dashes. Examples: `+1.5555555555` (US), `+44.2071234567` (UK), `+81.312345678`
    (Japan).
    """

    postal_info: Required[ContactsAdministratorPostalInfo]
    """Postal/mailing information for the contact.

    The `name` field is the complete contact name in one string. Some registries
    require a complete personal name, including a family or last name where
    applicable, but this API does not accept separate first-name and last-name
    fields for registration contacts.
    """

    fax: str
    """Fax number in E.164 format (e.g., `+1.5555555555`).

    Optional. Most registrations do not require a fax number.
    """


class ContactsBillingPostalInfoAddress(TypedDict, total=False):
    """Physical mailing address for the registrant contact."""

    city: Required[str]
    """City or locality name."""

    country_code: Required[str]
    """Two-letter country code per ISO 3166-1 alpha-2 (e.g., `US`, `GB`, `CA`, `DE`)."""

    postal_code: Required[str]
    """Postal or ZIP code."""

    state: Required[str]
    """State, province, or region.

    Use the standard abbreviation where applicable (e.g., `TX` for Texas, `ON` for
    Ontario).
    """

    street: Required[str]
    """Street address including building/suite number."""


class ContactsBillingPostalInfo(TypedDict, total=False):
    """Postal/mailing information for the contact.

    The `name` field is the
    complete contact name in one string. Some registries require a complete
    personal name, including a family or last name where applicable, but this
    API does not accept separate first-name and last-name fields for
    registration contacts.
    """

    address: Required[ContactsBillingPostalInfoAddress]
    """Physical mailing address for the registrant contact."""

    name: Required[str]
    """
    Full legal name of the contact, including all required name components for an
    individual or authorized representative. Some registries require a complete
    personal name that includes a family or last name where applicable. Provide the
    complete name in this single field, for example `Ada Lovelace`; do not send
    separate first-name or last-name fields.
    """

    organization: str
    """Organization or company name. Optional for individual registrants."""


class ContactsBilling(TypedDict, total=False):
    """Optional billing contact.

    Accepted only when the extension schema
    includes this role. When the registry requires an omitted contact,
    Cloudflare may derive it from `contacts.registrant`.
    """

    email: Required[str]
    """Email address for the registrant.

    Used for domain-related communications from the registry, including ownership
    verification and renewal notices.
    """

    phone: Required[str]
    """
    Phone number in E.164 format: `+{country_code}.{number}` without spaces or
    dashes. Examples: `+1.5555555555` (US), `+44.2071234567` (UK), `+81.312345678`
    (Japan).
    """

    postal_info: Required[ContactsBillingPostalInfo]
    """Postal/mailing information for the contact.

    The `name` field is the complete contact name in one string. Some registries
    require a complete personal name, including a family or last name where
    applicable, but this API does not accept separate first-name and last-name
    fields for registration contacts.
    """

    fax: str
    """Fax number in E.164 format (e.g., `+1.5555555555`).

    Optional. Most registrations do not require a fax number.
    """


class ContactsRegistrantPostalInfoAddress(TypedDict, total=False):
    """Physical mailing address for the registrant contact."""

    city: Required[str]
    """City or locality name."""

    country_code: Required[str]
    """Two-letter country code per ISO 3166-1 alpha-2 (e.g., `US`, `GB`, `CA`, `DE`)."""

    postal_code: Required[str]
    """Postal or ZIP code."""

    state: Required[str]
    """State, province, or region.

    Use the standard abbreviation where applicable (e.g., `TX` for Texas, `ON` for
    Ontario).
    """

    street: Required[str]
    """Street address including building/suite number."""


class ContactsRegistrantPostalInfo(TypedDict, total=False):
    """Postal/mailing information for the contact.

    The `name` field is the
    complete contact name in one string. Some registries require a complete
    personal name, including a family or last name where applicable, but this
    API does not accept separate first-name and last-name fields for
    registration contacts.
    """

    address: Required[ContactsRegistrantPostalInfoAddress]
    """Physical mailing address for the registrant contact."""

    name: Required[str]
    """
    Full legal name of the contact, including all required name components for an
    individual or authorized representative. Some registries require a complete
    personal name that includes a family or last name where applicable. Provide the
    complete name in this single field, for example `Ada Lovelace`; do not send
    separate first-name or last-name fields.
    """

    organization: str
    """Organization or company name. Optional for individual registrants."""


class ContactsRegistrant(TypedDict, total=False):
    """Optional registrant contact.

    If omitted, the account's default
    address book entry is used instead.
    """

    email: Required[str]
    """Email address for the registrant.

    Used for domain-related communications from the registry, including ownership
    verification and renewal notices.
    """

    phone: Required[str]
    """
    Phone number in E.164 format: `+{country_code}.{number}` without spaces or
    dashes. Examples: `+1.5555555555` (US), `+44.2071234567` (UK), `+81.312345678`
    (Japan).
    """

    postal_info: Required[ContactsRegistrantPostalInfo]
    """Postal/mailing information for the contact.

    The `name` field is the complete contact name in one string. Some registries
    require a complete personal name, including a family or last name where
    applicable, but this API does not accept separate first-name and last-name
    fields for registration contacts.
    """

    fax: str
    """Fax number in E.164 format (e.g., `+1.5555555555`).

    Optional. Most registrations do not require a fax number.
    """


class ContactsTechnicalPostalInfoAddress(TypedDict, total=False):
    """Physical mailing address for the registrant contact."""

    city: Required[str]
    """City or locality name."""

    country_code: Required[str]
    """Two-letter country code per ISO 3166-1 alpha-2 (e.g., `US`, `GB`, `CA`, `DE`)."""

    postal_code: Required[str]
    """Postal or ZIP code."""

    state: Required[str]
    """State, province, or region.

    Use the standard abbreviation where applicable (e.g., `TX` for Texas, `ON` for
    Ontario).
    """

    street: Required[str]
    """Street address including building/suite number."""


class ContactsTechnicalPostalInfo(TypedDict, total=False):
    """Postal/mailing information for the contact.

    The `name` field is the
    complete contact name in one string. Some registries require a complete
    personal name, including a family or last name where applicable, but this
    API does not accept separate first-name and last-name fields for
    registration contacts.
    """

    address: Required[ContactsTechnicalPostalInfoAddress]
    """Physical mailing address for the registrant contact."""

    name: Required[str]
    """
    Full legal name of the contact, including all required name components for an
    individual or authorized representative. Some registries require a complete
    personal name that includes a family or last name where applicable. Provide the
    complete name in this single field, for example `Ada Lovelace`; do not send
    separate first-name or last-name fields.
    """

    organization: str
    """Organization or company name. Optional for individual registrants."""


class ContactsTechnical(TypedDict, total=False):
    """Optional technical contact.

    Accepted only when the extension schema
    includes this role. When the registry requires an omitted contact,
    Cloudflare may derive it from `contacts.registrant`.
    """

    email: Required[str]
    """Email address for the registrant.

    Used for domain-related communications from the registry, including ownership
    verification and renewal notices.
    """

    phone: Required[str]
    """
    Phone number in E.164 format: `+{country_code}.{number}` without spaces or
    dashes. Examples: `+1.5555555555` (US), `+44.2071234567` (UK), `+81.312345678`
    (Japan).
    """

    postal_info: Required[ContactsTechnicalPostalInfo]
    """Postal/mailing information for the contact.

    The `name` field is the complete contact name in one string. Some registries
    require a complete personal name, including a family or last name where
    applicable, but this API does not accept separate first-name and last-name
    fields for registration contacts.
    """

    fax: str
    """Fax number in E.164 format (e.g., `+1.5555555555`).

    Optional. Most registrations do not require a fax number.
    """


class Contacts(TypedDict, total=False):
    """Provides contact data for the registration request.

    The per-extension schema from
    `GET /accounts/{account_id}/registrar/extensions/{extension}` defines the
    accepted contact roles. Every currently supported extension requires only
    `contacts.registrant` from API callers. Callers may provide additional roles
    such as `technical`, `administrator`, and `billing` when the extension
    schema includes them. When a registry requires an omitted role, Cloudflare
    may derive that contact from `contacts.registrant`.

    When the request omits either the entire `contacts` object or
    `contacts.registrant`, the system uses the account's default address book
    entry as the registrant contact. The account owner must configure this
    default at `https://dash.cloudflare.com/{account_id}/domains/registrations`,
    where they can create or update the address book entry and accept the
    required agreement. Dashboard settings currently provide the only way to
    manage address book entries.

    Without either a default address book entry or a registrant contact, the
    registration request fails validation.
    """

    administrator: ContactsAdministrator
    """Optional administrator contact.

    Accepted only when the extension schema includes this role. When the registry
    requires an omitted contact, Cloudflare may derive it from
    `contacts.registrant`.
    """

    billing: ContactsBilling
    """Optional billing contact.

    Accepted only when the extension schema includes this role. When the registry
    requires an omitted contact, Cloudflare may derive it from
    `contacts.registrant`.
    """

    registrant: ContactsRegistrant
    """Optional registrant contact.

    If omitted, the account's default address book entry is used instead.
    """

    technical: ContactsTechnical
    """Optional technical contact.

    Accepted only when the extension schema includes this role. When the registry
    requires an omitted contact, Cloudflare may derive it from
    `contacts.registrant`.
    """
