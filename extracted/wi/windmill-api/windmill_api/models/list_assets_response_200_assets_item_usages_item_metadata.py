from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAssetsResponse200AssetsItemUsagesItemMetadata")


@_attrs_define
class ListAssetsResponse200AssetsItemUsagesItemMetadata:
    """
    Attributes:
        runnable_path (Union[Unset, str]): The path of the script/flow that was run (only present when kind is 'job')
        job_kind (Union[Unset, str]): The kind of job (script, flow, preview, etc.) (only present when kind is 'job')
    """

    runnable_path: Union[Unset, str] = UNSET
    job_kind: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        runnable_path = self.runnable_path
        job_kind = self.job_kind

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if runnable_path is not UNSET:
            field_dict["runnable_path"] = runnable_path
        if job_kind is not UNSET:
            field_dict["job_kind"] = job_kind

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        runnable_path = d.pop("runnable_path", UNSET)

        job_kind = d.pop("job_kind", UNSET)

        list_assets_response_200_assets_item_usages_item_metadata = cls(
            runnable_path=runnable_path,
            job_kind=job_kind,
        )

        list_assets_response_200_assets_item_usages_item_metadata.additional_properties = d
        return list_assets_response_200_assets_item_usages_item_metadata

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
