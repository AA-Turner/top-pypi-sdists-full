from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_review_process_stages_item_reviewers_item_status import (
    EntryReviewProcessStagesItemReviewersItemStatus,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryReviewProcessStagesItemReviewersItem")


@attr.s(auto_attribs=True, repr=False)
class EntryReviewProcessStagesItemReviewersItem:
    """  """

    _status: Union[Unset, EntryReviewProcessStagesItemReviewersItemStatus] = UNSET
    _handle: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("status={}".format(repr(self._status)))
        fields.append("handle={}".format(repr(self._handle)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryReviewProcessStagesItemReviewersItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        handle = self._handle
        id = self._id
        name = self._name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if status is not UNSET:
            field_dict["status"] = status
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_status() -> Union[Unset, EntryReviewProcessStagesItemReviewersItemStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = EntryReviewProcessStagesItemReviewersItemStatus(_status)
                except ValueError:
                    status = EntryReviewProcessStagesItemReviewersItemStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, EntryReviewProcessStagesItemReviewersItemStatus], UNSET)

        def get_handle() -> Union[Unset, str]:
            handle = d.pop("handle")
            return handle

        try:
            handle = get_handle()
        except KeyError:
            if strict:
                raise
            handle = cast(Union[Unset, str], UNSET)

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

        entry_review_process_stages_item_reviewers_item = cls(
            status=status,
            handle=handle,
            id=id,
            name=name,
        )

        entry_review_process_stages_item_reviewers_item.additional_properties = d
        return entry_review_process_stages_item_reviewers_item

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
    def status(self) -> EntryReviewProcessStagesItemReviewersItemStatus:
        """ Status of the Reviewer """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: EntryReviewProcessStagesItemReviewersItemStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET

    @property
    def handle(self) -> str:
        if isinstance(self._handle, Unset):
            raise NotPresentError(self, "handle")
        return self._handle

    @handle.setter
    def handle(self, value: str) -> None:
        self._handle = value

    @handle.deleter
    def handle(self) -> None:
        self._handle = UNSET

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
