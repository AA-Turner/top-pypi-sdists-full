from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.advisory_severity import AdvisorySeverity
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.advisory_cvss import AdvisoryCVSS
  from ..models.advisory_epss import AdvisoryEPSS
  from ..models.advisory_weakness import AdvisoryWeakness





T = TypeVar("T", bound="AdvisoryItem")



@_attrs_define
class AdvisoryItem:
    """ One open Dependabot alert with the fields GitHub's alert page shows.

        Attributes:
            number (int): The alert's number on the forge. For Forgejo, the advisory's place in the list.
            state (str): The alert's state on the forge. Always "open" here.
            summary (str): The advisory's one-line title.
            severity (AdvisorySeverity | Unset): The worst severity among the open advisories. Absent when there are none.
            id (str | Unset): The advisory's own id in the database that states it. Set for Forgejo.
            ghsa_id (str | Unset):
            cve_id (str | Unset):
            package (str | Unset): The vulnerable dependency's name.
            ecosystem (str | Unset): The package ecosystem, such as "npm" or "pip".
            scope (str | Unset): Whether the dependency is needed at runtime or only in development.
            relationship (str | Unset): Whether the dependency is direct or transitive. Absent when GitHub didn't say.
            manifest_path (str | Unset): The file the dependency was detected in.
            opened_at (datetime.datetime | Unset):
            vulnerable_versions (str | Unset): The affected version range, as GitHub writes it.
            patched_version (str | Unset): The first version with the fix. Absent when there is none yet.
            cvss (AdvisoryCVSS | Unset):
            weaknesses (list[AdvisoryWeakness] | Unset):
            description (str | Unset): The advisory's text, Markdown exactly as GitHub stores it. Render it with raw HTML
                disabled.
            references (list[str] | Unset): Links the advisory cites. A client shows only http(s) ones.
            epss (AdvisoryEPSS | Unset): The Exploit Prediction Scoring System's reading, as GitHub sends it. Absent when
                GitHub sent none.
            url (str | Unset): The alert's own page on the forge.
     """

    number: int
    state: str
    summary: str
    severity: AdvisorySeverity | Unset = UNSET
    id: str | Unset = UNSET
    ghsa_id: str | Unset = UNSET
    cve_id: str | Unset = UNSET
    package: str | Unset = UNSET
    ecosystem: str | Unset = UNSET
    scope: str | Unset = UNSET
    relationship: str | Unset = UNSET
    manifest_path: str | Unset = UNSET
    opened_at: datetime.datetime | Unset = UNSET
    vulnerable_versions: str | Unset = UNSET
    patched_version: str | Unset = UNSET
    cvss: AdvisoryCVSS | Unset = UNSET
    weaknesses: list[AdvisoryWeakness] | Unset = UNSET
    description: str | Unset = UNSET
    references: list[str] | Unset = UNSET
    epss: AdvisoryEPSS | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.advisory_cvss import AdvisoryCVSS # noqa: PLC0415
        from ..models.advisory_epss import AdvisoryEPSS # noqa: PLC0415
        from ..models.advisory_weakness import AdvisoryWeakness # noqa: PLC0415
        number = self.number

        state = self.state

        summary = self.summary

        severity: str | Unset = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value


        id = self.id

        ghsa_id = self.ghsa_id

        cve_id = self.cve_id

        package = self.package

        ecosystem = self.ecosystem

        scope = self.scope

        relationship = self.relationship

        manifest_path = self.manifest_path

        opened_at: str | Unset = UNSET
        if not isinstance(self.opened_at, Unset):
            opened_at = self.opened_at.isoformat()

        vulnerable_versions = self.vulnerable_versions

        patched_version = self.patched_version

        cvss: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cvss, Unset):
            cvss = self.cvss.to_dict()

        weaknesses: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.weaknesses, Unset):
            weaknesses = []
            for weaknesses_item_data in self.weaknesses:
                weaknesses_item = weaknesses_item_data.to_dict()
                weaknesses.append(weaknesses_item)



        description = self.description

        references: list[str] | Unset = UNSET
        if not isinstance(self.references, Unset):
            references = self.references



        epss: dict[str, Any] | Unset = UNSET
        if not isinstance(self.epss, Unset):
            epss = self.epss.to_dict()

        url = self.url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "number": number,
            "state": state,
            "summary": summary,
        })
        if severity is not UNSET:
            field_dict["severity"] = severity
        if id is not UNSET:
            field_dict["id"] = id
        if ghsa_id is not UNSET:
            field_dict["ghsaId"] = ghsa_id
        if cve_id is not UNSET:
            field_dict["cveId"] = cve_id
        if package is not UNSET:
            field_dict["package"] = package
        if ecosystem is not UNSET:
            field_dict["ecosystem"] = ecosystem
        if scope is not UNSET:
            field_dict["scope"] = scope
        if relationship is not UNSET:
            field_dict["relationship"] = relationship
        if manifest_path is not UNSET:
            field_dict["manifestPath"] = manifest_path
        if opened_at is not UNSET:
            field_dict["openedAt"] = opened_at
        if vulnerable_versions is not UNSET:
            field_dict["vulnerableVersions"] = vulnerable_versions
        if patched_version is not UNSET:
            field_dict["patchedVersion"] = patched_version
        if cvss is not UNSET:
            field_dict["cvss"] = cvss
        if weaknesses is not UNSET:
            field_dict["weaknesses"] = weaknesses
        if description is not UNSET:
            field_dict["description"] = description
        if references is not UNSET:
            field_dict["references"] = references
        if epss is not UNSET:
            field_dict["epss"] = epss
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advisory_cvss import AdvisoryCVSS # noqa: PLC0415
        from ..models.advisory_epss import AdvisoryEPSS # noqa: PLC0415
        from ..models.advisory_weakness import AdvisoryWeakness # noqa: PLC0415
        d = dict(src_dict)
        number = d.pop("number")

        state = d.pop("state")

        summary = d.pop("summary")

        _severity = d.pop("severity", UNSET)
        severity: AdvisorySeverity | Unset
        if isinstance(_severity,  Unset):
            severity = UNSET
        else:
            severity = AdvisorySeverity(_severity)




        id = d.pop("id", UNSET)

        ghsa_id = d.pop("ghsaId", UNSET)

        cve_id = d.pop("cveId", UNSET)

        package = d.pop("package", UNSET)

        ecosystem = d.pop("ecosystem", UNSET)

        scope = d.pop("scope", UNSET)

        relationship = d.pop("relationship", UNSET)

        manifest_path = d.pop("manifestPath", UNSET)

        _opened_at = d.pop("openedAt", UNSET)
        opened_at: datetime.datetime | Unset
        if isinstance(_opened_at,  Unset):
            opened_at = UNSET
        else:
            opened_at = datetime.datetime.fromisoformat(_opened_at)




        vulnerable_versions = d.pop("vulnerableVersions", UNSET)

        patched_version = d.pop("patchedVersion", UNSET)

        _cvss = d.pop("cvss", UNSET)
        cvss: AdvisoryCVSS | Unset
        if isinstance(_cvss,  Unset):
            cvss = UNSET
        else:
            cvss = AdvisoryCVSS.from_dict(_cvss)




        _weaknesses = d.pop("weaknesses", UNSET)
        weaknesses: list[AdvisoryWeakness] | Unset = UNSET
        if _weaknesses is not UNSET:
            weaknesses = []
            for weaknesses_item_data in _weaknesses:
                weaknesses_item = AdvisoryWeakness.from_dict(weaknesses_item_data)



                weaknesses.append(weaknesses_item)


        description = d.pop("description", UNSET)

        references = cast(list[str], d.pop("references", UNSET))


        _epss = d.pop("epss", UNSET)
        epss: AdvisoryEPSS | Unset
        if isinstance(_epss,  Unset):
            epss = UNSET
        else:
            epss = AdvisoryEPSS.from_dict(_epss)




        url = d.pop("url", UNSET)

        advisory_item = cls(
            number=number,
            state=state,
            summary=summary,
            severity=severity,
            id=id,
            ghsa_id=ghsa_id,
            cve_id=cve_id,
            package=package,
            ecosystem=ecosystem,
            scope=scope,
            relationship=relationship,
            manifest_path=manifest_path,
            opened_at=opened_at,
            vulnerable_versions=vulnerable_versions,
            patched_version=patched_version,
            cvss=cvss,
            weaknesses=weaknesses,
            description=description,
            references=references,
            epss=epss,
            url=url,
        )


        advisory_item.additional_properties = d
        return advisory_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
