from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_create_attachments_review_record_status import EntryCreateAttachmentsReviewRecordStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryCreateAttachmentsReviewRecord")


@attr.s(auto_attribs=True, repr=False)
class EntryCreateAttachmentsReviewRecord:
    """  """

    _comment: Union[Unset, str] = UNSET
    _status: Union[Unset, EntryCreateAttachmentsReviewRecordStatus] = UNSET

    def __repr__(self):
        fields = []
        fields.append("comment={}".format(repr(self._comment)))
        fields.append("status={}".format(repr(self._status)))
        return "EntryCreateAttachmentsReviewRecord({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        comment = self._comment
        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if comment is not UNSET:
            field_dict["comment"] = comment
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

        def get_status() -> Union[Unset, EntryCreateAttachmentsReviewRecordStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = EntryCreateAttachmentsReviewRecordStatus(_status)
                except ValueError:
                    status = EntryCreateAttachmentsReviewRecordStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, EntryCreateAttachmentsReviewRecordStatus], UNSET)

        entry_create_attachments_review_record = cls(
            comment=comment,
            status=status,
        )

        return entry_create_attachments_review_record

    @property
    def comment(self) -> str:
        """ User message to set on review """
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
    def status(self) -> EntryCreateAttachmentsReviewRecordStatus:
        """ Review Status for entry """
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: EntryCreateAttachmentsReviewRecordStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
