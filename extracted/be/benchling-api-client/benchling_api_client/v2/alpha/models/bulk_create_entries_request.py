from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_create_attachments import EntryCreateAttachments
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkCreateEntriesRequest")


@attr.s(auto_attribs=True, repr=False)
class BulkCreateEntriesRequest:
    """  """

    _entry_datas: Union[Unset, List[EntryCreateAttachments]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("entry_datas={}".format(repr(self._entry_datas)))
        return "BulkCreateEntriesRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        entry_datas: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._entry_datas, Unset):
            entry_datas = []
            for entry_datas_item_data in self._entry_datas:
                entry_datas_item = entry_datas_item_data.to_dict()

                entry_datas.append(entry_datas_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if entry_datas is not UNSET:
            field_dict["entryDatas"] = entry_datas

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_entry_datas() -> Union[Unset, List[EntryCreateAttachments]]:
            entry_datas = []
            _entry_datas = d.pop("entryDatas")
            for entry_datas_item_data in _entry_datas or []:
                entry_datas_item = EntryCreateAttachments.from_dict(entry_datas_item_data, strict=False)

                entry_datas.append(entry_datas_item)

            return entry_datas

        try:
            entry_datas = get_entry_datas()
        except KeyError:
            if strict:
                raise
            entry_datas = cast(Union[Unset, List[EntryCreateAttachments]], UNSET)

        bulk_create_entries_request = cls(
            entry_datas=entry_datas,
        )

        return bulk_create_entries_request

    @property
    def entry_datas(self) -> List[EntryCreateAttachments]:
        if isinstance(self._entry_datas, Unset):
            raise NotPresentError(self, "entry_datas")
        return self._entry_datas

    @entry_datas.setter
    def entry_datas(self, value: List[EntryCreateAttachments]) -> None:
        self._entry_datas = value

    @entry_datas.deleter
    def entry_datas(self) -> None:
        self._entry_datas = UNSET
