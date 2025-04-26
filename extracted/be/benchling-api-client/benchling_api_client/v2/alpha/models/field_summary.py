from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.field_summary_link import FieldSummaryLink
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldSummary")


@attr.s(auto_attribs=True, repr=False)
class FieldSummary:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _decimal_precision: Union[Unset, None, str] = UNSET
    _dropdown_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _is_computed: Union[Unset, bool] = UNSET
    _is_converted_from_link: Union[Unset, bool] = UNSET
    _is_integration: Union[Unset, bool] = UNSET
    _is_single_link: Union[Unset, bool] = UNSET
    _is_snapshot: Union[Unset, bool] = UNSET
    _is_uneditable: Union[Unset, bool] = UNSET
    _legal_text_dropdown_id: Union[Unset, None, str] = UNSET
    _link: Union[Unset, None, FieldSummaryLink] = UNSET
    _numeric_max: Union[Unset, None, str] = UNSET
    _numeric_min: Union[Unset, None, str] = UNSET
    _strict_selector: Union[Unset, bool] = UNSET
    _system_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("decimal_precision={}".format(repr(self._decimal_precision)))
        fields.append("dropdown_id={}".format(repr(self._dropdown_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_computed={}".format(repr(self._is_computed)))
        fields.append("is_converted_from_link={}".format(repr(self._is_converted_from_link)))
        fields.append("is_integration={}".format(repr(self._is_integration)))
        fields.append("is_single_link={}".format(repr(self._is_single_link)))
        fields.append("is_snapshot={}".format(repr(self._is_snapshot)))
        fields.append("is_uneditable={}".format(repr(self._is_uneditable)))
        fields.append("legal_text_dropdown_id={}".format(repr(self._legal_text_dropdown_id)))
        fields.append("link={}".format(repr(self._link)))
        fields.append("numeric_max={}".format(repr(self._numeric_max)))
        fields.append("numeric_min={}".format(repr(self._numeric_min)))
        fields.append("strict_selector={}".format(repr(self._strict_selector)))
        fields.append("system_name={}".format(repr(self._system_name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FieldSummary({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        decimal_precision = self._decimal_precision
        dropdown_id = self._dropdown_id
        id = self._id
        is_computed = self._is_computed
        is_converted_from_link = self._is_converted_from_link
        is_integration = self._is_integration
        is_single_link = self._is_single_link
        is_snapshot = self._is_snapshot
        is_uneditable = self._is_uneditable
        legal_text_dropdown_id = self._legal_text_dropdown_id
        link: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._link, Unset):
            link = self._link.to_dict() if self._link else None

        numeric_max = self._numeric_max
        numeric_min = self._numeric_min
        strict_selector = self._strict_selector
        system_name = self._system_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if decimal_precision is not UNSET:
            field_dict["decimalPrecision"] = decimal_precision
        if dropdown_id is not UNSET:
            field_dict["dropdownId"] = dropdown_id
        if id is not UNSET:
            field_dict["id"] = id
        if is_computed is not UNSET:
            field_dict["isComputed"] = is_computed
        if is_converted_from_link is not UNSET:
            field_dict["isConvertedFromLink"] = is_converted_from_link
        if is_integration is not UNSET:
            field_dict["isIntegration"] = is_integration
        if is_single_link is not UNSET:
            field_dict["isSingleLink"] = is_single_link
        if is_snapshot is not UNSET:
            field_dict["isSnapshot"] = is_snapshot
        if is_uneditable is not UNSET:
            field_dict["isUneditable"] = is_uneditable
        if legal_text_dropdown_id is not UNSET:
            field_dict["legalTextDropdownId"] = legal_text_dropdown_id
        if link is not UNSET:
            field_dict["link"] = link
        if numeric_max is not UNSET:
            field_dict["numericMax"] = numeric_max
        if numeric_min is not UNSET:
            field_dict["numericMin"] = numeric_min
        if strict_selector is not UNSET:
            field_dict["strictSelector"] = strict_selector
        if system_name is not UNSET:
            field_dict["systemName"] = system_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

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

        def get_decimal_precision() -> Union[Unset, None, str]:
            decimal_precision = d.pop("decimalPrecision")
            return decimal_precision

        try:
            decimal_precision = get_decimal_precision()
        except KeyError:
            if strict:
                raise
            decimal_precision = cast(Union[Unset, None, str], UNSET)

        def get_dropdown_id() -> Union[Unset, str]:
            dropdown_id = d.pop("dropdownId")
            return dropdown_id

        try:
            dropdown_id = get_dropdown_id()
        except KeyError:
            if strict:
                raise
            dropdown_id = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_is_computed() -> Union[Unset, bool]:
            is_computed = d.pop("isComputed")
            return is_computed

        try:
            is_computed = get_is_computed()
        except KeyError:
            if strict:
                raise
            is_computed = cast(Union[Unset, bool], UNSET)

        def get_is_converted_from_link() -> Union[Unset, bool]:
            is_converted_from_link = d.pop("isConvertedFromLink")
            return is_converted_from_link

        try:
            is_converted_from_link = get_is_converted_from_link()
        except KeyError:
            if strict:
                raise
            is_converted_from_link = cast(Union[Unset, bool], UNSET)

        def get_is_integration() -> Union[Unset, bool]:
            is_integration = d.pop("isIntegration")
            return is_integration

        try:
            is_integration = get_is_integration()
        except KeyError:
            if strict:
                raise
            is_integration = cast(Union[Unset, bool], UNSET)

        def get_is_single_link() -> Union[Unset, bool]:
            is_single_link = d.pop("isSingleLink")
            return is_single_link

        try:
            is_single_link = get_is_single_link()
        except KeyError:
            if strict:
                raise
            is_single_link = cast(Union[Unset, bool], UNSET)

        def get_is_snapshot() -> Union[Unset, bool]:
            is_snapshot = d.pop("isSnapshot")
            return is_snapshot

        try:
            is_snapshot = get_is_snapshot()
        except KeyError:
            if strict:
                raise
            is_snapshot = cast(Union[Unset, bool], UNSET)

        def get_is_uneditable() -> Union[Unset, bool]:
            is_uneditable = d.pop("isUneditable")
            return is_uneditable

        try:
            is_uneditable = get_is_uneditable()
        except KeyError:
            if strict:
                raise
            is_uneditable = cast(Union[Unset, bool], UNSET)

        def get_legal_text_dropdown_id() -> Union[Unset, None, str]:
            legal_text_dropdown_id = d.pop("legalTextDropdownId")
            return legal_text_dropdown_id

        try:
            legal_text_dropdown_id = get_legal_text_dropdown_id()
        except KeyError:
            if strict:
                raise
            legal_text_dropdown_id = cast(Union[Unset, None, str], UNSET)

        def get_link() -> Union[Unset, None, FieldSummaryLink]:
            link = None
            _link = d.pop("link")

            if _link is not None and not isinstance(_link, Unset):
                link = FieldSummaryLink.from_dict(_link)

            return link

        try:
            link = get_link()
        except KeyError:
            if strict:
                raise
            link = cast(Union[Unset, None, FieldSummaryLink], UNSET)

        def get_numeric_max() -> Union[Unset, None, str]:
            numeric_max = d.pop("numericMax")
            return numeric_max

        try:
            numeric_max = get_numeric_max()
        except KeyError:
            if strict:
                raise
            numeric_max = cast(Union[Unset, None, str], UNSET)

        def get_numeric_min() -> Union[Unset, None, str]:
            numeric_min = d.pop("numericMin")
            return numeric_min

        try:
            numeric_min = get_numeric_min()
        except KeyError:
            if strict:
                raise
            numeric_min = cast(Union[Unset, None, str], UNSET)

        def get_strict_selector() -> Union[Unset, bool]:
            strict_selector = d.pop("strictSelector")
            return strict_selector

        try:
            strict_selector = get_strict_selector()
        except KeyError:
            if strict:
                raise
            strict_selector = cast(Union[Unset, bool], UNSET)

        def get_system_name() -> Union[Unset, str]:
            system_name = d.pop("systemName")
            return system_name

        try:
            system_name = get_system_name()
        except KeyError:
            if strict:
                raise
            system_name = cast(Union[Unset, str], UNSET)

        field_summary = cls(
            archive_record=archive_record,
            decimal_precision=decimal_precision,
            dropdown_id=dropdown_id,
            id=id,
            is_computed=is_computed,
            is_converted_from_link=is_converted_from_link,
            is_integration=is_integration,
            is_single_link=is_single_link,
            is_snapshot=is_snapshot,
            is_uneditable=is_uneditable,
            legal_text_dropdown_id=legal_text_dropdown_id,
            link=link,
            numeric_max=numeric_max,
            numeric_min=numeric_min,
            strict_selector=strict_selector,
            system_name=system_name,
        )

        field_summary.additional_properties = d
        return field_summary

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
    def decimal_precision(self) -> Optional[str]:
        if isinstance(self._decimal_precision, Unset):
            raise NotPresentError(self, "decimal_precision")
        return self._decimal_precision

    @decimal_precision.setter
    def decimal_precision(self, value: Optional[str]) -> None:
        self._decimal_precision = value

    @decimal_precision.deleter
    def decimal_precision(self) -> None:
        self._decimal_precision = UNSET

    @property
    def dropdown_id(self) -> str:
        if isinstance(self._dropdown_id, Unset):
            raise NotPresentError(self, "dropdown_id")
        return self._dropdown_id

    @dropdown_id.setter
    def dropdown_id(self, value: str) -> None:
        self._dropdown_id = value

    @dropdown_id.deleter
    def dropdown_id(self) -> None:
        self._dropdown_id = UNSET

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
    def is_computed(self) -> bool:
        if isinstance(self._is_computed, Unset):
            raise NotPresentError(self, "is_computed")
        return self._is_computed

    @is_computed.setter
    def is_computed(self, value: bool) -> None:
        self._is_computed = value

    @is_computed.deleter
    def is_computed(self) -> None:
        self._is_computed = UNSET

    @property
    def is_converted_from_link(self) -> bool:
        if isinstance(self._is_converted_from_link, Unset):
            raise NotPresentError(self, "is_converted_from_link")
        return self._is_converted_from_link

    @is_converted_from_link.setter
    def is_converted_from_link(self, value: bool) -> None:
        self._is_converted_from_link = value

    @is_converted_from_link.deleter
    def is_converted_from_link(self) -> None:
        self._is_converted_from_link = UNSET

    @property
    def is_integration(self) -> bool:
        if isinstance(self._is_integration, Unset):
            raise NotPresentError(self, "is_integration")
        return self._is_integration

    @is_integration.setter
    def is_integration(self, value: bool) -> None:
        self._is_integration = value

    @is_integration.deleter
    def is_integration(self) -> None:
        self._is_integration = UNSET

    @property
    def is_single_link(self) -> bool:
        if isinstance(self._is_single_link, Unset):
            raise NotPresentError(self, "is_single_link")
        return self._is_single_link

    @is_single_link.setter
    def is_single_link(self, value: bool) -> None:
        self._is_single_link = value

    @is_single_link.deleter
    def is_single_link(self) -> None:
        self._is_single_link = UNSET

    @property
    def is_snapshot(self) -> bool:
        if isinstance(self._is_snapshot, Unset):
            raise NotPresentError(self, "is_snapshot")
        return self._is_snapshot

    @is_snapshot.setter
    def is_snapshot(self, value: bool) -> None:
        self._is_snapshot = value

    @is_snapshot.deleter
    def is_snapshot(self) -> None:
        self._is_snapshot = UNSET

    @property
    def is_uneditable(self) -> bool:
        if isinstance(self._is_uneditable, Unset):
            raise NotPresentError(self, "is_uneditable")
        return self._is_uneditable

    @is_uneditable.setter
    def is_uneditable(self, value: bool) -> None:
        self._is_uneditable = value

    @is_uneditable.deleter
    def is_uneditable(self) -> None:
        self._is_uneditable = UNSET

    @property
    def legal_text_dropdown_id(self) -> Optional[str]:
        if isinstance(self._legal_text_dropdown_id, Unset):
            raise NotPresentError(self, "legal_text_dropdown_id")
        return self._legal_text_dropdown_id

    @legal_text_dropdown_id.setter
    def legal_text_dropdown_id(self, value: Optional[str]) -> None:
        self._legal_text_dropdown_id = value

    @legal_text_dropdown_id.deleter
    def legal_text_dropdown_id(self) -> None:
        self._legal_text_dropdown_id = UNSET

    @property
    def link(self) -> Optional[FieldSummaryLink]:
        if isinstance(self._link, Unset):
            raise NotPresentError(self, "link")
        return self._link

    @link.setter
    def link(self, value: Optional[FieldSummaryLink]) -> None:
        self._link = value

    @link.deleter
    def link(self) -> None:
        self._link = UNSET

    @property
    def numeric_max(self) -> Optional[str]:
        if isinstance(self._numeric_max, Unset):
            raise NotPresentError(self, "numeric_max")
        return self._numeric_max

    @numeric_max.setter
    def numeric_max(self, value: Optional[str]) -> None:
        self._numeric_max = value

    @numeric_max.deleter
    def numeric_max(self) -> None:
        self._numeric_max = UNSET

    @property
    def numeric_min(self) -> Optional[str]:
        if isinstance(self._numeric_min, Unset):
            raise NotPresentError(self, "numeric_min")
        return self._numeric_min

    @numeric_min.setter
    def numeric_min(self, value: Optional[str]) -> None:
        self._numeric_min = value

    @numeric_min.deleter
    def numeric_min(self) -> None:
        self._numeric_min = UNSET

    @property
    def strict_selector(self) -> bool:
        if isinstance(self._strict_selector, Unset):
            raise NotPresentError(self, "strict_selector")
        return self._strict_selector

    @strict_selector.setter
    def strict_selector(self, value: bool) -> None:
        self._strict_selector = value

    @strict_selector.deleter
    def strict_selector(self) -> None:
        self._strict_selector = UNSET

    @property
    def system_name(self) -> str:
        if isinstance(self._system_name, Unset):
            raise NotPresentError(self, "system_name")
        return self._system_name

    @system_name.setter
    def system_name(self, value: str) -> None:
        self._system_name = value

    @system_name.deleter
    def system_name(self) -> None:
        self._system_name = UNSET
