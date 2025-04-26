from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.workflow_end_node_details import WorkflowEndNodeDetails
from ..models.workflow_flowchart_node_config_node_type import WorkflowFlowchartNodeConfigNodeType
from ..models.workflow_output_node_details import WorkflowOutputNodeDetails
from ..models.workflow_root_node_details import WorkflowRootNodeDetails
from ..models.workflow_router_node_details import WorkflowRouterNodeDetails
from ..models.workflow_task_node_details import WorkflowTaskNodeDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowFlowchartNodeConfig")


@attr.s(auto_attribs=True, repr=False)
class WorkflowFlowchartNodeConfig:
    """  """

    _id: Union[Unset, str] = UNSET
    _node_details: Union[
        Unset,
        WorkflowRootNodeDetails,
        WorkflowOutputNodeDetails,
        WorkflowTaskNodeDetails,
        WorkflowRouterNodeDetails,
        WorkflowEndNodeDetails,
        UnknownType,
    ] = UNSET
    _node_type: Union[Unset, WorkflowFlowchartNodeConfigNodeType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("node_details={}".format(repr(self._node_details)))
        fields.append("node_type={}".format(repr(self._node_type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowFlowchartNodeConfig({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        node_details: Union[Unset, Dict[str, Any]]
        if isinstance(self._node_details, Unset):
            node_details = UNSET
        elif isinstance(self._node_details, UnknownType):
            node_details = self._node_details.value
        elif isinstance(self._node_details, WorkflowRootNodeDetails):
            node_details = UNSET
            if not isinstance(self._node_details, Unset):
                node_details = self._node_details.to_dict()

        elif isinstance(self._node_details, WorkflowOutputNodeDetails):
            node_details = UNSET
            if not isinstance(self._node_details, Unset):
                node_details = self._node_details.to_dict()

        elif isinstance(self._node_details, WorkflowTaskNodeDetails):
            node_details = UNSET
            if not isinstance(self._node_details, Unset):
                node_details = self._node_details.to_dict()

        elif isinstance(self._node_details, WorkflowRouterNodeDetails):
            node_details = UNSET
            if not isinstance(self._node_details, Unset):
                node_details = self._node_details.to_dict()

        else:
            node_details = UNSET
            if not isinstance(self._node_details, Unset):
                node_details = self._node_details.to_dict()

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self._node_type, Unset):
            node_type = self._node_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if node_details is not UNSET:
            field_dict["nodeDetails"] = node_details
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

        def get_node_details() -> Union[
            Unset,
            WorkflowRootNodeDetails,
            WorkflowOutputNodeDetails,
            WorkflowTaskNodeDetails,
            WorkflowRouterNodeDetails,
            WorkflowEndNodeDetails,
            UnknownType,
        ]:
            node_details: Union[
                Unset,
                WorkflowRootNodeDetails,
                WorkflowOutputNodeDetails,
                WorkflowTaskNodeDetails,
                WorkflowRouterNodeDetails,
                WorkflowEndNodeDetails,
                UnknownType,
            ]
            _node_details = d.pop("nodeDetails")

            if not isinstance(_node_details, Unset):
                discriminator = _node_details["nodeType"]
                if discriminator == "END":
                    node_details = WorkflowEndNodeDetails.from_dict(_node_details)
                elif discriminator == "OUTPUT":
                    node_details = WorkflowOutputNodeDetails.from_dict(_node_details)
                elif discriminator == "ROOT":
                    node_details = WorkflowRootNodeDetails.from_dict(_node_details)
                elif discriminator == "ROUTER":
                    node_details = WorkflowRouterNodeDetails.from_dict(_node_details)
                elif discriminator == "TASK":
                    node_details = WorkflowTaskNodeDetails.from_dict(_node_details)
                else:
                    node_details = UnknownType(value=_node_details)

            return node_details

        try:
            node_details = get_node_details()
        except KeyError:
            if strict:
                raise
            node_details = cast(
                Union[
                    Unset,
                    WorkflowRootNodeDetails,
                    WorkflowOutputNodeDetails,
                    WorkflowTaskNodeDetails,
                    WorkflowRouterNodeDetails,
                    WorkflowEndNodeDetails,
                    UnknownType,
                ],
                UNSET,
            )

        def get_node_type() -> Union[Unset, WorkflowFlowchartNodeConfigNodeType]:
            node_type = UNSET
            _node_type = d.pop("nodeType")
            if _node_type is not None and _node_type is not UNSET:
                try:
                    node_type = WorkflowFlowchartNodeConfigNodeType(_node_type)
                except ValueError:
                    node_type = WorkflowFlowchartNodeConfigNodeType.of_unknown(_node_type)

            return node_type

        try:
            node_type = get_node_type()
        except KeyError:
            if strict:
                raise
            node_type = cast(Union[Unset, WorkflowFlowchartNodeConfigNodeType], UNSET)

        workflow_flowchart_node_config = cls(
            id=id,
            node_details=node_details,
            node_type=node_type,
        )

        workflow_flowchart_node_config.additional_properties = d
        return workflow_flowchart_node_config

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
    def id(self) -> str:
        """ The ID of the workflow flowchart node config """
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
    def node_details(
        self,
    ) -> Union[
        WorkflowRootNodeDetails,
        WorkflowOutputNodeDetails,
        WorkflowTaskNodeDetails,
        WorkflowRouterNodeDetails,
        WorkflowEndNodeDetails,
        UnknownType,
    ]:
        if isinstance(self._node_details, Unset):
            raise NotPresentError(self, "node_details")
        return self._node_details

    @node_details.setter
    def node_details(
        self,
        value: Union[
            WorkflowRootNodeDetails,
            WorkflowOutputNodeDetails,
            WorkflowTaskNodeDetails,
            WorkflowRouterNodeDetails,
            WorkflowEndNodeDetails,
            UnknownType,
        ],
    ) -> None:
        self._node_details = value

    @node_details.deleter
    def node_details(self) -> None:
        self._node_details = UNSET

    @property
    def node_type(self) -> WorkflowFlowchartNodeConfigNodeType:
        """ The type associated with the node config """
        if isinstance(self._node_type, Unset):
            raise NotPresentError(self, "node_type")
        return self._node_type

    @node_type.setter
    def node_type(self, value: WorkflowFlowchartNodeConfigNodeType) -> None:
        self._node_type = value

    @node_type.deleter
    def node_type(self) -> None:
        self._node_type = UNSET
