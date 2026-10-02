from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json
from .. import types

from ..types import UNSET, Unset

from ..types import File, FileTypes
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="ManagedAgentsFormDataSkillVersionBundleUploadRequest")



@_attrs_define
class ManagedAgentsFormDataSkillVersionBundleUploadRequest:
    """ Multipart body carrying a zipped skill directory in the bundle part, plus the base version it advances from.
    Replaces every file in the skill: parts left out are cleared, not inherited from the current version.

        Example:
            {'base_skill_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'bundle': 'example', 'display_title':
                'example', 'metadata': 'example'}

        Attributes:
            base_skill_version_id (str): Required. The skill's current latest_skill_version_id, as returned by getSkill.
                Rejected with 409 revision_conflict if the skill has moved past this version.
            bundle (File | Unset): A zipped skill directory: SKILL.md at its root or one level down, plus optional scripts/,
                references/ and assets/. Files under scripts/ are mounted executable.
            display_title (str | Unset): Human-readable title for listings. Defaults to the frontmatter name.
            metadata (str | Unset): Caller-owned key/value data as a JSON object, since a form part cannot carry structure.
                Rejected rather than dropped when it does not parse.
     """

    base_skill_version_id: str
    bundle: File | Unset = UNSET
    display_title: str | Unset = UNSET
    metadata: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        base_skill_version_id = self.base_skill_version_id

        bundle: FileTypes | Unset = UNSET
        if not isinstance(self.bundle, Unset):
            bundle = self.bundle.to_tuple()


        display_title = self.display_title

        metadata = self.metadata


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "base_skill_version_id": base_skill_version_id,
        })
        if bundle is not UNSET:
            field_dict["bundle"] = bundle
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("base_skill_version_id", (None, str(self.base_skill_version_id).encode(), "text/plain")))



        if not isinstance(self.bundle, Unset):
            files.append(("bundle", self.bundle.to_tuple()))



        if not isinstance(self.display_title, Unset):
            files.append(("display_title", (None, str(self.display_title).encode(), "text/plain")))



        if not isinstance(self.metadata, Unset):
            files.append(("metadata", (None, str(self.metadata).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base_skill_version_id = d.pop("base_skill_version_id")

        _bundle = d.pop("bundle", UNSET)
        bundle: File | Unset
        if isinstance(_bundle,  Unset):
            bundle = UNSET
        else:
            bundle = File(
             payload = BytesIO(_bundle)
        )




        display_title = d.pop("display_title", UNSET)

        metadata = d.pop("metadata", UNSET)

        managed_agents_form_data_skill_version_bundle_upload_request = cls(
            base_skill_version_id=base_skill_version_id,
            bundle=bundle,
            display_title=display_title,
            metadata=metadata,
        )


        managed_agents_form_data_skill_version_bundle_upload_request.additional_properties = d
        return managed_agents_form_data_skill_version_bundle_upload_request

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
