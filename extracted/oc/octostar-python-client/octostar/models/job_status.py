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
    from ..models.job_status_labels import JobStatusLabels


T = TypeVar("T", bound="JobStatus")


@attr.s(auto_attribs=True)
class JobStatus:
    """
    ### Attributes:
    * `active (Union[Unset, int])`: The active status of the job
    * `completion_time (Union[Unset, None, datetime.datetime])`: The completion time of the job
    * `creation_timestamp (Union[Unset, datetime.datetime])`: The creation timestamp of the job
    * `failed (Union[Unset, None, int])`: If the job has failed
    * `labels (Union[Unset, JobStatusLabels])`: Labels assigned to the job
    * `name (Union[Unset, str])`: The name of the job
    * `ready (Union[Unset, int])`: The ready status of the job
    * `start_time (Union[Unset, datetime.datetime])`: The start time of the job
    * `succeeded (Union[Unset, None, int])`: If the job has succeeded
    * `uid (Union[Unset, str])`: The unique identifier of the job
    * `url (Union[Unset, str])`: The current URL of the job.
    """

    active: Union[Unset, int] = UNSET
    completion_time: Union[Unset, None, datetime.datetime] = UNSET
    creation_timestamp: Union[Unset, datetime.datetime] = UNSET
    failed: Union[Unset, None, int] = UNSET
    labels: Union[Unset, "JobStatusLabels"] = UNSET
    name: Union[Unset, str] = UNSET
    ready: Union[Unset, int] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    succeeded: Union[Unset, None, int] = UNSET
    uid: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.job_status_labels import JobStatusLabels

        active = self.active
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
        ready = self.ready
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        succeeded = self.succeeded
        uid = self.uid
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
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
        if ready is not UNSET:
            field_dict["ready"] = ready
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if succeeded is not UNSET:
            field_dict["succeeded"] = succeeded
        if uid is not UNSET:
            field_dict["uid"] = uid
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.job_status_labels import JobStatusLabels

        d = src_dict.copy()
        active = d.pop("active", UNSET)

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
        labels: Union[Unset, JobStatusLabels]
        if isinstance(_labels, Unset):
            labels = UNSET
        else:
            labels = JobStatusLabels.from_dict(_labels)

        name = d.pop("name", UNSET)

        ready = d.pop("ready", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        succeeded = d.pop("succeeded", UNSET)

        uid = d.pop("uid", UNSET)

        url = d.pop("url", UNSET)

        job_status = cls(
            active=active,
            completion_time=completion_time,
            creation_timestamp=creation_timestamp,
            failed=failed,
            labels=labels,
            name=name,
            ready=ready,
            start_time=start_time,
            succeeded=succeeded,
            uid=uid,
            url=url,
        )

        job_status.additional_properties = d
        return job_status

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
