from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_end_node_details_node_type import WorkflowEndNodeDetailsNodeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowEndNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowEndNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _node_type: Union[Unset, WorkflowEndNodeDetailsNodeType] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("node_type={}".format(repr(self._node_type)))
        return "WorkflowEndNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        node_type: Union[Unset, int] = UNSET
        if not isinstance(self._node_type, Unset):
            node_type = self._node_type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if node_type is not UNSET:
            field_dict["nodeType"] = node_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

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

        def get_node_type() -> Union[Unset, WorkflowEndNodeDetailsNodeType]:
            node_type = UNSET
            _node_type = d.pop("nodeType")
            if _node_type is not None and _node_type is not UNSET:
                try:
                    node_type = WorkflowEndNodeDetailsNodeType(_node_type)
                except ValueError:
                    node_type = WorkflowEndNodeDetailsNodeType.of_unknown(_node_type)

            return node_type

        try:
            node_type = get_node_type()
        except KeyError:
            if strict:
                raise
            node_type = cast(Union[Unset, WorkflowEndNodeDetailsNodeType], UNSET)

        workflow_end_node_details = cls(
            id=id,
            name=name,
            node_type=node_type,
        )

        return workflow_end_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow flowchart end node config details """
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
        """ The name of the end node """
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
    def node_type(self) -> WorkflowEndNodeDetailsNodeType:
        """ The type of the node """
        if isinstance(self._node_type, Unset):
            raise NotPresentError(self, "node_type")
        return self._node_type

    @node_type.setter
    def node_type(self, value: WorkflowEndNodeDetailsNodeType) -> None:
        self._node_type = value

    @node_type.deleter
    def node_type(self) -> None:
        self._node_type = UNSET
