from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_dbt_warehouses_json_body_dbt_warehouses import EditDbtWarehousesJsonBodyDbtWarehouses


T = TypeVar("T", bound="EditDbtWarehousesJsonBody")


@_attrs_define
class EditDbtWarehousesJsonBody:
    """
    Attributes:
        dbt_warehouses (Union[Unset, EditDbtWarehousesJsonBodyDbtWarehouses]): Warehouses a dbt project may run against,
            by name. `main` is the one a project gets when its descriptor names none. Each entry points at a resource; it
            never holds credentials.
    """

    dbt_warehouses: Union[Unset, "EditDbtWarehousesJsonBodyDbtWarehouses"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dbt_warehouses: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dbt_warehouses, Unset):
            dbt_warehouses = self.dbt_warehouses.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dbt_warehouses is not UNSET:
            field_dict["dbt_warehouses"] = dbt_warehouses

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_dbt_warehouses_json_body_dbt_warehouses import EditDbtWarehousesJsonBodyDbtWarehouses

        d = src_dict.copy()
        _dbt_warehouses = d.pop("dbt_warehouses", UNSET)
        dbt_warehouses: Union[Unset, EditDbtWarehousesJsonBodyDbtWarehouses]
        if isinstance(_dbt_warehouses, Unset):
            dbt_warehouses = UNSET
        else:
            dbt_warehouses = EditDbtWarehousesJsonBodyDbtWarehouses.from_dict(_dbt_warehouses)

        edit_dbt_warehouses_json_body = cls(
            dbt_warehouses=dbt_warehouses,
        )

        edit_dbt_warehouses_json_body.additional_properties = d
        return edit_dbt_warehouses_json_body

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
