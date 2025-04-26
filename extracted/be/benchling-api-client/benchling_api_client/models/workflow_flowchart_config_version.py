from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_flowchart import WorkflowFlowchart
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowFlowchartConfigVersion")


@attr.s(auto_attribs=True, repr=False)
class WorkflowFlowchartConfigVersion:
    """  """

    _created_at: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _template_flowchart: Union[Unset, WorkflowFlowchart] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("template_flowchart={}".format(repr(self._template_flowchart)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowFlowchartConfigVersion({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        created_at = self._created_at
        id = self._id
        modified_at = self._modified_at
        template_flowchart: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._template_flowchart, Unset):
            template_flowchart = self._template_flowchart.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if template_flowchart is not UNSET:
            field_dict["templateFlowchart"] = template_flowchart

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

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, str]:
            modified_at = d.pop("modifiedAt")
            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, str], UNSET)

        def get_template_flowchart() -> Union[Unset, WorkflowFlowchart]:
            template_flowchart: Union[Unset, Union[Unset, WorkflowFlowchart]] = UNSET
            _template_flowchart = d.pop("templateFlowchart")

            if not isinstance(_template_flowchart, Unset):
                template_flowchart = WorkflowFlowchart.from_dict(_template_flowchart)

            return template_flowchart

        try:
            template_flowchart = get_template_flowchart()
        except KeyError:
            if strict:
                raise
            template_flowchart = cast(Union[Unset, WorkflowFlowchart], UNSET)

        workflow_flowchart_config_version = cls(
            created_at=created_at,
            id=id,
            modified_at=modified_at,
            template_flowchart=template_flowchart,
        )

        workflow_flowchart_config_version.additional_properties = d
        return workflow_flowchart_config_version

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
        """ The ISO formatted date and time that the flowchart config version was created """
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
    def id(self) -> str:
        """ The ID of the workflow flowchart config version """
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
    def modified_at(self) -> str:
        """ The ISO formatted date and time that the flowchart config version was last modified """
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
    def template_flowchart(self) -> WorkflowFlowchart:
        if isinstance(self._template_flowchart, Unset):
            raise NotPresentError(self, "template_flowchart")
        return self._template_flowchart

    @template_flowchart.setter
    def template_flowchart(self, value: WorkflowFlowchart) -> None:
        self._template_flowchart = value

    @template_flowchart.deleter
    def template_flowchart(self) -> None:
        self._template_flowchart = UNSET
