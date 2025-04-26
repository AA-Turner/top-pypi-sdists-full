from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..types import UNSET, Unset

T = TypeVar("T", bound="Unit")


@attr.s(auto_attribs=True, repr=False)
class Unit:
    """  """

    _aliases: Union[Unset, List[str]] = UNSET
    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _conversion_factor: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _symbol: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("conversion_factor={}".format(repr(self._conversion_factor)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("symbol={}".format(repr(self._symbol)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Unit({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aliases, Unset):
            aliases = self._aliases

        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        conversion_factor = self._conversion_factor
        id = self._id
        name = self._name
        symbol = self._symbol

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if conversion_factor is not UNSET:
            field_dict["conversionFactor"] = conversion_factor
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if symbol is not UNSET:
            field_dict["symbol"] = symbol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_aliases() -> Union[Unset, List[str]]:
            aliases = cast(List[str], d.pop("aliases"))

            return aliases

        try:
            aliases = get_aliases()
        except KeyError:
            if strict:
                raise
            aliases = cast(Union[Unset, List[str]], UNSET)

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

        def get_conversion_factor() -> Union[Unset, str]:
            conversion_factor = d.pop("conversionFactor")
            return conversion_factor

        try:
            conversion_factor = get_conversion_factor()
        except KeyError:
            if strict:
                raise
            conversion_factor = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_symbol() -> Union[Unset, str]:
            symbol = d.pop("symbol")
            return symbol

        try:
            symbol = get_symbol()
        except KeyError:
            if strict:
                raise
            symbol = cast(Union[Unset, str], UNSET)

        unit = cls(
            aliases=aliases,
            archive_record=archive_record,
            conversion_factor=conversion_factor,
            id=id,
            name=name,
            symbol=symbol,
        )

        unit.additional_properties = d
        return unit

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
    def aliases(self) -> List[str]:
        if isinstance(self._aliases, Unset):
            raise NotPresentError(self, "aliases")
        return self._aliases

    @aliases.setter
    def aliases(self, value: List[str]) -> None:
        self._aliases = value

    @aliases.deleter
    def aliases(self) -> None:
        self._aliases = UNSET

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
    def conversion_factor(self) -> str:
        """ A decimal string relating this unit to its type's base unit """
        if isinstance(self._conversion_factor, Unset):
            raise NotPresentError(self, "conversion_factor")
        return self._conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value: str) -> None:
        self._conversion_factor = value

    @conversion_factor.deleter
    def conversion_factor(self) -> None:
        self._conversion_factor = UNSET

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

    @property
    def symbol(self) -> str:
        if isinstance(self._symbol, Unset):
            raise NotPresentError(self, "symbol")
        return self._symbol

    @symbol.setter
    def symbol(self, value: str) -> None:
        self._symbol = value

    @symbol.deleter
    def symbol(self) -> None:
        self._symbol = UNSET
