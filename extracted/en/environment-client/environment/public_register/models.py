from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PublicRegisterModel(BaseModel):
    """Base model with common configuration for Public Register data."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Metadata(PublicRegisterModel):
    publisher: str
    licence: str
    documentation: str
    has_format: list[str] | None = Field(None, alias="hasFormat")
    version: str | None = None
    comment: str | None = None
    limit: int | None = None
    offset: int | None = None


class Register(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    label: str | None = None
    type: dict[str, Any] | None = None


class Holder(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    name: str | list[str]
    trading_name: str | None = Field(None, alias="tradingName")


class HolderSummary(Holder):
    type: str | list[str] | None = None


class HolderTypeReference(PublicRegisterModel):
    id: str = Field(..., alias="@id")


class HolderDetail(Holder):
    type: HolderTypeReference | list[HolderTypeReference] | None = None


class PostcodeReference(PublicRegisterModel):
    id: str = Field(..., alias="@id")


class Address(PublicRegisterModel):
    address: str | list[str]
    postcode: str | None = None
    organization_name: str | None = Field(None, alias="organization_name")
    street_address: str | int | list[str] | None = Field(None, alias="street_address")
    locality: str | None = None

    @field_validator("postcode", mode="before")
    @classmethod
    def ensure_postcode_str(cls, value: Any) -> str | None:
        """
        Handle cases where API returns a list of postcodes.
        Prioritizes the formatted version (containing a space).
        """
        if isinstance(value, list):
            if not value:
                return None

            for postcode in value:
                if " " in postcode:
                    return postcode

            return value[0]

        return value


class AddressSummary(Address):
    postcode_uri: str | PostcodeReference | None = Field(None, alias="postcodeURI")


class AddressDetail(Address):
    postcode_uri: str | PostcodeReference | None = Field(None, alias="postcodeURI")


class Site(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    site_address: AddressSummary | AddressDetail | None = Field(
        None, alias="siteAddress"
    )


class SiteLocation(PublicRegisterModel):
    easting: float
    northing: float
    grid_reference: str | None = Field(None, alias="gridReference")


class SiteDetail(Site):
    location: SiteLocation | None = None
    premises: str | None = None
    site_type: dict[str, Any] | None = Field(None, alias="siteType")


class RegistrationType(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    notation: str | None = None
    label: str | None = None
    pref_label: str | None = Field(None, alias="prefLabel")
    see_also: str | dict[str, str] | None = Field(None, alias="seeAlso")


class LocalAuthority(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    label: str


class Tier(PublicRegisterModel):
    id: str | None = Field(None, alias="@id")
    label: str | None = None


class RDFType(PublicRegisterModel):
    id: str = Field(..., alias="@id")


class GenericRegistration(PublicRegisterModel):
    id: str = Field(..., alias="@id")
    register_: Register = Field(..., alias="register")
    registration_number: str | int = Field(..., alias="registrationNumber")

    @property
    def register(self) -> Register:
        """Expose the register field without shadowing BaseModel.register."""
        return self.register_


class GenericRegistrationSummary(GenericRegistration):
    type: list[str] | None = None
    holder: HolderSummary | list[HolderSummary] | None = None


class GenericRegistrationDetail(GenericRegistration):
    type: list[RDFType] = Field(default_factory=list)
    holder: HolderDetail | list[HolderDetail] | None = None


class RegistrationSummary(GenericRegistrationSummary):
    expiry_date: str | None = Field(None, alias="expiryDate")
    registration_date: str | None = Field(None, alias="registrationDate")
    local_authority: LocalAuthority | None = Field(None, alias="localAuthority")
    registration_type: RegistrationType | None = Field(None, alias="registrationType")
    site: Site | list[Site] | None = None
    tier: Tier | None = None
    distance: float | None = None


class RegistrationDetail(GenericRegistrationDetail):
    label: str | None = None
    notation: str | None = None
    expiry_date: str | None = Field(None, alias="expiryDate")
    registration_date: str | None = Field(None, alias="registrationDate")
    registration_type: RegistrationType | None = Field(None, alias="registrationType")
    site: Site | SiteDetail | None = None
    tier: Tier | None = None
    local_authority: LocalAuthority | None = Field(None, alias="localAuthority")


class RegistrationSearchResponse(PublicRegisterModel):
    meta: Metadata
    items: list[RegistrationSummary] = Field(default_factory=list)
