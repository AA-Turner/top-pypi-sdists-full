from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryAttachments")


@attr.s(auto_attribs=True, repr=False)
class EntryAttachments:
    """  """

    _attachment_text: Union[Unset, None] = UNSET
    _attachments: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("attachment_text={}".format(repr(self._attachment_text)))
        fields.append("attachments={}".format(repr(self._attachments)))
        return "EntryAttachments({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        attachment_text = None

        attachments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._attachments, Unset):
            attachments = self._attachments

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if attachment_text is not UNSET:
            field_dict["attachmentText"] = attachment_text
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_attachment_text() -> Union[Unset, None]:
            attachment_text = None

            return attachment_text

        try:
            attachment_text = get_attachment_text()
        except KeyError:
            if strict:
                raise
            attachment_text = cast(Union[Unset, None], UNSET)

        def get_attachments() -> Union[Unset, List[str]]:
            attachments = cast(List[str], d.pop("attachments"))

            return attachments

        try:
            attachments = get_attachments()
        except KeyError:
            if strict:
                raise
            attachments = cast(Union[Unset, List[str]], UNSET)

        entry_attachments = cls(
            attachment_text=attachment_text,
            attachments=attachments,
        )

        return entry_attachments

    @property
    def attachment_text(self) -> None:
        """Text to include in the entry before the attachments. If not provided, the text will be "File attachments are listed below:" """
        if isinstance(self._attachment_text, Unset):
            raise NotPresentError(self, "attachment_text")
        return self._attachment_text

    @attachment_text.setter
    def attachment_text(self, value: None) -> None:
        self._attachment_text = value

    @attachment_text.deleter
    def attachment_text(self) -> None:
        self._attachment_text = UNSET

    @property
    def attachments(self) -> List[str]:
        """An array of IDs representing Blob objects in Benchling to be attached to the entry."""
        if isinstance(self._attachments, Unset):
            raise NotPresentError(self, "attachments")
        return self._attachments

    @attachments.setter
    def attachments(self, value: List[str]) -> None:
        self._attachments = value

    @attachments.deleter
    def attachments(self) -> None:
        self._attachments = UNSET
