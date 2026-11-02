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
    List,
    Union,
    cast,
)

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.execute_app_job_json_body_annotation import (
        ExecuteAppJobJsonBodyAnnotation,
    )


T = TypeVar("T", bound="ExecuteAppJobJsonBody")


@attr.s(auto_attribs=True)
class ExecuteAppJobJsonBody:
    """
    ### Attributes:
    * `ancestor (str)`: The job name of the ancestor App. This will be used for cleaning up this job when the ancestor App is deleted. Example: od-c2-d2-e61
    * `ontology (str)`: Ontology Example: os_ontology_v1
    * `image (Union[Unset, str])`: The docker image name. E.g. python:3.11 Example: python:3.11
    * `is_frontend (Union[Unset, bool])`: If true, the job will have a public URL and will be accessible from the frontend. Example: True
    * `archive (Union[Unset, str])`: The URL of the zip file containing the source code Example: https://somewhere.com/archive.zip
    * `manifest (Union[Unset, str])`: Optional manifest content as a string. Takes precedence over archive and ancestor's manifest.
    * `annotation (Union[Unset, ExecuteAppJobJsonBodyAnnotation])`: A key value bag of strings to store additional information. Keys must start with 'app.octostar.com/'. Example: {'app.octostar.com/author': 'John Doe'}
    * `commands (Union[Unset, List[str]])`: List of command strings to execute. Example: ['wget https://example.com/my.data.txt', 'python worker.py my.data.txt']
    """

    ancestor: str
    ontology: str
    image: Union[Unset, str] = UNSET
    is_frontend: Union[Unset, bool] = True
    archive: Union[Unset, str] = UNSET
    manifest: Union[Unset, str] = UNSET
    annotation: Union[Unset, "ExecuteAppJobJsonBodyAnnotation"] = UNSET
    commands: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.execute_app_job_json_body_annotation import (
            ExecuteAppJobJsonBodyAnnotation,
        )

        ancestor = self.ancestor
        ontology = self.ontology
        image = self.image
        is_frontend = self.is_frontend
        archive = self.archive
        manifest = self.manifest
        annotation: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.annotation, Unset):
            annotation = self.annotation.to_dict()

        commands: Union[Unset, List[str]] = UNSET
        if not isinstance(self.commands, Unset):
            commands = self.commands

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ancestor": ancestor,
                "ontology": ontology,
            }
        )
        if image is not UNSET:
            field_dict["image"] = image
        if is_frontend is not UNSET:
            field_dict["is_frontend"] = is_frontend
        if archive is not UNSET:
            field_dict["archive"] = archive
        if manifest is not UNSET:
            field_dict["manifest"] = manifest
        if annotation is not UNSET:
            field_dict["annotation"] = annotation
        if commands is not UNSET:
            field_dict["commands"] = commands

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execute_app_job_json_body_annotation import (
            ExecuteAppJobJsonBodyAnnotation,
        )

        d = src_dict.copy()
        ancestor = d.pop("ancestor")

        ontology = d.pop("ontology")

        image = d.pop("image", UNSET)

        is_frontend = d.pop("is_frontend", UNSET)

        archive = d.pop("archive", UNSET)

        manifest = d.pop("manifest", UNSET)

        _annotation = d.pop("annotation", UNSET)
        annotation: Union[Unset, ExecuteAppJobJsonBodyAnnotation]
        if isinstance(_annotation, Unset):
            annotation = UNSET
        else:
            annotation = ExecuteAppJobJsonBodyAnnotation.from_dict(_annotation)

        commands = cast(List[str], d.pop("commands", UNSET))

        execute_app_job_json_body = cls(
            ancestor=ancestor,
            ontology=ontology,
            image=image,
            is_frontend=is_frontend,
            archive=archive,
            manifest=manifest,
            annotation=annotation,
            commands=commands,
        )

        execute_app_job_json_body.additional_properties = d
        return execute_app_job_json_body

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
