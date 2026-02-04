from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_review_process_completion_status import EntryReviewProcessCompletionStatus
from ..models.entry_review_process_stages_item import EntryReviewProcessStagesItem
from ..models.entry_review_process_type import EntryReviewProcessType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryReviewProcess")


@attr.s(auto_attribs=True, repr=False)
class EntryReviewProcess:
    """  """

    _completion_status: Union[Unset, EntryReviewProcessCompletionStatus] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _stages: Union[Unset, List[EntryReviewProcessStagesItem]] = UNSET
    _type: Union[Unset, EntryReviewProcessType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("completion_status={}".format(repr(self._completion_status)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("stages={}".format(repr(self._stages)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "EntryReviewProcess({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        completion_status: Union[Unset, int] = UNSET
        if not isinstance(self._completion_status, Unset):
            completion_status = self._completion_status.value

        id = self._id
        name = self._name
        stages: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._stages, Unset):
            stages = []
            for stages_item_data in self._stages:
                stages_item = stages_item_data.to_dict()

                stages.append(stages_item)

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if completion_status is not UNSET:
            field_dict["completionStatus"] = completion_status
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if stages is not UNSET:
            field_dict["stages"] = stages
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_completion_status() -> Union[Unset, EntryReviewProcessCompletionStatus]:
            completion_status = UNSET
            _completion_status = d.pop("completionStatus")
            if _completion_status is not None and _completion_status is not UNSET:
                try:
                    completion_status = EntryReviewProcessCompletionStatus(_completion_status)
                except ValueError:
                    completion_status = EntryReviewProcessCompletionStatus.of_unknown(_completion_status)

            return completion_status

        try:
            completion_status = get_completion_status()
        except KeyError:
            if strict:
                raise
            completion_status = cast(Union[Unset, EntryReviewProcessCompletionStatus], UNSET)

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

        def get_stages() -> Union[Unset, List[EntryReviewProcessStagesItem]]:
            stages = []
            _stages = d.pop("stages")
            for stages_item_data in _stages or []:
                stages_item = EntryReviewProcessStagesItem.from_dict(stages_item_data, strict=False)

                stages.append(stages_item)

            return stages

        try:
            stages = get_stages()
        except KeyError:
            if strict:
                raise
            stages = cast(Union[Unset, List[EntryReviewProcessStagesItem]], UNSET)

        def get_type() -> Union[Unset, EntryReviewProcessType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = EntryReviewProcessType(_type)
                except ValueError:
                    type = EntryReviewProcessType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, EntryReviewProcessType], UNSET)

        entry_review_process = cls(
            completion_status=completion_status,
            id=id,
            name=name,
            stages=stages,
            type=type,
        )

        entry_review_process.additional_properties = d
        return entry_review_process

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
    def completion_status(self) -> EntryReviewProcessCompletionStatus:
        """ State of the Entry at the end of the Review Process """
        if isinstance(self._completion_status, Unset):
            raise NotPresentError(self, "completion_status")
        return self._completion_status

    @completion_status.setter
    def completion_status(self, value: EntryReviewProcessCompletionStatus) -> None:
        self._completion_status = value

    @completion_status.deleter
    def completion_status(self) -> None:
        self._completion_status = UNSET

    @property
    def id(self) -> str:
        """ ID of the Review Process """
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
        """ Name of the Review Process """
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
    def stages(self) -> List[EntryReviewProcessStagesItem]:
        """ Array of Stages for the Review Process """
        if isinstance(self._stages, Unset):
            raise NotPresentError(self, "stages")
        return self._stages

    @stages.setter
    def stages(self, value: List[EntryReviewProcessStagesItem]) -> None:
        self._stages = value

    @stages.deleter
    def stages(self) -> None:
        self._stages = UNSET

    @property
    def type(self) -> EntryReviewProcessType:
        """ Type of the Review Process """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: EntryReviewProcessType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
