from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunUpdate")


@attr.s(auto_attribs=True, repr=False)
class AssayRunUpdate:
    """  """

    _equipment_id: Union[Unset, None, str] = UNSET
    _fields: Union[Unset, Fields] = UNSET

    def __repr__(self):
        fields = []
        fields.append("equipment_id={}".format(repr(self._equipment_id)))
        fields.append("fields={}".format(repr(self._fields)))
        return "AssayRunUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        equipment_id = self._equipment_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if equipment_id is not UNSET:
            field_dict["equipmentId"] = equipment_id
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_equipment_id() -> Union[Unset, None, str]:
            equipment_id = d.pop("equipmentId")
            return equipment_id

        try:
            equipment_id = get_equipment_id()
        except KeyError:
            if strict:
                raise
            equipment_id = cast(Union[Unset, None, str], UNSET)

        def get_fields() -> Union[Unset, Fields]:
            fields: Union[Unset, Union[Unset, Fields]] = UNSET
            _fields = d.pop("fields")

            if not isinstance(_fields, Unset):
                fields = Fields.from_dict(_fields)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, Fields], UNSET)

        assay_run_update = cls(
            equipment_id=equipment_id,
            fields=fields,
        )

        return assay_run_update

    @property
    def equipment_id(self) -> Optional[str]:
        """ The equipment that the assay run should be associated with.  This attribute is only supported if the equipment feature is enabled for the tenant; otherwise, supplying it leads to a 400 request error """
        if isinstance(self._equipment_id, Unset):
            raise NotPresentError(self, "equipment_id")
        return self._equipment_id

    @equipment_id.setter
    def equipment_id(self, value: Optional[str]) -> None:
        self._equipment_id = value

    @equipment_id.deleter
    def equipment_id(self) -> None:
        self._equipment_id = UNSET

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET
