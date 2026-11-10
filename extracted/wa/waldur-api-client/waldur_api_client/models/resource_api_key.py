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
    from ..models.resource_api_key_current_usages_type_0 import ResourceApiKeyCurrentUsagesType0
    from ..models.resource_api_key_limits_type_0 import ResourceApiKeyLimitsType0
    from ..models.resource_api_key_spending_limits_type_0 import ResourceApiKeySpendingLimitsType0
    from ..models.spending_limit_usage import SpendingLimitUsage


T = TypeVar("T", bound="ResourceApiKey")


@_attrs_define
class ResourceApiKey:
    """
    Attributes:
        uuid (UUID):
        resource_uuid (UUID):
        resource_backend_id (str):
        pending_action (Union[BlankEnum, ResourceApiKeyAction]):
        modified (datetime.datetime):
        user_uuid (Union[None, UUID]):
        user_full_name (Union[None, str]):
        limits (Union['ResourceApiKeyLimitsType0', None]): The month limits of spending_limits, per component type, for
            clients that know only monthly limits.
        spending_limits (Union['ResourceApiKeySpendingLimitsType0', None]): Limits per component type and period.
        spending_limit_status (Union[None, list['SpendingLimitUsage']]):
        allowed_models (Union[None, list[str]]): The key's own model list, as chosen.
        effective_models (Union[None, list[str]]): The models the key can call: the resource's selection, then the key's
            list. The site agent applies this one.
        current_usages (Union['ResourceApiKeyCurrentUsagesType0', None]):
        usage_period (Union[None, datetime.date]):
        paused_by_limit (Union[None, bool]): Waldur paused the key because its usage reached a limit. Such a key is
            resumed automatically once its usage is under its limits again: when the period of the limit resets, or when a
            limit is raised. A total limit never resets, so only raising or clearing it does.
        limit_resumes_at (Union[None, datetime.datetime]): When every limit that paused the key has reset, so that it
            resumes without a new usage report. Empty while a reached total limit holds the key: a total never resets, so
            the key resumes only when that limit is raised or cleared.
        api_key (str):
        client_id (Union[Unset, str]):
        description (Union[Unset, str]):
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
    limits: Union["ResourceApiKeyLimitsType0", None]
    spending_limits: Union["ResourceApiKeySpendingLimitsType0", None]
    spending_limit_status: Union[None, list["SpendingLimitUsage"]]
    allowed_models: Union[None, list[str]]
    effective_models: Union[None, list[str]]
    current_usages: Union["ResourceApiKeyCurrentUsagesType0", None]
    usage_period: Union[None, datetime.date]
    paused_by_limit: Union[None, bool]
    limit_resumes_at: Union[None, datetime.datetime]
    api_key: str
    client_id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, ResourceApiKeyState] = UNSET
    issued_at: Union[None, Unset, datetime.datetime] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_api_key_current_usages_type_0 import ResourceApiKeyCurrentUsagesType0
        from ..models.resource_api_key_limits_type_0 import ResourceApiKeyLimitsType0
        from ..models.resource_api_key_spending_limits_type_0 import ResourceApiKeySpendingLimitsType0

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
        if isinstance(self.limits, ResourceApiKeyLimitsType0):
            limits = self.limits.to_dict()
        else:
            limits = self.limits

        spending_limits: Union[None, dict[str, Any]]
        if isinstance(self.spending_limits, ResourceApiKeySpendingLimitsType0):
            spending_limits = self.spending_limits.to_dict()
        else:
            spending_limits = self.spending_limits

        spending_limit_status: Union[None, list[dict[str, Any]]]
        if isinstance(self.spending_limit_status, list):
            spending_limit_status = []
            for spending_limit_status_type_0_item_data in self.spending_limit_status:
                spending_limit_status_type_0_item = spending_limit_status_type_0_item_data.to_dict()
                spending_limit_status.append(spending_limit_status_type_0_item)

        else:
            spending_limit_status = self.spending_limit_status

        allowed_models: Union[None, list[str]]
        if isinstance(self.allowed_models, list):
            allowed_models = self.allowed_models

        else:
            allowed_models = self.allowed_models

        effective_models: Union[None, list[str]]
        if isinstance(self.effective_models, list):
            effective_models = self.effective_models

        else:
            effective_models = self.effective_models

        current_usages: Union[None, dict[str, Any]]
        if isinstance(self.current_usages, ResourceApiKeyCurrentUsagesType0):
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

        limit_resumes_at: Union[None, str]
        if isinstance(self.limit_resumes_at, datetime.datetime):
            limit_resumes_at = self.limit_resumes_at.isoformat()
        else:
            limit_resumes_at = self.limit_resumes_at

        api_key = self.api_key

        client_id = self.client_id

        description = self.description

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
                "spending_limits": spending_limits,
                "spending_limit_status": spending_limit_status,
                "allowed_models": allowed_models,
                "effective_models": effective_models,
                "current_usages": current_usages,
                "usage_period": usage_period,
                "paused_by_limit": paused_by_limit,
                "limit_resumes_at": limit_resumes_at,
                "api_key": api_key,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if description is not UNSET:
            field_dict["description"] = description
        if state is not UNSET:
            field_dict["state"] = state
        if issued_at is not UNSET:
            field_dict["issued_at"] = issued_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_api_key_current_usages_type_0 import ResourceApiKeyCurrentUsagesType0
        from ..models.resource_api_key_limits_type_0 import ResourceApiKeyLimitsType0
        from ..models.resource_api_key_spending_limits_type_0 import ResourceApiKeySpendingLimitsType0
        from ..models.spending_limit_usage import SpendingLimitUsage

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

        def _parse_limits(data: object) -> Union["ResourceApiKeyLimitsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                limits_type_0 = ResourceApiKeyLimitsType0.from_dict(data)

                return limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeyLimitsType0", None], data)

        limits = _parse_limits(d.pop("limits"))

        def _parse_spending_limits(data: object) -> Union["ResourceApiKeySpendingLimitsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                spending_limits_type_0 = ResourceApiKeySpendingLimitsType0.from_dict(data)

                return spending_limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeySpendingLimitsType0", None], data)

        spending_limits = _parse_spending_limits(d.pop("spending_limits"))

        def _parse_spending_limit_status(data: object) -> Union[None, list["SpendingLimitUsage"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                spending_limit_status_type_0 = []
                _spending_limit_status_type_0 = data
                for spending_limit_status_type_0_item_data in _spending_limit_status_type_0:
                    spending_limit_status_type_0_item = SpendingLimitUsage.from_dict(
                        spending_limit_status_type_0_item_data
                    )

                    spending_limit_status_type_0.append(spending_limit_status_type_0_item)

                return spending_limit_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["SpendingLimitUsage"]], data)

        spending_limit_status = _parse_spending_limit_status(d.pop("spending_limit_status"))

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

        def _parse_effective_models(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                effective_models_type_0 = cast(list[str], data)

                return effective_models_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        effective_models = _parse_effective_models(d.pop("effective_models"))

        def _parse_current_usages(data: object) -> Union["ResourceApiKeyCurrentUsagesType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                current_usages_type_0 = ResourceApiKeyCurrentUsagesType0.from_dict(data)

                return current_usages_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeyCurrentUsagesType0", None], data)

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

        def _parse_limit_resumes_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                limit_resumes_at_type_0 = isoparse(data)

                return limit_resumes_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        limit_resumes_at = _parse_limit_resumes_at(d.pop("limit_resumes_at"))

        api_key = d.pop("api_key")

        client_id = d.pop("client_id", UNSET)

        description = d.pop("description", UNSET)

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

        resource_api_key = cls(
            uuid=uuid,
            resource_uuid=resource_uuid,
            resource_backend_id=resource_backend_id,
            pending_action=pending_action,
            modified=modified,
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            limits=limits,
            spending_limits=spending_limits,
            spending_limit_status=spending_limit_status,
            allowed_models=allowed_models,
            effective_models=effective_models,
            current_usages=current_usages,
            usage_period=usage_period,
            paused_by_limit=paused_by_limit,
            limit_resumes_at=limit_resumes_at,
            api_key=api_key,
            client_id=client_id,
            description=description,
            state=state,
            issued_at=issued_at,
            error_message=error_message,
        )

        resource_api_key.additional_properties = d
        return resource_api_key

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
