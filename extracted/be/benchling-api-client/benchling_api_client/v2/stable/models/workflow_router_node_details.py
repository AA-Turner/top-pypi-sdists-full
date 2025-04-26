from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_router_function import WorkflowRouterFunction
from ..models.workflow_router_node_details_node_type import WorkflowRouterNodeDetailsNodeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowRouterNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowRouterNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _node_type: Union[Unset, WorkflowRouterNodeDetailsNodeType] = UNSET
    _router_functions: Union[Unset, List[WorkflowRouterFunction]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("node_type={}".format(repr(self._node_type)))
        fields.append("router_functions={}".format(repr(self._router_functions)))
        return "WorkflowRouterNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        node_type: Union[Unset, int] = UNSET
        if not isinstance(self._node_type, Unset):
            node_type = self._node_type.value

        router_functions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._router_functions, Unset):
            router_functions = []
            for router_functions_item_data in self._router_functions:
                router_functions_item = router_functions_item_data.to_dict()

                router_functions.append(router_functions_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if node_type is not UNSET:
            field_dict["nodeType"] = node_type
        if router_functions is not UNSET:
            field_dict["routerFunctions"] = router_functions

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

        def get_node_type() -> Union[Unset, WorkflowRouterNodeDetailsNodeType]:
            node_type = UNSET
            _node_type = d.pop("nodeType")
            if _node_type is not None and _node_type is not UNSET:
                try:
                    node_type = WorkflowRouterNodeDetailsNodeType(_node_type)
                except ValueError:
                    node_type = WorkflowRouterNodeDetailsNodeType.of_unknown(_node_type)

            return node_type

        try:
            node_type = get_node_type()
        except KeyError:
            if strict:
                raise
            node_type = cast(Union[Unset, WorkflowRouterNodeDetailsNodeType], UNSET)

        def get_router_functions() -> Union[Unset, List[WorkflowRouterFunction]]:
            router_functions = []
            _router_functions = d.pop("routerFunctions")
            for router_functions_item_data in _router_functions or []:
                router_functions_item = WorkflowRouterFunction.from_dict(
                    router_functions_item_data, strict=False
                )

                router_functions.append(router_functions_item)

            return router_functions

        try:
            router_functions = get_router_functions()
        except KeyError:
            if strict:
                raise
            router_functions = cast(Union[Unset, List[WorkflowRouterFunction]], UNSET)

        workflow_router_node_details = cls(
            id=id,
            name=name,
            node_type=node_type,
            router_functions=router_functions,
        )

        return workflow_router_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow router node config details """
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
        """ The name of the router node """
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
    def node_type(self) -> WorkflowRouterNodeDetailsNodeType:
        """ The type of the node """
        if isinstance(self._node_type, Unset):
            raise NotPresentError(self, "node_type")
        return self._node_type

    @node_type.setter
    def node_type(self, value: WorkflowRouterNodeDetailsNodeType) -> None:
        self._node_type = value

    @node_type.deleter
    def node_type(self) -> None:
        self._node_type = UNSET

    @property
    def router_functions(self) -> List[WorkflowRouterFunction]:
        """ Router functions associated with this router node """
        if isinstance(self._router_functions, Unset):
            raise NotPresentError(self, "router_functions")
        return self._router_functions

    @router_functions.setter
    def router_functions(self, value: List[WorkflowRouterFunction]) -> None:
        self._router_functions = value

    @router_functions.deleter
    def router_functions(self) -> None:
        self._router_functions = UNSET
