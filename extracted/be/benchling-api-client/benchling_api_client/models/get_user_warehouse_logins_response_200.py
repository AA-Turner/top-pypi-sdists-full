from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.warehouse_credential_summary import WarehouseCredentialSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetUserWarehouseLoginsResponse_200")


@attr.s(auto_attribs=True, repr=False)
class GetUserWarehouseLoginsResponse_200:
    """  """

    _warehouse_credentials: Union[Unset, List[WarehouseCredentialSummary]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("warehouse_credentials={}".format(repr(self._warehouse_credentials)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "GetUserWarehouseLoginsResponse_200({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        warehouse_credentials: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._warehouse_credentials, Unset):
            warehouse_credentials = []
            for warehouse_credentials_item_data in self._warehouse_credentials:
                warehouse_credentials_item = warehouse_credentials_item_data.to_dict()

                warehouse_credentials.append(warehouse_credentials_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if warehouse_credentials is not UNSET:
            field_dict["warehouseCredentials"] = warehouse_credentials

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_warehouse_credentials() -> Union[Unset, List[WarehouseCredentialSummary]]:
            warehouse_credentials = []
            _warehouse_credentials = d.pop("warehouseCredentials")
            for warehouse_credentials_item_data in _warehouse_credentials or []:
                warehouse_credentials_item = WarehouseCredentialSummary.from_dict(
                    warehouse_credentials_item_data, strict=False
                )

                warehouse_credentials.append(warehouse_credentials_item)

            return warehouse_credentials

        try:
            warehouse_credentials = get_warehouse_credentials()
        except KeyError:
            if strict:
                raise
            warehouse_credentials = cast(Union[Unset, List[WarehouseCredentialSummary]], UNSET)

        get_user_warehouse_logins_response_200 = cls(
            warehouse_credentials=warehouse_credentials,
        )

        get_user_warehouse_logins_response_200.additional_properties = d
        return get_user_warehouse_logins_response_200

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def warehouse_credentials(self) -> List[WarehouseCredentialSummary]:
        if isinstance(self._warehouse_credentials, Unset):
            raise NotPresentError(self, "warehouse_credentials")
        return self._warehouse_credentials

    @warehouse_credentials.setter
    def warehouse_credentials(self, value: List[WarehouseCredentialSummary]) -> None:
        self._warehouse_credentials = value

    @warehouse_credentials.deleter
    def warehouse_credentials(self) -> None:
        self._warehouse_credentials = UNSET
