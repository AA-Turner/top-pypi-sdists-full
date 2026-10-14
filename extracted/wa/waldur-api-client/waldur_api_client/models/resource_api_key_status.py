import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.resource_api_key_action import ResourceApiKeyAction
from ..models.resource_api_key_state import ResourceApiKeyState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_api_key_status_current_usages_type_0 import ResourceApiKeyStatusCurrentUsagesType0
    from ..models.resource_api_key_status_limits_type_0 import ResourceApiKeyStatusLimitsType0


T = TypeVar("T", bound="ResourceApiKeyStatus")


@_attrs_define
class ResourceApiKeyStatus:
    """
    Attributes:
        uuid (UUID):
        resource_uuid (UUID):
        resource_backend_id (str):
        pending_action (Union[BlankEnum, ResourceApiKeyAction]):
        modified (datetime.datetime):
        user_uuid (Union[None, UUID]):
        user_full_name (Union[None, str]):
        limits (Union['ResourceApiKeyStatusLimitsType0', None]):
        allowed_models (Union[None, list[str]]):
        current_usages (Union['ResourceApiKeyStatusCurrentUsagesType0', None]):
        usage_period (Union[None, datetime.date]):
        paused_by_limit (Union[None, bool]):
        client_id (Union[Unset, str]):
        state (Union[Unset, ResourceApiKeyState]):
        issued_at (Union[None, Unset, datetime.datetime]): When the agent last stored a value for this key: its creation
            or its latest rotation. Unlike modified, a pause or an edit leaves it alone.
        error_message (Union[Unset, str]):
    """

    uuid: UUID
    resource_uuid: UUID
    resource_backend_id: str
    pending_action: Union[BlankEnum, ResourceApiKeyAction]
    modified: datetime.datetime
    user_uuid: Union[None, UUID]
    user_full_name: Union[None, str]
    limits: Union["ResourceApiKeyStatusLimitsType0", None]
    allowed_models: Union[None, list[str]]
    current_usages: Union["ResourceApiKeyStatusCurrentUsagesType0", None]
    usage_period: Union[None, datetime.date]
    paused_by_limit: Union[None, bool]
    client_id: Union[Unset, str] = UNSET
    state: Union[Unset, ResourceApiKeyState] = UNSET
    issued_at: Union[None, Unset, datetime.datetime] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_api_key_status_current_usages_type_0 import ResourceApiKeyStatusCurrentUsagesType0
        from ..models.resource_api_key_status_limits_type_0 import ResourceApiKeyStatusLimitsType0

        uuid = str(self.uuid)

        resource_uuid = str(self.resource_uuid)

        resource_backend_id = self.resource_backend_id

        pending_action: str
        if isinstance(self.pending_action, ResourceApiKeyAction):
            pending_action = self.pending_action.value
        else:
            pending_action = self.pending_action.value

        modified = self.modified.isoformat()

        user_uuid: Union[None, str]
        if isinstance(self.user_uuid, UUID):
            user_uuid = str(self.user_uuid)
        else:
            user_uuid = self.user_uuid

        user_full_name: Union[None, str]
        user_full_name = self.user_full_name

        limits: Union[None, dict[str, Any]]
        if isinstance(self.limits, ResourceApiKeyStatusLimitsType0):
            limits = self.limits.to_dict()
        else:
            limits = self.limits

        allowed_models: Union[None, list[str]]
        if isinstance(self.allowed_models, list):
            allowed_models = self.allowed_models

        else:
            allowed_models = self.allowed_models

        current_usages: Union[None, dict[str, Any]]
        if isinstance(self.current_usages, ResourceApiKeyStatusCurrentUsagesType0):
            current_usages = self.current_usages.to_dict()
        else:
            current_usages = self.current_usages

        usage_period: Union[None, str]
        if isinstance(self.usage_period, datetime.date):
            usage_period = self.usage_period.isoformat()
        else:
            usage_period = self.usage_period

        paused_by_limit: Union[None, bool]
        paused_by_limit = self.paused_by_limit

        client_id = self.client_id

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        issued_at: Union[None, Unset, str]
        if isinstance(self.issued_at, Unset):
            issued_at = UNSET
        elif isinstance(self.issued_at, datetime.datetime):
            issued_at = self.issued_at.isoformat()
        else:
            issued_at = self.issued_at

        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource_uuid": resource_uuid,
                "resource_backend_id": resource_backend_id,
                "pending_action": pending_action,
                "modified": modified,
                "user_uuid": user_uuid,
                "user_full_name": user_full_name,
                "limits": limits,
                "allowed_models": allowed_models,
                "current_usages": current_usages,
                "usage_period": usage_period,
                "paused_by_limit": paused_by_limit,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if state is not UNSET:
            field_dict["state"] = state
        if issued_at is not UNSET:
            field_dict["issued_at"] = issued_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_api_key_status_current_usages_type_0 import ResourceApiKeyStatusCurrentUsagesType0
        from ..models.resource_api_key_status_limits_type_0 import ResourceApiKeyStatusLimitsType0

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_backend_id = d.pop("resource_backend_id")

        def _parse_pending_action(data: object) -> Union[BlankEnum, ResourceApiKeyAction]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pending_action_type_0 = ResourceApiKeyAction(data)

                return pending_action_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            pending_action_type_1 = BlankEnum(data)

            return pending_action_type_1

        pending_action = _parse_pending_action(d.pop("pending_action"))

        modified = isoparse(d.pop("modified"))

        def _parse_user_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_uuid_type_0 = UUID(data)

                return user_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        user_uuid = _parse_user_uuid(d.pop("user_uuid"))

        def _parse_user_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_full_name = _parse_user_full_name(d.pop("user_full_name"))

        def _parse_limits(data: object) -> Union["ResourceApiKeyStatusLimitsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                limits_type_0 = ResourceApiKeyStatusLimitsType0.from_dict(data)

                return limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeyStatusLimitsType0", None], data)

        limits = _parse_limits(d.pop("limits"))

        def _parse_allowed_models(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_models_type_0 = cast(list[str], data)

                return allowed_models_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        allowed_models = _parse_allowed_models(d.pop("allowed_models"))

        def _parse_current_usages(data: object) -> Union["ResourceApiKeyStatusCurrentUsagesType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_usages_type_0 = ResourceApiKeyStatusCurrentUsagesType0.from_dict(data)

                return current_usages_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeyStatusCurrentUsagesType0", None], data)

        current_usages = _parse_current_usages(d.pop("current_usages"))

        def _parse_usage_period(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                usage_period_type_0 = isoparse(data).date()

                return usage_period_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        usage_period = _parse_usage_period(d.pop("usage_period"))

        def _parse_paused_by_limit(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        paused_by_limit = _parse_paused_by_limit(d.pop("paused_by_limit"))

        client_id = d.pop("client_id", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, ResourceApiKeyState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ResourceApiKeyState(_state)

        def _parse_issued_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                issued_at_type_0 = isoparse(data)

                return issued_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        issued_at = _parse_issued_at(d.pop("issued_at", UNSET))

        error_message = d.pop("error_message", UNSET)

        resource_api_key_status = cls(
            uuid=uuid,
            resource_uuid=resource_uuid,
            resource_backend_id=resource_backend_id,
            pending_action=pending_action,
            modified=modified,
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            limits=limits,
            allowed_models=allowed_models,
            current_usages=current_usages,
            usage_period=usage_period,
            paused_by_limit=paused_by_limit,
            client_id=client_id,
            state=state,
            issued_at=issued_at,
            error_message=error_message,
        )

        resource_api_key_status.additional_properties = d
        return resource_api_key_status

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
