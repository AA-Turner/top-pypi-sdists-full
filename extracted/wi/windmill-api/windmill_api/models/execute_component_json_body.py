from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execute_component_json_body_force_viewer_one_of_fields import (
        ExecuteComponentJsonBodyForceViewerOneOfFields,
    )
    from ..models.execute_component_json_body_force_viewer_static_fields import (
        ExecuteComponentJsonBodyForceViewerStaticFields,
    )
    from ..models.execute_component_json_body_raw_code import ExecuteComponentJsonBodyRawCode


T = TypeVar("T", bound="ExecuteComponentJsonBody")


@_attrs_define
class ExecuteComponentJsonBody:
    """
    Attributes:
        component (str):
        args (Any):
        path (Union[Unset, str]):
        version (Union[Unset, int]):
        raw_code (Union[Unset, ExecuteComponentJsonBodyRawCode]):
        id (Union[Unset, int]):
        force_viewer_static_fields (Union[Unset, ExecuteComponentJsonBodyForceViewerStaticFields]):
        force_viewer_one_of_fields (Union[Unset, ExecuteComponentJsonBodyForceViewerOneOfFields]):
        force_viewer_allow_user_resources (Union[Unset, List[str]]):
    """

    component: str
    args: Any
    path: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    raw_code: Union[Unset, "ExecuteComponentJsonBodyRawCode"] = UNSET
    id: Union[Unset, int] = UNSET
    force_viewer_static_fields: Union[Unset, "ExecuteComponentJsonBodyForceViewerStaticFields"] = UNSET
    force_viewer_one_of_fields: Union[Unset, "ExecuteComponentJsonBodyForceViewerOneOfFields"] = UNSET
    force_viewer_allow_user_resources: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        component = self.component
        args = self.args
        path = self.path
        version = self.version
        raw_code: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.raw_code, Unset):
            raw_code = self.raw_code.to_dict()

        id = self.id
        force_viewer_static_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.force_viewer_static_fields, Unset):
            force_viewer_static_fields = self.force_viewer_static_fields.to_dict()

        force_viewer_one_of_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.force_viewer_one_of_fields, Unset):
            force_viewer_one_of_fields = self.force_viewer_one_of_fields.to_dict()

        force_viewer_allow_user_resources: Union[Unset, List[str]] = UNSET
        if not isinstance(self.force_viewer_allow_user_resources, Unset):
            force_viewer_allow_user_resources = self.force_viewer_allow_user_resources

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component": component,
                "args": args,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if version is not UNSET:
            field_dict["version"] = version
        if raw_code is not UNSET:
            field_dict["raw_code"] = raw_code
        if id is not UNSET:
            field_dict["id"] = id
        if force_viewer_static_fields is not UNSET:
            field_dict["force_viewer_static_fields"] = force_viewer_static_fields
        if force_viewer_one_of_fields is not UNSET:
            field_dict["force_viewer_one_of_fields"] = force_viewer_one_of_fields
        if force_viewer_allow_user_resources is not UNSET:
            field_dict["force_viewer_allow_user_resources"] = force_viewer_allow_user_resources

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execute_component_json_body_force_viewer_one_of_fields import (
            ExecuteComponentJsonBodyForceViewerOneOfFields,
        )
        from ..models.execute_component_json_body_force_viewer_static_fields import (
            ExecuteComponentJsonBodyForceViewerStaticFields,
        )
        from ..models.execute_component_json_body_raw_code import ExecuteComponentJsonBodyRawCode

        d = src_dict.copy()
        component = d.pop("component")

        args = d.pop("args")

        path = d.pop("path", UNSET)

        version = d.pop("version", UNSET)

        _raw_code = d.pop("raw_code", UNSET)
        raw_code: Union[Unset, ExecuteComponentJsonBodyRawCode]
        if isinstance(_raw_code, Unset):
            raw_code = UNSET
        else:
            raw_code = ExecuteComponentJsonBodyRawCode.from_dict(_raw_code)

        id = d.pop("id", UNSET)

        _force_viewer_static_fields = d.pop("force_viewer_static_fields", UNSET)
        force_viewer_static_fields: Union[Unset, ExecuteComponentJsonBodyForceViewerStaticFields]
        if isinstance(_force_viewer_static_fields, Unset):
            force_viewer_static_fields = UNSET
        else:
            force_viewer_static_fields = ExecuteComponentJsonBodyForceViewerStaticFields.from_dict(
                _force_viewer_static_fields
            )

        _force_viewer_one_of_fields = d.pop("force_viewer_one_of_fields", UNSET)
        force_viewer_one_of_fields: Union[Unset, ExecuteComponentJsonBodyForceViewerOneOfFields]
        if isinstance(_force_viewer_one_of_fields, Unset):
            force_viewer_one_of_fields = UNSET
        else:
            force_viewer_one_of_fields = ExecuteComponentJsonBodyForceViewerOneOfFields.from_dict(
                _force_viewer_one_of_fields
            )

        force_viewer_allow_user_resources = cast(List[str], d.pop("force_viewer_allow_user_resources", UNSET))

        execute_component_json_body = cls(
            component=component,
            args=args,
            path=path,
            version=version,
            raw_code=raw_code,
            id=id,
            force_viewer_static_fields=force_viewer_static_fields,
            force_viewer_one_of_fields=force_viewer_one_of_fields,
            force_viewer_allow_user_resources=force_viewer_allow_user_resources,
        )

        execute_component_json_body.additional_properties = d
        return execute_component_json_body

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
