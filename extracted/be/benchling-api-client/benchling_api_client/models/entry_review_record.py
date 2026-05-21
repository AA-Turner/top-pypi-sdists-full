from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_review_process import EntryReviewProcess
from ..models.entry_review_record_status import EntryReviewRecordStatus
from ..models.review_change import ReviewChange
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryReviewRecord")


@attr.s(auto_attribs=True, repr=False)
class EntryReviewRecord:
    """ Review record if set """

    _comment: Union[Unset, str] = UNSET
    _review_changes: Union[Unset, List[ReviewChange]] = UNSET
    _review_processes: Union[Unset, None, List[EntryReviewProcess]] = UNSET
    _status: Union[Unset, EntryReviewRecordStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("comment={}".format(repr(self._comment)))
        fields.append("review_changes={}".format(repr(self._review_changes)))
        fields.append("review_processes={}".format(repr(self._review_processes)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryReviewRecord({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        comment = self._comment
        review_changes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._review_changes, Unset):
            review_changes = []
            for review_changes_item_data in self._review_changes:
                review_changes_item = review_changes_item_data.to_dict()

                review_changes.append(review_changes_item)

        review_processes: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._review_processes, Unset):
            if self._review_processes is None:
                review_processes = None
            else:
                review_processes = []
                for review_processes_item_data in self._review_processes:
                    review_processes_item = review_processes_item_data.to_dict()

                    review_processes.append(review_processes_item)

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if comment is not UNSET:
            field_dict["comment"] = comment
        if review_changes is not UNSET:
            field_dict["reviewChanges"] = review_changes
        if review_processes is not UNSET:
            field_dict["reviewProcesses"] = review_processes
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_comment() -> Union[Unset, str]:
            comment = d.pop("comment")
            return comment

        try:
            comment = get_comment()
        except KeyError:
            if strict:
                raise
            comment = cast(Union[Unset, str], UNSET)

        def get_review_changes() -> Union[Unset, List[ReviewChange]]:
            review_changes = []
            _review_changes = d.pop("reviewChanges")
            for review_changes_item_data in _review_changes or []:
                review_changes_item = ReviewChange.from_dict(review_changes_item_data, strict=False)

                review_changes.append(review_changes_item)

            return review_changes

        try:
            review_changes = get_review_changes()
        except KeyError:
            if strict:
                raise
            review_changes = cast(Union[Unset, List[ReviewChange]], UNSET)

        def get_review_processes() -> Union[Unset, None, List[EntryReviewProcess]]:
            review_processes = []
            _review_processes = d.pop("reviewProcesses")
            for review_processes_item_data in _review_processes or []:
                review_processes_item = EntryReviewProcess.from_dict(review_processes_item_data, strict=False)

                review_processes.append(review_processes_item)

            return review_processes

        try:
            review_processes = get_review_processes()
        except KeyError:
            if strict:
                raise
            review_processes = cast(Union[Unset, None, List[EntryReviewProcess]], UNSET)

        def get_status() -> Union[Unset, EntryReviewRecordStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = EntryReviewRecordStatus(_status)
                except ValueError:
                    status = EntryReviewRecordStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, EntryReviewRecordStatus], UNSET)

        entry_review_record = cls(
            comment=comment,
            review_changes=review_changes,
            review_processes=review_processes,
            status=status,
        )

        entry_review_record.additional_properties = d
        return entry_review_record

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
    def comment(self) -> str:
        """ Reviewer's Comments """
        if isinstance(self._comment, Unset):
            raise NotPresentError(self, "comment")
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:
        self._comment = value

    @comment.deleter
    def comment(self) -> None:
        self._comment = UNSET

    @property
    def review_changes(self) -> List[ReviewChange]:
        """ A list of the Review Changes that have been made to this entry """
        if isinstance(self._review_changes, Unset):
            raise NotPresentError(self, "review_changes")
        return self._review_changes

    @review_changes.setter
    def review_changes(self, value: List[ReviewChange]) -> None:
        self._review_changes = value

    @review_changes.deleter
    def review_changes(self) -> None:
        self._review_changes = UNSET

    @property
    def review_processes(self) -> Optional[List[EntryReviewProcess]]:
        """ Review Processes associated with the Entry """
        if isinstance(self._review_processes, Unset):
            raise NotPresentError(self, "review_processes")
        return self._review_processes

    @review_processes.setter
    def review_processes(self, value: Optional[List[EntryReviewProcess]]) -> None:
        self._review_processes = value

    @review_processes.deleter
    def review_processes(self) -> None:
        self._review_processes = UNSET

    @property
    def status(self) -> EntryReviewRecordStatus:
        """ Review Status of the entry """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: EntryReviewRecordStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
