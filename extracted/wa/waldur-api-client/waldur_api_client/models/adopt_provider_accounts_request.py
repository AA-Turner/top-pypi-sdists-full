from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.adopt_provider_accounts_request_resolutions import AdoptProviderAccountsRequestResolutions


T = TypeVar("T", bound="AdoptProviderAccountsRequest")


@_attrs_define
class AdoptProviderAccountsRequest:
    """
    Attributes:
        resolutions (Union[Unset, AdoptProviderAccountsRequestResolutions]): User UUID (hex) to the username that
            survives adoption. Only needed for users reported by the 'username_conflicts' action.
    """

    resolutions: Union[Unset, "AdoptProviderAccountsRequestResolutions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resolutions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resolutions, Unset):
            resolutions = self.resolutions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if resolutions is not UNSET:
            field_dict["resolutions"] = resolutions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.adopt_provider_accounts_request_resolutions import AdoptProviderAccountsRequestResolutions

        d = dict(src_dict)
        _resolutions = d.pop("resolutions", UNSET)
        resolutions: Union[Unset, AdoptProviderAccountsRequestResolutions]
        if isinstance(_resolutions, Unset):
            resolutions = UNSET
        else:
            resolutions = AdoptProviderAccountsRequestResolutions.from_dict(_resolutions)

        adopt_provider_accounts_request = cls(
            resolutions=resolutions,
        )

        adopt_provider_accounts_request.additional_properties = d
        return adopt_provider_accounts_request

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
