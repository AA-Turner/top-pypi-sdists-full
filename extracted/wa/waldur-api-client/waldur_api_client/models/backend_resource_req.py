import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.backend_resource_req_state_enum import BackendResourceReqStateEnum

T = TypeVar("T", bound="BackendResourceReq")


@_attrs_define
class BackendResourceReq:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        started (Union[None, datetime.datetime]): Time when request processing started
        finished (Union[None, datetime.datetime]): Time when request processing finished
        state (BackendResourceReqStateEnum):
        offering (UUID):
        offering_name (str):
        offering_url (str):
        error_message (str):
        error_traceback (str):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    started: Union[None, datetime.datetime]
    finished: Union[None, datetime.datetime]
    state: BackendResourceReqStateEnum
    offering: UUID
    offering_name: str
    offering_url: str
    error_message: str
    error_traceback: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        started: Union[None, str]
        if isinstance(self.started, datetime.datetime):
            started = self.started.isoformat()
        else:
            started = self.started

        finished: Union[None, str]
        if isinstance(self.finished, datetime.datetime):
            finished = self.finished.isoformat()
        else:
            finished = self.finished

        state = self.state.value

        offering = str(self.offering)

        offering_name = self.offering_name

        offering_url = self.offering_url

        error_message = self.error_message

        error_traceback = self.error_traceback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "started": started,
                "finished": finished,
                "state": state,
                "offering": offering,
                "offering_name": offering_name,
                "offering_url": offering_url,
                "error_message": error_message,
                "error_traceback": error_traceback,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        def _parse_started(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_type_0 = isoparse(data)

                return started_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started = _parse_started(d.pop("started"))

        def _parse_finished(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                finished_type_0 = isoparse(data)

                return finished_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        finished = _parse_finished(d.pop("finished"))

        state = BackendResourceReqStateEnum(d.pop("state"))

        offering = UUID(d.pop("offering"))

        offering_name = d.pop("offering_name")

        offering_url = d.pop("offering_url")

        error_message = d.pop("error_message")

        error_traceback = d.pop("error_traceback")

        backend_resource_req = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            started=started,
            finished=finished,
            state=state,
            offering=offering,
            offering_name=offering_name,
            offering_url=offering_url,
            error_message=error_message,
            error_traceback=error_traceback,
        )

        backend_resource_req.additional_properties = d
        return backend_resource_req

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
