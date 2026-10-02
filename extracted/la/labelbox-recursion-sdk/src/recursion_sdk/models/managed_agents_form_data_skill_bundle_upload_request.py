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






T = TypeVar("T", bound="ManagedAgentsFormDataSkillBundleUploadRequest")



@_attrs_define
class ManagedAgentsFormDataSkillBundleUploadRequest:
    """ Multipart body carrying a zipped skill directory in the bundle part. The document, name and description still come
    from the archive's SKILL.md.

        Example:
            {'bundle': 'example', 'display_title': 'example', 'metadata': 'example', 'skill_group_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            bundle (File | Unset): A zipped skill directory: SKILL.md at its root or one level down, plus optional scripts/,
                references/ and assets/. Files under scripts/ are mounted executable.
            display_title (str | Unset): Human-readable title for listings. Defaults to the frontmatter name.
            metadata (str | Unset): Caller-owned key/value data as a JSON object, since a form part cannot carry structure.
                Rejected rather than dropped when it does not parse.
            skill_group_id (str | Unset): Catalog group to file this skill under. Present and empty removes it from its
                group; omit the part to leave the group unchanged.
     """

    bundle: File | Unset = UNSET
    display_title: str | Unset = UNSET
    metadata: str | Unset = UNSET
    skill_group_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bundle: FileTypes | Unset = UNSET
        if not isinstance(self.bundle, Unset):
            bundle = self.bundle.to_tuple()


        display_title = self.display_title

        metadata = self.metadata

        skill_group_id = self.skill_group_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if bundle is not UNSET:
            field_dict["bundle"] = bundle
        if display_title is not UNSET:
            field_dict["display_title"] = display_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if skill_group_id is not UNSET:
            field_dict["skill_group_id"] = skill_group_id

        return field_dict


    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.bundle, Unset):
            files.append(("bundle", self.bundle.to_tuple()))



        if not isinstance(self.display_title, Unset):
            files.append(("display_title", (None, str(self.display_title).encode(), "text/plain")))



        if not isinstance(self.metadata, Unset):
            files.append(("metadata", (None, str(self.metadata).encode(), "text/plain")))



        if not isinstance(self.skill_group_id, Unset):
            files.append(("skill_group_id", (None, str(self.skill_group_id).encode(), "text/plain")))




        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))



        return files


    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
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

        skill_group_id = d.pop("skill_group_id", UNSET)

        managed_agents_form_data_skill_bundle_upload_request = cls(
            bundle=bundle,
            display_title=display_title,
            metadata=metadata,
            skill_group_id=skill_group_id,
        )


        managed_agents_form_data_skill_bundle_upload_request.additional_properties = d
        return managed_agents_form_data_skill_bundle_upload_request

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
