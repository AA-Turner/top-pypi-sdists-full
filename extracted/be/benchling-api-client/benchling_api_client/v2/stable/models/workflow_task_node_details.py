from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_task_node_details_node_type import WorkflowTaskNodeDetailsNodeType
from ..models.workflow_task_schema_summary import WorkflowTaskSchemaSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTaskNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowTaskNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _node_type: Union[Unset, WorkflowTaskNodeDetailsNodeType] = UNSET
    _task_schema: Union[Unset, WorkflowTaskSchemaSummary] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("node_type={}".format(repr(self._node_type)))
        fields.append("task_schema={}".format(repr(self._task_schema)))
        return "WorkflowTaskNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        node_type: Union[Unset, int] = UNSET
        if not isinstance(self._node_type, Unset):
            node_type = self._node_type.value

        task_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._task_schema, Unset):
            task_schema = self._task_schema.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if node_type is not UNSET:
            field_dict["nodeType"] = node_type
        if task_schema is not UNSET:
            field_dict["taskSchema"] = task_schema

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

        def get_node_type() -> Union[Unset, WorkflowTaskNodeDetailsNodeType]:
            node_type = UNSET
            _node_type = d.pop("nodeType")
            if _node_type is not None and _node_type is not UNSET:
                try:
                    node_type = WorkflowTaskNodeDetailsNodeType(_node_type)
                except ValueError:
                    node_type = WorkflowTaskNodeDetailsNodeType.of_unknown(_node_type)

            return node_type

        try:
            node_type = get_node_type()
        except KeyError:
            if strict:
                raise
            node_type = cast(Union[Unset, WorkflowTaskNodeDetailsNodeType], UNSET)

        def get_task_schema() -> Union[Unset, WorkflowTaskSchemaSummary]:
            task_schema: Union[Unset, Union[Unset, WorkflowTaskSchemaSummary]] = UNSET
            _task_schema = d.pop("taskSchema")

            if not isinstance(_task_schema, Unset):
                task_schema = WorkflowTaskSchemaSummary.from_dict(_task_schema)

            return task_schema

        try:
            task_schema = get_task_schema()
        except KeyError:
            if strict:
                raise
            task_schema = cast(Union[Unset, WorkflowTaskSchemaSummary], UNSET)

        workflow_task_node_details = cls(
            id=id,
            node_type=node_type,
            task_schema=task_schema,
        )

        return workflow_task_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow task node config details """
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
    def node_type(self) -> WorkflowTaskNodeDetailsNodeType:
        """ The type of the node """
        if isinstance(self._node_type, Unset):
            raise NotPresentError(self, "node_type")
        return self._node_type

    @node_type.setter
    def node_type(self, value: WorkflowTaskNodeDetailsNodeType) -> None:
        self._node_type = value

    @node_type.deleter
    def node_type(self) -> None:
        self._node_type = UNSET

    @property
    def task_schema(self) -> WorkflowTaskSchemaSummary:
        if isinstance(self._task_schema, Unset):
            raise NotPresentError(self, "task_schema")
        return self._task_schema

    @task_schema.setter
    def task_schema(self, value: WorkflowTaskSchemaSummary) -> None:
        self._task_schema = value

    @task_schema.deleter
    def task_schema(self) -> None:
        self._task_schema = UNSET
