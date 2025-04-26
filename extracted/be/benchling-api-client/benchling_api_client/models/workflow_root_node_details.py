from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_root_node_details_node_type import WorkflowRootNodeDetailsNodeType
from ..models.workflow_task_schema_summary import WorkflowTaskSchemaSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRootNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowRootNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _node_type: Union[Unset, WorkflowRootNodeDetailsNodeType] = UNSET
    _root_task_schema: Union[Unset, WorkflowTaskSchemaSummary] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("node_type={}".format(repr(self._node_type)))
        fields.append("root_task_schema={}".format(repr(self._root_task_schema)))
        return "WorkflowRootNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        node_type: Union[Unset, int] = UNSET
        if not isinstance(self._node_type, Unset):
            node_type = self._node_type.value

        root_task_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._root_task_schema, Unset):
            root_task_schema = self._root_task_schema.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if node_type is not UNSET:
            field_dict["nodeType"] = node_type
        if root_task_schema is not UNSET:
            field_dict["rootTaskSchema"] = root_task_schema

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

        def get_node_type() -> Union[Unset, WorkflowRootNodeDetailsNodeType]:
            node_type = UNSET
            _node_type = d.pop("nodeType")
            if _node_type is not None and _node_type is not UNSET:
                try:
                    node_type = WorkflowRootNodeDetailsNodeType(_node_type)
                except ValueError:
                    node_type = WorkflowRootNodeDetailsNodeType.of_unknown(_node_type)

            return node_type

        try:
            node_type = get_node_type()
        except KeyError:
            if strict:
                raise
            node_type = cast(Union[Unset, WorkflowRootNodeDetailsNodeType], UNSET)

        def get_root_task_schema() -> Union[Unset, WorkflowTaskSchemaSummary]:
            root_task_schema: Union[Unset, Union[Unset, WorkflowTaskSchemaSummary]] = UNSET
            _root_task_schema = d.pop("rootTaskSchema")

            if not isinstance(_root_task_schema, Unset):
                root_task_schema = WorkflowTaskSchemaSummary.from_dict(_root_task_schema)

            return root_task_schema

        try:
            root_task_schema = get_root_task_schema()
        except KeyError:
            if strict:
                raise
            root_task_schema = cast(Union[Unset, WorkflowTaskSchemaSummary], UNSET)

        workflow_root_node_details = cls(
            id=id,
            node_type=node_type,
            root_task_schema=root_task_schema,
        )

        return workflow_root_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow root node config details """
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
    def node_type(self) -> WorkflowRootNodeDetailsNodeType:
        """ The type of the node """
        if isinstance(self._node_type, Unset):
            raise NotPresentError(self, "node_type")
        return self._node_type

    @node_type.setter
    def node_type(self, value: WorkflowRootNodeDetailsNodeType) -> None:
        self._node_type = value

    @node_type.deleter
    def node_type(self) -> None:
        self._node_type = UNSET

    @property
    def root_task_schema(self) -> WorkflowTaskSchemaSummary:
        if isinstance(self._root_task_schema, Unset):
            raise NotPresentError(self, "root_task_schema")
        return self._root_task_schema

    @root_task_schema.setter
    def root_task_schema(self, value: WorkflowTaskSchemaSummary) -> None:
        self._root_task_schema = value

    @root_task_schema.deleter
    def root_task_schema(self) -> None:
        self._root_task_schema = UNSET
