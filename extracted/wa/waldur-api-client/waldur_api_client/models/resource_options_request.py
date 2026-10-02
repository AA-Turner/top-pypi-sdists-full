from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_options_request_options_type_0 import ResourceOptionsRequestOptionsType0


T = TypeVar("T", bound="ResourceOptionsRequest")


@_attrs_define
class ResourceOptionsRequest:
    """
    Attributes:
        options (Union['ResourceOptionsRequestOptionsType0', None, Unset]):
    """

    options: Union["ResourceOptionsRequestOptionsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_options_request_options_type_0 import ResourceOptionsRequestOptionsType0

        options: Union[None, Unset, dict[str, Any]]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, ResourceOptionsRequestOptionsType0):
            options = self.options.to_dict()
        else:
            options = self.options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_options_request_options_type_0 import ResourceOptionsRequestOptionsType0

        d = dict(src_dict)

        def _parse_options(data: object) -> Union["ResourceOptionsRequestOptionsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = ResourceOptionsRequestOptionsType0.from_dict(data)

                return options_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceOptionsRequestOptionsType0", None, Unset], data)

        options = _parse_options(d.pop("options", UNSET))

        resource_options_request = cls(
            options=options,
        )

        resource_options_request.additional_properties = d
        return resource_options_request

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
