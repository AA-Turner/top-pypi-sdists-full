import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_software_target import NestedSoftwareTarget
    from ..models.nested_software_version_module import NestedSoftwareVersionModule
    from ..models.nested_software_version_toolchain import NestedSoftwareVersionToolchain


T = TypeVar("T", bound="NestedSoftwareVersion")


@_attrs_define
class NestedSoftwareVersion:
    """
    Attributes:
        uuid (UUID):
        version (str):
        targets (list['NestedSoftwareTarget']):
        module (NestedSoftwareVersionModule):
        required_modules (list[Any]):
        extensions (list[Any]):
        toolchain (NestedSoftwareVersionToolchain):
        toolchain_families_compatibility (list[Any]):
        release_date (Union[None, Unset, datetime.date]):
    """

    uuid: UUID
    version: str
    targets: list["NestedSoftwareTarget"]
    module: "NestedSoftwareVersionModule"
    required_modules: list[Any]
    extensions: list[Any]
    toolchain: "NestedSoftwareVersionToolchain"
    toolchain_families_compatibility: list[Any]
    release_date: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        version = self.version

        targets = []
        for targets_item_data in self.targets:
            targets_item = targets_item_data.to_dict()
            targets.append(targets_item)

        module = self.module.to_dict()

        required_modules = self.required_modules

        extensions = self.extensions

        toolchain = self.toolchain.to_dict()

        toolchain_families_compatibility = self.toolchain_families_compatibility

        release_date: Union[None, Unset, str]
        if isinstance(self.release_date, Unset):
            release_date = UNSET
        elif isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "version": version,
                "targets": targets,
                "module": module,
                "required_modules": required_modules,
                "extensions": extensions,
                "toolchain": toolchain,
                "toolchain_families_compatibility": toolchain_families_compatibility,
            }
        )
        if release_date is not UNSET:
            field_dict["release_date"] = release_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_software_target import NestedSoftwareTarget
        from ..models.nested_software_version_module import NestedSoftwareVersionModule
        from ..models.nested_software_version_toolchain import NestedSoftwareVersionToolchain

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        version = d.pop("version")

        targets = []
        _targets = d.pop("targets")
        for targets_item_data in _targets:
            targets_item = NestedSoftwareTarget.from_dict(targets_item_data)

            targets.append(targets_item)

        module = NestedSoftwareVersionModule.from_dict(d.pop("module"))

        required_modules = cast(list[Any], d.pop("required_modules"))

        extensions = cast(list[Any], d.pop("extensions"))

        toolchain = NestedSoftwareVersionToolchain.from_dict(d.pop("toolchain"))

        toolchain_families_compatibility = cast(list[Any], d.pop("toolchain_families_compatibility"))

        def _parse_release_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_date_type_0 = isoparse(data).date()

                return release_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        release_date = _parse_release_date(d.pop("release_date", UNSET))

        nested_software_version = cls(
            uuid=uuid,
            version=version,
            targets=targets,
            module=module,
            required_modules=required_modules,
            extensions=extensions,
            toolchain=toolchain,
            toolchain_families_compatibility=toolchain_families_compatibility,
            release_date=release_date,
        )

        nested_software_version.additional_properties = d
        return nested_software_version

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
