from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.constraint_status_status import ConstraintStatusStatus
from ..models.field_definition import FieldDefinition
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstraintStatus")


@attr.s(auto_attribs=True, repr=False)
class ConstraintStatus:
    """  """

    _fields: Union[Unset, List[FieldDefinition]] = UNSET
    _status: Union[Unset, ConstraintStatusStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ConstraintStatus({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = []
            for fields_item_data in self._fields:
                fields_item = fields_item_data.to_dict()

                fields.append(fields_item)

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fields is not UNSET:
            field_dict["fields"] = fields
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_fields() -> Union[Unset, List[FieldDefinition]]:
            fields = []
            _fields = d.pop("fields")
            for fields_item_data in _fields or []:
                fields_item = FieldDefinition.from_dict(fields_item_data, strict=False)

                fields.append(fields_item)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, List[FieldDefinition]], UNSET)

        def get_status() -> Union[Unset, ConstraintStatusStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = ConstraintStatusStatus(_status)
                except ValueError:
                    status = ConstraintStatusStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, ConstraintStatusStatus], UNSET)

        constraint_status = cls(
            fields=fields,
            status=status,
        )

        constraint_status.additional_properties = d
        return constraint_status

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
    def fields(self) -> List[FieldDefinition]:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: List[FieldDefinition]) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def status(self) -> ConstraintStatusStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: ConstraintStatusStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
