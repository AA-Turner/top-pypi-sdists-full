from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_review_process_stages_item_action_label import EntryReviewProcessStagesItemActionLabel
from ..models.entry_review_process_stages_item_reviewers_item import EntryReviewProcessStagesItemReviewersItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryReviewProcessStagesItem")


@attr.s(auto_attribs=True, repr=False)
class EntryReviewProcessStagesItem:
    """  """

    _action_label: Union[Unset, EntryReviewProcessStagesItemActionLabel] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _reviewers: Union[Unset, List[EntryReviewProcessStagesItemReviewersItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("action_label={}".format(repr(self._action_label)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("reviewers={}".format(repr(self._reviewers)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryReviewProcessStagesItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        action_label: Union[Unset, int] = UNSET
        if not isinstance(self._action_label, Unset):
            action_label = self._action_label.value

        id = self._id
        name = self._name
        reviewers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._reviewers, Unset):
            reviewers = []
            for reviewers_item_data in self._reviewers:
                reviewers_item = reviewers_item_data.to_dict()

                reviewers.append(reviewers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if action_label is not UNSET:
            field_dict["actionLabel"] = action_label
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if reviewers is not UNSET:
            field_dict["reviewers"] = reviewers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_action_label() -> Union[Unset, EntryReviewProcessStagesItemActionLabel]:
            action_label = UNSET
            _action_label = d.pop("actionLabel")
            if _action_label is not None and _action_label is not UNSET:
                try:
                    action_label = EntryReviewProcessStagesItemActionLabel(_action_label)
                except ValueError:
                    action_label = EntryReviewProcessStagesItemActionLabel.of_unknown(_action_label)

            return action_label

        try:
            action_label = get_action_label()
        except KeyError:
            if strict:
                raise
            action_label = cast(Union[Unset, EntryReviewProcessStagesItemActionLabel], UNSET)

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

        def get_reviewers() -> Union[Unset, List[EntryReviewProcessStagesItemReviewersItem]]:
            reviewers = []
            _reviewers = d.pop("reviewers")
            for reviewers_item_data in _reviewers or []:
                reviewers_item = EntryReviewProcessStagesItemReviewersItem.from_dict(
                    reviewers_item_data, strict=False
                )

                reviewers.append(reviewers_item)

            return reviewers

        try:
            reviewers = get_reviewers()
        except KeyError:
            if strict:
                raise
            reviewers = cast(Union[Unset, List[EntryReviewProcessStagesItemReviewersItem]], UNSET)

        entry_review_process_stages_item = cls(
            action_label=action_label,
            id=id,
            name=name,
            reviewers=reviewers,
        )

        entry_review_process_stages_item.additional_properties = d
        return entry_review_process_stages_item

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
    def action_label(self) -> EntryReviewProcessStagesItemActionLabel:
        """ Action reviewer is doing during the review """
        if isinstance(self._action_label, Unset):
            raise NotPresentError(self, "action_label")
        return self._action_label

    @action_label.setter
    def action_label(self, value: EntryReviewProcessStagesItemActionLabel) -> None:
        self._action_label = value

    @action_label.deleter
    def action_label(self) -> None:
        self._action_label = UNSET

    @property
    def id(self) -> str:
        """ ID of the Review Stage """
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
        """ Name of the Review Stage """
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
    def reviewers(self) -> List[EntryReviewProcessStagesItemReviewersItem]:
        """ Reviewers for the Review Stage """
        if isinstance(self._reviewers, Unset):
            raise NotPresentError(self, "reviewers")
        return self._reviewers

    @reviewers.setter
    def reviewers(self, value: List[EntryReviewProcessStagesItemReviewersItem]) -> None:
        self._reviewers = value

    @reviewers.deleter
    def reviewers(self) -> None:
        self._reviewers = UNSET
