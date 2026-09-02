from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dbt_asset_provenance_data_tests_item_args import DbtAssetProvenanceDataTestsItemArgs


T = TypeVar("T", bound="DbtAssetProvenanceDataTestsItem")


@_attrs_define
class DbtAssetProvenanceDataTestsItem:
    """
    Attributes:
        kind (str): One of the four generic tests, or a package test's namespaced name (`dbt_utils.accepted_range`).
        column (Union[Unset, str]):
        args (Union[Unset, DbtAssetProvenanceDataTestsItemArgs]):
        severity (Union[Unset, str]): Lowercased. dbt's severity decides whether a failure fails the run.
    """

    kind: str
    column: Union[Unset, str] = UNSET
    args: Union[Unset, "DbtAssetProvenanceDataTestsItemArgs"] = UNSET
    severity: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind
        column = self.column
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        severity = self.severity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )
        if column is not UNSET:
            field_dict["column"] = column
        if args is not UNSET:
            field_dict["args"] = args
        if severity is not UNSET:
            field_dict["severity"] = severity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dbt_asset_provenance_data_tests_item_args import DbtAssetProvenanceDataTestsItemArgs

        d = src_dict.copy()
        kind = d.pop("kind")

        column = d.pop("column", UNSET)

        _args = d.pop("args", UNSET)
        args: Union[Unset, DbtAssetProvenanceDataTestsItemArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = DbtAssetProvenanceDataTestsItemArgs.from_dict(_args)

        severity = d.pop("severity", UNSET)

        dbt_asset_provenance_data_tests_item = cls(
            kind=kind,
            column=column,
            args=args,
            severity=severity,
        )

        dbt_asset_provenance_data_tests_item.additional_properties = d
        return dbt_asset_provenance_data_tests_item

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
