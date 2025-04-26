from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.integer_field_definition_type import IntegerFieldDefinitionType
from ..models.unit_summary import UnitSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegerFieldDefinition")


@attr.s(auto_attribs=True, repr=False)
class IntegerFieldDefinition:
    """  """

    _numeric_max: Union[Unset, None, float] = UNSET
    _numeric_min: Union[Unset, None, float] = UNSET
    _type: Union[Unset, IntegerFieldDefinitionType] = UNSET
    _unit: Union[Unset, None, UnitSummary] = UNSET
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _id: Union[Unset, str] = UNSET
    _is_multi: Union[Unset, bool] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("numeric_max={}".format(repr(self._numeric_max)))
        fields.append("numeric_min={}".format(repr(self._numeric_min)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("unit={}".format(repr(self._unit)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_multi={}".format(repr(self._is_multi)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "IntegerFieldDefinition({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        numeric_max = self._numeric_max
        numeric_min = self._numeric_min
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        unit: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._unit, Unset):
            unit = self._unit.to_dict() if self._unit else None

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        id = self._id
        is_multi = self._is_multi
        is_required = self._is_required
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if numeric_max is not UNSET:
            field_dict["numericMax"] = numeric_max
        if numeric_min is not UNSET:
            field_dict["numericMin"] = numeric_min
        if type is not UNSET:
            field_dict["type"] = type
        if unit is not UNSET:
            field_dict["unit"] = unit
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if id is not UNSET:
            field_dict["id"] = id
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_numeric_max() -> Union[Unset, None, float]:
            numeric_max = d.pop("numericMax")
            return numeric_max

        try:
            numeric_max = get_numeric_max()
        except KeyError:
            if strict:
                raise
            numeric_max = cast(Union[Unset, None, float], UNSET)

        def get_numeric_min() -> Union[Unset, None, float]:
            numeric_min = d.pop("numericMin")
            return numeric_min

        try:
            numeric_min = get_numeric_min()
        except KeyError:
            if strict:
                raise
            numeric_min = cast(Union[Unset, None, float], UNSET)

        def get_type() -> Union[Unset, IntegerFieldDefinitionType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = IntegerFieldDefinitionType(_type)
                except ValueError:
                    type = IntegerFieldDefinitionType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, IntegerFieldDefinitionType], UNSET)

        def get_unit() -> Union[Unset, None, UnitSummary]:
            unit = None
            _unit = d.pop("unit")

            if _unit is not None and not isinstance(_unit, Unset):
                unit = UnitSummary.from_dict(_unit)

            return unit

        try:
            unit = get_unit()
        except KeyError:
            if strict:
                raise
            unit = cast(Union[Unset, None, UnitSummary], UNSET)

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, ArchiveRecord], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_is_multi() -> Union[Unset, bool]:
            is_multi = d.pop("isMulti")
            return is_multi

        try:
            is_multi = get_is_multi()
        except KeyError:
            if strict:
                raise
            is_multi = cast(Union[Unset, bool], UNSET)

        def get_is_required() -> Union[Unset, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        integer_field_definition = cls(
            numeric_max=numeric_max,
            numeric_min=numeric_min,
            type=type,
            unit=unit,
            archive_record=archive_record,
            id=id,
            is_multi=is_multi,
            is_required=is_required,
            name=name,
        )

        integer_field_definition.additional_properties = d
        return integer_field_definition

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
    def numeric_max(self) -> Optional[float]:
        if isinstance(self._numeric_max, Unset):
            raise NotPresentError(self, "numeric_max")
        return self._numeric_max

    @numeric_max.setter
    def numeric_max(self, value: Optional[float]) -> None:
        self._numeric_max = value

    @numeric_max.deleter
    def numeric_max(self) -> None:
        self._numeric_max = UNSET

    @property
    def numeric_min(self) -> Optional[float]:
        if isinstance(self._numeric_min, Unset):
            raise NotPresentError(self, "numeric_min")
        return self._numeric_min

    @numeric_min.setter
    def numeric_min(self, value: Optional[float]) -> None:
        self._numeric_min = value

    @numeric_min.deleter
    def numeric_min(self) -> None:
        self._numeric_min = UNSET

    @property
    def type(self) -> IntegerFieldDefinitionType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: IntegerFieldDefinitionType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def unit(self) -> Optional[UnitSummary]:
        if isinstance(self._unit, Unset):
            raise NotPresentError(self, "unit")
        return self._unit

    @unit.setter
    def unit(self, value: Optional[UnitSummary]) -> None:
        self._unit = value

    @unit.deleter
    def unit(self) -> None:
        self._unit = UNSET

    @property
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def is_multi(self) -> bool:
        if isinstance(self._is_multi, Unset):
            raise NotPresentError(self, "is_multi")
        return self._is_multi

    @is_multi.setter
    def is_multi(self, value: bool) -> None:
        self._is_multi = value

    @is_multi.deleter
    def is_multi(self) -> None:
        self._is_multi = UNSET

    @property
    def is_required(self) -> bool:
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
