from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import Field, HttpUrl

from depgather.models.defaultonnone import DefaultOnNoneModel

DEFAULT_URL = HttpUrl("https://example.invalid")


class SPDXDataLicense(StrEnum):
	CC0_1_0 = "CC0-1.0"


class RelationshipType(StrEnum):
	depends_on = "DEPENDS_ON"
	dependency_of = "DEPENDENCY_OF"
	contains = "CONTAINS"
	contained_by = "CONTAINED_BY"
	describes = "DESCRIBES"


class Checksum(DefaultOnNoneModel):
	algorithm: str = ""
	checksum_value: str = Field("", alias="checksumValue")


class License(DefaultOnNoneModel):
	id: str = ""
	name: str = ""


class ExternalReference(DefaultOnNoneModel):
	reference_type: str = Field("", alias="referenceType")
	locator: HttpUrl = DEFAULT_URL
	comment: str = ""


class CreationInfo(DefaultOnNoneModel):
	created: datetime = datetime.now(tz=UTC)
	creators: list[str] = Field(default_factory=list)
	license_list_version: str = Field("", alias="licenseListVersion")


class Package(DefaultOnNoneModel):
	name: str = ""
	spdx_id: str = Field("", alias="SPDXID")

	version_info: str = Field("", alias="versionInfo")
	supplier: str = ""
	originator: str = ""

	download_location: HttpUrl = DEFAULT_URL

	license_concluded: str = Field("", alias="licenseConcluded")
	license_declared: str = Field("", alias="licenseDeclared")

	copyright_text: str = Field("", alias="copyrightText")

	checksums: list[Checksum] = Field(default_factory=list)
	external_refs: list[ExternalReference] = Field(
		default_factory=list,
		alias="externalRefs",
	)


class File(DefaultOnNoneModel):
	file_name: str = Field("", alias="fileName")
	spdx_id: str = Field("", alias="SPDXID")

	checksums: list[Checksum] = Field(default_factory=list)
	license_concluded: str = Field("", alias="licenseConcluded")


class Relationship(DefaultOnNoneModel):
	spdx_element_id: str = Field("", alias="spdxElementId")
	relationship_type: RelationshipType = Field(
		RelationshipType.depends_on,
		alias="relationshipType",
	)
	related_spdx_element: str = Field(
		"",
		alias="relatedSpdxElement",
	)


class SPDX(DefaultOnNoneModel):
	spdx_version: str = Field("SPDX-2.3", alias="spdxVersion")
	data_license: SPDXDataLicense = Field(
		SPDXDataLicense.CC0_1_0,
		alias="dataLicense",
	)

	name: str = ""
	document_namespace: HttpUrl = Field(
		DEFAULT_URL,
		alias="documentNamespace",
	)

	creation_info: CreationInfo = Field(
		default_factory=CreationInfo,
		alias="creationInfo",
	)

	packages: list[Package] = Field(default_factory=list)
	files: list[File] = Field(default_factory=list)
	relationships: list[Relationship] = Field(default_factory=list)
