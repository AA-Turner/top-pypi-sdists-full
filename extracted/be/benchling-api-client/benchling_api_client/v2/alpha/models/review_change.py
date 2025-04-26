import datetime
from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.review_change_action import ReviewChangeAction
from ..models.review_snapshot import ReviewSnapshot
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewChange")


@attr.s(auto_attribs=True, repr=False)
class ReviewChange:
    """  """

    _action: Union[Unset, ReviewChangeAction] = UNSET
    _comment: Union[Unset, None, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _esigned: Union[Unset, bool] = UNSET
    _id: Union[Unset, str] = UNSET
    _review_snapshot: Union[Unset, None, ReviewSnapshot] = UNSET

    def __repr__(self):
        fields = []
        fields.append("action={}".format(repr(self._action)))
        fields.append("comment={}".format(repr(self._comment)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("esigned={}".format(repr(self._esigned)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("review_snapshot={}".format(repr(self._review_snapshot)))
        return "ReviewChange({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        action: Union[Unset, int] = UNSET
        if not isinstance(self._action, Unset):
            action = self._action.value

        comment = self._comment
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        esigned = self._esigned
        id = self._id
        review_snapshot: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._review_snapshot, Unset):
            review_snapshot = self._review_snapshot.to_dict() if self._review_snapshot else None

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if action is not UNSET:
            field_dict["action"] = action
        if comment is not UNSET:
            field_dict["comment"] = comment
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if esigned is not UNSET:
            field_dict["esigned"] = esigned
        if id is not UNSET:
            field_dict["id"] = id
        if review_snapshot is not UNSET:
            field_dict["reviewSnapshot"] = review_snapshot

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_action() -> Union[Unset, ReviewChangeAction]:
            action = UNSET
            _action = d.pop("action")
            if _action is not None and _action is not UNSET:
                try:
                    action = ReviewChangeAction(_action)
                except ValueError:
                    action = ReviewChangeAction.of_unknown(_action)

            return action

        try:
            action = get_action()
        except KeyError:
            if strict:
                raise
            action = cast(Union[Unset, ReviewChangeAction], UNSET)

        def get_comment() -> Union[Unset, None, str]:
            comment = d.pop("comment")
            return comment

        try:
            comment = get_comment()
        except KeyError:
            if strict:
                raise
            comment = cast(Union[Unset, None, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_esigned() -> Union[Unset, bool]:
            esigned = d.pop("esigned")
            return esigned

        try:
            esigned = get_esigned()
        except KeyError:
            if strict:
                raise
            esigned = cast(Union[Unset, bool], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_review_snapshot() -> Union[Unset, None, ReviewSnapshot]:
            review_snapshot = None
            _review_snapshot = d.pop("reviewSnapshot")

            if _review_snapshot is not None and not isinstance(_review_snapshot, Unset):
                review_snapshot = ReviewSnapshot.from_dict(_review_snapshot)

            return review_snapshot

        try:
            review_snapshot = get_review_snapshot()
        except KeyError:
            if strict:
                raise
            review_snapshot = cast(Union[Unset, None, ReviewSnapshot], UNSET)

        review_change = cls(
            action=action,
            comment=comment,
            created_at=created_at,
            esigned=esigned,
            id=id,
            review_snapshot=review_snapshot,
        )

        return review_change

    @property
    def action(self) -> ReviewChangeAction:
        """ The action which was performed with this change """
        if isinstance(self._action, Unset):
            raise NotPresentError(self, "action")
        return self._action

    @action.setter
    def action(self, value: ReviewChangeAction) -> None:
        self._action = value

    @action.deleter
    def action(self) -> None:
        self._action = UNSET

    @property
    def comment(self) -> Optional[str]:
        """ The comment which was left when the Review Change was submitted """
        if isinstance(self._comment, Unset):
            raise NotPresentError(self, "comment")
        return self._comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        self._comment = value

    @comment.deleter
    def comment(self) -> None:
        self._comment = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ DateTime the Review Change was created at """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def esigned(self) -> bool:
        """ Was the action verified through an e-signature compliant step """
        if isinstance(self._esigned, Unset):
            raise NotPresentError(self, "esigned")
        return self._esigned

    @esigned.setter
    def esigned(self, value: bool) -> None:
        self._esigned = value

    @esigned.deleter
    def esigned(self) -> None:
        self._esigned = UNSET

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
    def review_snapshot(self) -> Optional[ReviewSnapshot]:
        if isinstance(self._review_snapshot, Unset):
            raise NotPresentError(self, "review_snapshot")
        return self._review_snapshot

    @review_snapshot.setter
    def review_snapshot(self, value: Optional[ReviewSnapshot]) -> None:
        self._review_snapshot = value

    @review_snapshot.deleter
    def review_snapshot(self) -> None:
        self._review_snapshot = UNSET
