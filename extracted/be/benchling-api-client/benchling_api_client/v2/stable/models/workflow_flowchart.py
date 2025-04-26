from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_flowchart_edge_config import WorkflowFlowchartEdgeConfig
from ..models.workflow_flowchart_node_config import WorkflowFlowchartNodeConfig
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowFlowchart")


@attr.s(auto_attribs=True, repr=False)
class WorkflowFlowchart:
    """  """

    _created_at: Union[Unset, str] = UNSET
    _edge_configs: Union[Unset, List[WorkflowFlowchartEdgeConfig]] = UNSET
    _id: Union[Unset, str] = UNSET
    _migrated_from_flowchart_id: Union[Unset, None, str] = UNSET
    _migrated_to_flowchart_id: Union[Unset, None, str] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _node_configs: Union[Unset, List[WorkflowFlowchartNodeConfig]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("edge_configs={}".format(repr(self._edge_configs)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("migrated_from_flowchart_id={}".format(repr(self._migrated_from_flowchart_id)))
        fields.append("migrated_to_flowchart_id={}".format(repr(self._migrated_to_flowchart_id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("node_configs={}".format(repr(self._node_configs)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowFlowchart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at
        edge_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._edge_configs, Unset):
            edge_configs = []
            for edge_configs_item_data in self._edge_configs:
                edge_configs_item = edge_configs_item_data.to_dict()

                edge_configs.append(edge_configs_item)

        id = self._id
        migrated_from_flowchart_id = self._migrated_from_flowchart_id
        migrated_to_flowchart_id = self._migrated_to_flowchart_id
        modified_at = self._modified_at
        node_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._node_configs, Unset):
            node_configs = []
            for node_configs_item_data in self._node_configs:
                node_configs_item = node_configs_item_data.to_dict()

                node_configs.append(node_configs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if edge_configs is not UNSET:
            field_dict["edgeConfigs"] = edge_configs
        if id is not UNSET:
            field_dict["id"] = id
        if migrated_from_flowchart_id is not UNSET:
            field_dict["migratedFromFlowchartId"] = migrated_from_flowchart_id
        if migrated_to_flowchart_id is not UNSET:
            field_dict["migratedToFlowchartId"] = migrated_to_flowchart_id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if node_configs is not UNSET:
            field_dict["nodeConfigs"] = node_configs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_created_at() -> Union[Unset, str]:
            created_at = d.pop("createdAt")
            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, str], UNSET)

        def get_edge_configs() -> Union[Unset, List[WorkflowFlowchartEdgeConfig]]:
            edge_configs = []
            _edge_configs = d.pop("edgeConfigs")
            for edge_configs_item_data in _edge_configs or []:
                edge_configs_item = WorkflowFlowchartEdgeConfig.from_dict(
                    edge_configs_item_data, strict=False
                )

                edge_configs.append(edge_configs_item)

            return edge_configs

        try:
            edge_configs = get_edge_configs()
        except KeyError:
            if strict:
                raise
            edge_configs = cast(Union[Unset, List[WorkflowFlowchartEdgeConfig]], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_migrated_from_flowchart_id() -> Union[Unset, None, str]:
            migrated_from_flowchart_id = d.pop("migratedFromFlowchartId")
            return migrated_from_flowchart_id

        try:
            migrated_from_flowchart_id = get_migrated_from_flowchart_id()
        except KeyError:
            if strict:
                raise
            migrated_from_flowchart_id = cast(Union[Unset, None, str], UNSET)

        def get_migrated_to_flowchart_id() -> Union[Unset, None, str]:
            migrated_to_flowchart_id = d.pop("migratedToFlowchartId")
            return migrated_to_flowchart_id

        try:
            migrated_to_flowchart_id = get_migrated_to_flowchart_id()
        except KeyError:
            if strict:
                raise
            migrated_to_flowchart_id = cast(Union[Unset, None, str], UNSET)

        def get_modified_at() -> Union[Unset, str]:
            modified_at = d.pop("modifiedAt")
            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, str], UNSET)

        def get_node_configs() -> Union[Unset, List[WorkflowFlowchartNodeConfig]]:
            node_configs = []
            _node_configs = d.pop("nodeConfigs")
            for node_configs_item_data in _node_configs or []:
                node_configs_item = WorkflowFlowchartNodeConfig.from_dict(
                    node_configs_item_data, strict=False
                )

                node_configs.append(node_configs_item)

            return node_configs

        try:
            node_configs = get_node_configs()
        except KeyError:
            if strict:
                raise
            node_configs = cast(Union[Unset, List[WorkflowFlowchartNodeConfig]], UNSET)

        workflow_flowchart = cls(
            created_at=created_at,
            edge_configs=edge_configs,
            id=id,
            migrated_from_flowchart_id=migrated_from_flowchart_id,
            migrated_to_flowchart_id=migrated_to_flowchart_id,
            modified_at=modified_at,
            node_configs=node_configs,
        )

        workflow_flowchart.additional_properties = d
        return workflow_flowchart

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
    def created_at(self) -> str:
        """ The ISO formatted date and time that the flowchart was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: str) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def edge_configs(self) -> List[WorkflowFlowchartEdgeConfig]:
        """ The edges of the flowchart """
        if isinstance(self._edge_configs, Unset):
            raise NotPresentError(self, "edge_configs")
        return self._edge_configs

    @edge_configs.setter
    def edge_configs(self, value: List[WorkflowFlowchartEdgeConfig]) -> None:
        self._edge_configs = value

    @edge_configs.deleter
    def edge_configs(self) -> None:
        self._edge_configs = UNSET

    @property
    def id(self) -> str:
        """ The ID of the flowchart """
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
    def migrated_from_flowchart_id(self) -> Optional[str]:
        """ The ID of the flowchart that this was migrated from """
        if isinstance(self._migrated_from_flowchart_id, Unset):
            raise NotPresentError(self, "migrated_from_flowchart_id")
        return self._migrated_from_flowchart_id

    @migrated_from_flowchart_id.setter
    def migrated_from_flowchart_id(self, value: Optional[str]) -> None:
        self._migrated_from_flowchart_id = value

    @migrated_from_flowchart_id.deleter
    def migrated_from_flowchart_id(self) -> None:
        self._migrated_from_flowchart_id = UNSET

    @property
    def migrated_to_flowchart_id(self) -> Optional[str]:
        """ The ID of the flowchart that this was migrated to """
        if isinstance(self._migrated_to_flowchart_id, Unset):
            raise NotPresentError(self, "migrated_to_flowchart_id")
        return self._migrated_to_flowchart_id

    @migrated_to_flowchart_id.setter
    def migrated_to_flowchart_id(self, value: Optional[str]) -> None:
        self._migrated_to_flowchart_id = value

    @migrated_to_flowchart_id.deleter
    def migrated_to_flowchart_id(self) -> None:
        self._migrated_to_flowchart_id = UNSET

    @property
    def modified_at(self) -> str:
        """ The ISO formatted date and time that the flowchart was last modified """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: str) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def node_configs(self) -> List[WorkflowFlowchartNodeConfig]:
        """ The nodes of the flowchart """
        if isinstance(self._node_configs, Unset):
            raise NotPresentError(self, "node_configs")
        return self._node_configs

    @node_configs.setter
    def node_configs(self, value: List[WorkflowFlowchartNodeConfig]) -> None:
        self._node_configs = value

    @node_configs.deleter
    def node_configs(self) -> None:
        self._node_configs = UNSET
