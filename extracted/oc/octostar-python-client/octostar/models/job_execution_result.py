from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="JobExecutionResult")


@attr.s(auto_attribs=True)
class JobExecutionResult:
    """
    ### Attributes:
    * `job_id (Union[Unset, str])`: None Example: oj-c2-d2-e61-j6a1
    * `pod_name (Union[Unset, str])`: None Example: oj-os-ontology-v1-s-scarduzio-c3c61-kg5gl
    * `job_name (Union[Unset, str])`: None Example: oj-c2-d2-e61-j6a1
    * `ancestor (Union[Unset, str])`: None Example: od-c2-d2-e61
    * `status (Union[Unset, str])`: None Example: Running
    * `app_id (Union[Unset, str])`: None
    * `app_name (Union[Unset, str])`: None Example: MyApp
    * `app_url (Union[Unset, str])`: None Example: https://home.local.test/apps/my-service/
    * `os_entity_id (Union[Unset, str])`: None Example: e61b7226-b3ac-4974-b9f7-66f4eda5b51d
    * `os_workspace (Union[Unset, str])`: None Example: d2cc4d61-3f0a-499f-a867-75bfd29a1d08
    """

    job_id: Union[Unset, str] = UNSET
    pod_name: Union[Unset, str] = UNSET
    job_name: Union[Unset, str] = UNSET
    ancestor: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    app_id: Union[Unset, str] = UNSET
    app_name: Union[Unset, str] = UNSET
    app_url: Union[Unset, str] = UNSET
    os_entity_id: Union[Unset, str] = UNSET
    os_workspace: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        pod_name = self.pod_name
        job_name = self.job_name
        ancestor = self.ancestor
        status = self.status
        app_id = self.app_id
        app_name = self.app_name
        app_url = self.app_url
        os_entity_id = self.os_entity_id
        os_workspace = self.os_workspace

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if pod_name is not UNSET:
            field_dict["pod_name"] = pod_name
        if job_name is not UNSET:
            field_dict["job_name"] = job_name
        if ancestor is not UNSET:
            field_dict["ancestor"] = ancestor
        if status is not UNSET:
            field_dict["status"] = status
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if app_name is not UNSET:
            field_dict["app_name"] = app_name
        if app_url is not UNSET:
            field_dict["app_url"] = app_url
        if os_entity_id is not UNSET:
            field_dict["os_entity_id"] = os_entity_id
        if os_workspace is not UNSET:
            field_dict["os_workspace"] = os_workspace

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id", UNSET)

        pod_name = d.pop("pod_name", UNSET)

        job_name = d.pop("job_name", UNSET)

        ancestor = d.pop("ancestor", UNSET)

        status = d.pop("status", UNSET)

        app_id = d.pop("app_id", UNSET)

        app_name = d.pop("app_name", UNSET)

        app_url = d.pop("app_url", UNSET)

        os_entity_id = d.pop("os_entity_id", UNSET)

        os_workspace = d.pop("os_workspace", UNSET)

        job_execution_result = cls(
            job_id=job_id,
            pod_name=pod_name,
            job_name=job_name,
            ancestor=ancestor,
            status=status,
            app_id=app_id,
            app_name=app_name,
            app_url=app_url,
            os_entity_id=os_entity_id,
            os_workspace=os_workspace,
        )

        job_execution_result.additional_properties = d
        return job_execution_result

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
