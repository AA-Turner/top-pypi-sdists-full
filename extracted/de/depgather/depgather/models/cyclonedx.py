from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import Field, HttpUrl

from depgather.models.defaultonnone import DefaultOnNoneModel

DEFAULT_URL = HttpUrl("https://example.invalid")


class ComponentType(StrEnum):
	application = "application"
	framework = "framework"
	library = "library"
	container = "container"
	operating_system = "operating-system"
	device = "device"
	firmware = "firmware"
	file = "file"


class Hash(DefaultOnNoneModel):
	alg: str = ""
	content: str = ""


class License(DefaultOnNoneModel):
	id: str = ""
	name: str = ""


class LicenseChoice(DefaultOnNoneModel):
	license: License = License()


class OrganizationalEntity(DefaultOnNoneModel):
	name: str = ""
	urls: list[HttpUrl] = Field(default_factory=list)
	contacts: list[str] = Field(default_factory=list)


class ExternalReference(DefaultOnNoneModel):
	type: str = ""
	url: HttpUrl = DEFAULT_URL
	comment: str = ""


class Tool(DefaultOnNoneModel):
	vendor: str = ""
	name: str = ""
	version: str = ""


class Component(DefaultOnNoneModel):
	type: ComponentType = ComponentType.application
	name: str = ""

	version: str = ""
	bom_ref: str = Field("", alias="bom-ref")
	purl: str = ""
	cpe: str = ""

	supplier: OrganizationalEntity = OrganizationalEntity()

	hashes: list[Hash] = Field(default_factory=list)
	licenses: list[LicenseChoice] = Field(default_factory=list)
	external_references: list[ExternalReference] = Field(
		default_factory=list,
		alias="externalReferences",
	)

	components: list[Component] = Field(default_factory=list)


class Metadata(DefaultOnNoneModel):
	timestamp: datetime = datetime.now(tz=UTC)
	tools: list[Tool] = Field(default_factory=list)
	component: Component = Component()


class Bom(DefaultOnNoneModel):
	bom_format: str = Field(alias="bomFormat", default="")
	spec_version: str = Field(alias="specVersion", default="")
	serial_number: str | None = Field(None, alias="serialNumber")
	version: int = 1

	metadata: Metadata = Metadata()
	components: list[Component] = Field(default_factory=list)
