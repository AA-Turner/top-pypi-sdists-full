from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_application_request_answers import RancherApplicationRequestAnswers


T = TypeVar("T", bound="RancherApplicationRequest")


@_attrs_define
class RancherApplicationRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        template (str):
        rancher_project (str):
        version (str):
        description (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        runtime_state (Union[Unset, str]):
        namespace (Union[Unset, str]):
        namespace_name (Union[Unset, str]):
        answers (Union[Unset, RancherApplicationRequestAnswers]):
    """

    name: str
    service_settings: str
    project: str
    template: str
    rancher_project: str
    version: str
    description: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    runtime_state: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    namespace_name: Union[Unset, str] = UNSET
    answers: Union[Unset, "RancherApplicationRequestAnswers"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        template = self.template

        rancher_project = self.rancher_project

        version = self.version

        description = self.description

        error_message = self.error_message

        error_traceback = self.error_traceback

        backend_id = self.backend_id

        runtime_state = self.runtime_state

        namespace = self.namespace

        namespace_name = self.namespace_name

        answers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.answers, Unset):
            answers = self.answers.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "template": template,
                "rancher_project": rancher_project,
                "version": version,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if namespace_name is not UNSET:
            field_dict["namespace_name"] = namespace_name
        if answers is not UNSET:
            field_dict["answers"] = answers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_application_request_answers import RancherApplicationRequestAnswers

        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        template = d.pop("template")

        rancher_project = d.pop("rancher_project")

        version = d.pop("version")

        description = d.pop("description", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        runtime_state = d.pop("runtime_state", UNSET)

        namespace = d.pop("namespace", UNSET)

        namespace_name = d.pop("namespace_name", UNSET)

        _answers = d.pop("answers", UNSET)
        answers: Union[Unset, RancherApplicationRequestAnswers]
        if isinstance(_answers, Unset):
            answers = UNSET
        else:
            answers = RancherApplicationRequestAnswers.from_dict(_answers)

        rancher_application_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            template=template,
            rancher_project=rancher_project,
            version=version,
            description=description,
            error_message=error_message,
            error_traceback=error_traceback,
            backend_id=backend_id,
            runtime_state=runtime_state,
            namespace=namespace,
            namespace_name=namespace_name,
            answers=answers,
        )

        rancher_application_request.additional_properties = d
        return rancher_application_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
