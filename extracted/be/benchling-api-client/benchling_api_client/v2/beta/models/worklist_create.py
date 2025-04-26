from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.member_collaborator import MemberCollaborator
from ..models.principal_collaborator import PrincipalCollaborator
from ..models.worklist_type import WorklistType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorklistCreate")


@attr.s(auto_attribs=True, repr=False)
class WorklistCreate:
    """  """

    _name: str
    _type: WorklistType
    _collaborations: Union[Unset, List[Union[PrincipalCollaborator, MemberCollaborator, UnknownType]]] = UNSET
    _worklist_item_ids: Union[Unset, List[str]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("name={}".format(repr(self._name)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("collaborations={}".format(repr(self._collaborations)))
        fields.append("worklist_item_ids={}".format(repr(self._worklist_item_ids)))
        return "WorklistCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        name = self._name
        type = self._type.value

        collaborations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._collaborations, Unset):
            collaborations = []
            for collaborations_item_data in self._collaborations:
                if isinstance(collaborations_item_data, UnknownType):
                    collaborations_item = collaborations_item_data.value
                elif isinstance(collaborations_item_data, PrincipalCollaborator):
                    collaborations_item = collaborations_item_data.to_dict()

                else:
                    collaborations_item = collaborations_item_data.to_dict()

                collaborations.append(collaborations_item)

        worklist_item_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._worklist_item_ids, Unset):
            worklist_item_ids = self._worklist_item_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if collaborations is not UNSET:
            field_dict["collaborations"] = collaborations
        if worklist_item_ids is not UNSET:
            field_dict["worklistItemIds"] = worklist_item_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_type() -> WorklistType:
            _type = d.pop("type")
            try:
                type = WorklistType(_type)
            except ValueError:
                type = WorklistType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(WorklistType, UNSET)

        def get_collaborations() -> Union[
            Unset, List[Union[PrincipalCollaborator, MemberCollaborator, UnknownType]]
        ]:
            collaborations = []
            _collaborations = d.pop("collaborations")
            for collaborations_item_data in _collaborations or []:

                def _parse_collaborations_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[PrincipalCollaborator, MemberCollaborator, UnknownType]:
                    collaborations_item: Union[PrincipalCollaborator, MemberCollaborator, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        collaboration_create = PrincipalCollaborator.from_dict(data, strict=True)

                        return collaboration_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        collaboration_create = MemberCollaborator.from_dict(data, strict=True)

                        return collaboration_create
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                collaborations_item = _parse_collaborations_item(collaborations_item_data)

                collaborations.append(collaborations_item)

            return collaborations

        try:
            collaborations = get_collaborations()
        except KeyError:
            if strict:
                raise
            collaborations = cast(
                Union[Unset, List[Union[PrincipalCollaborator, MemberCollaborator, UnknownType]]], UNSET
            )

        def get_worklist_item_ids() -> Union[Unset, List[str]]:
            worklist_item_ids = cast(List[str], d.pop("worklistItemIds"))

            return worklist_item_ids

        try:
            worklist_item_ids = get_worklist_item_ids()
        except KeyError:
            if strict:
                raise
            worklist_item_ids = cast(Union[Unset, List[str]], UNSET)

        worklist_create = cls(
            name=name,
            type=type,
            collaborations=collaborations,
            worklist_item_ids=worklist_item_ids,
        )

        return worklist_create

    @property
    def name(self) -> str:
        """ Name of the worklist """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def type(self) -> WorklistType:
        """The type of items a worklist contains."""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: WorklistType) -> None:
        self._type = value

    @property
    def collaborations(self) -> List[Union[PrincipalCollaborator, MemberCollaborator, UnknownType]]:
        if isinstance(self._collaborations, Unset):
            raise NotPresentError(self, "collaborations")
        return self._collaborations

    @collaborations.setter
    def collaborations(
        self, value: List[Union[PrincipalCollaborator, MemberCollaborator, UnknownType]]
    ) -> None:
        self._collaborations = value

    @collaborations.deleter
    def collaborations(self) -> None:
        self._collaborations = UNSET

    @property
    def worklist_item_ids(self) -> List[str]:
        """An ordered set of IDs to assign as worklist items. IDs should reference existing items which fit the worklist's specific type. For instance, a worklist of type container should only have item IDs which represent containers."""
        if isinstance(self._worklist_item_ids, Unset):
            raise NotPresentError(self, "worklist_item_ids")
        return self._worklist_item_ids

    @worklist_item_ids.setter
    def worklist_item_ids(self, value: List[str]) -> None:
        self._worklist_item_ids = value

    @worklist_item_ids.deleter
    def worklist_item_ids(self) -> None:
        self._worklist_item_ids = UNSET
