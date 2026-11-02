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
import datetime

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.app_status_annotations import AppStatusAnnotations
    from ..models.app_status_labels import AppStatusLabels


T = TypeVar("T", bound="AppStatus")


@attr.s(auto_attribs=True)
class AppStatus:
    """
    ### Attributes:
    * `active (Union[Unset, int])`: The active status of the App Example: 1
    * `app_id (Union[Unset, str])`: Stable app identifier (the Kubernetes deployment name), also on Stopped apps Example: od-c2-d2-e61
    * `app_state (Union[Unset, str])`: The current state of the app Example: booting
    * `app_url (Union[Unset, None, str])`: The URL where the app can be accessed; None unless the app is deployed Example: https://home.local.test/apps/od-c2-d2-e61/
    * `annotations (Union[Unset, AppStatusAnnotations])`: Annotations for the app Example: {'deployment.kubernetes.io/revision': '1', 'os-app-name': 'MyAPP', 'os-app-title': 'MyAPP is awesome', 'os-manifest': '...', 'os-ontology': 'os_ontology_v1', 'os-username': 'admin'}
    * `completion_time (Union[Unset, None, datetime.datetime])`: The completion time of the App
    * `creation_timestamp (Union[Unset, datetime.datetime])`: The creation timestamp of the App Example: 2025-04-09T08:34:00+00:00
    * `failed (Union[Unset, None, int])`: If the App has failed
    * `labels (Union[Unset, AppStatusLabels])`: Labels assigned to the App Example: {'app.kubernetes.io/instance': 'local', 'app.kubernetes.io/name': 'my-service', 'os-alias': 'my-service', 'os-ancestor': 'od-c2-d2-e61', 'os-app-id': 'od-c2-d2-e61', 'os-deployment-id': 'od-c2-d2-e61', 'os-entity-id': 'e61b7226-b3ac-4974-b9f7-66f4eda5b51d', 'os-instance-type': 'normal', 'os-needs-ingress': 'true', 'os-ontology': 'os_ontology_v1', 'os-username': 'admin', 'os-workload-type': 'frontend', 'os-workspace': 'd2cc4d61-3f0a-499f-a867-75bfd29a1d08'}
    * `name (Union[Unset, str])`: The name of the App Example: od-c2-d2-e61
    * `namespace (Union[Unset, str])`: The namespace where the app is deployed Example: octostar-main
    * `ready (Union[Unset, int])`: The ready status of the App
    * `start_time (Union[Unset, datetime.datetime])`: The start time of the App Example: 2025-04-09T08:34:00+00:00
    * `succeeded (Union[Unset, None, int])`: If the App has succeeded
    * `uid (Union[Unset, str])`: The unique identifier of the App Example: 5c4c446c-3399-4e23-9f8b-b3d129ae3801
    * `state (Union[Unset, str])`: The current state of the job (for worker jobs) Example: running
    """

    active: Union[Unset, int] = UNSET
    app_id: Union[Unset, str] = UNSET
    app_state: Union[Unset, str] = UNSET
    app_url: Union[Unset, None, str] = UNSET
    annotations: Union[Unset, "AppStatusAnnotations"] = UNSET
    completion_time: Union[Unset, None, datetime.datetime] = UNSET
    creation_timestamp: Union[Unset, datetime.datetime] = UNSET
    failed: Union[Unset, None, int] = UNSET
    labels: Union[Unset, "AppStatusLabels"] = UNSET
    name: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    ready: Union[Unset, int] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    succeeded: Union[Unset, None, int] = UNSET
    uid: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.app_status_annotations import AppStatusAnnotations
        from ..models.app_status_labels import AppStatusLabels

        active = self.active
        app_id = self.app_id
        app_state = self.app_state
        app_url = self.app_url
        annotations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        completion_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.completion_time, Unset):
            completion_time = (
                self.completion_time.isoformat() if self.completion_time else None
            )

        creation_timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.creation_timestamp, Unset):
            creation_timestamp = self.creation_timestamp.isoformat()

        failed = self.failed
        labels: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels.to_dict()

        name = self.name
        namespace = self.namespace
        ready = self.ready
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        succeeded = self.succeeded
        uid = self.uid
        state = self.state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if app_id is not UNSET:
            field_dict["app_id"] = app_id
        if app_state is not UNSET:
            field_dict["app_state"] = app_state
        if app_url is not UNSET:
            field_dict["app_url"] = app_url
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if completion_time is not UNSET:
            field_dict["completion_time"] = completion_time
        if creation_timestamp is not UNSET:
            field_dict["creation_timestamp"] = creation_timestamp
        if failed is not UNSET:
            field_dict["failed"] = failed
        if labels is not UNSET:
            field_dict["labels"] = labels
        if name is not UNSET:
            field_dict["name"] = name
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if ready is not UNSET:
            field_dict["ready"] = ready
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if succeeded is not UNSET:
            field_dict["succeeded"] = succeeded
        if uid is not UNSET:
            field_dict["uid"] = uid
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.app_status_annotations import AppStatusAnnotations
        from ..models.app_status_labels import AppStatusLabels

        d = src_dict.copy()
        active = d.pop("active", UNSET)

        app_id = d.pop("app_id", UNSET)

        app_state = d.pop("app_state", UNSET)

        app_url = d.pop("app_url", UNSET)

        _annotations = d.pop("annotations", UNSET)
        annotations: Union[Unset, AppStatusAnnotations]
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = AppStatusAnnotations.from_dict(_annotations)

        _completion_time = d.pop("completion_time", UNSET)
        completion_time: Union[Unset, None, datetime.datetime]
        if _completion_time is None:
            completion_time = None
        elif isinstance(_completion_time, Unset):
            completion_time = UNSET
        else:
            completion_time = isoparse(_completion_time)

        _creation_timestamp = d.pop("creation_timestamp", UNSET)
        creation_timestamp: Union[Unset, datetime.datetime]
        if isinstance(_creation_timestamp, Unset):
            creation_timestamp = UNSET
        else:
            creation_timestamp = isoparse(_creation_timestamp)

        failed = d.pop("failed", UNSET)

        _labels = d.pop("labels", UNSET)
        labels: Union[Unset, AppStatusLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = AppStatusLabels.from_dict(_labels)

        name = d.pop("name", UNSET)

        namespace = d.pop("namespace", UNSET)

        ready = d.pop("ready", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        succeeded = d.pop("succeeded", UNSET)

        uid = d.pop("uid", UNSET)

        state = d.pop("state", UNSET)

        app_status = cls(
            active=active,
            app_id=app_id,
            app_state=app_state,
            app_url=app_url,
            annotations=annotations,
            completion_time=completion_time,
            creation_timestamp=creation_timestamp,
            failed=failed,
            labels=labels,
            name=name,
            namespace=namespace,
            ready=ready,
            start_time=start_time,
            succeeded=succeeded,
            uid=uid,
            state=state,
        )

        app_status.additional_properties = d
        return app_status

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
