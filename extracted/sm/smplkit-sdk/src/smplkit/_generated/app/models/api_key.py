from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.api_key_scopes import ApiKeyScopes


T = TypeVar("T", bound="ApiKey")


@_attrs_define
class ApiKey:
    """An API key used by SDKs, scripts, and other programmatic clients to
    authenticate with the smplkit API on behalf of the account.

    The full key value is returned in plaintext on the create response and
    is otherwise unavailable — record it somewhere safe immediately after
    creation.

        Example:
            {'created_at': '2026-03-20T11:02:16.616Z', 'created_by': 'd290f1ee-6c54-4b01-90e6-d701748f0851', 'expires_at':
                '2027-03-20T11:02:16.616Z', 'key': 'sk_api_a1b2c3d4e5f6g7h8i9j0', 'last_used_at': '2026-03-19T08:45:00.000Z',
                'name': 'Production API Key', 'scopes': {}, 'status': 'ACTIVE', 'updated_at': '2026-03-20T11:02:16.616Z'}

        Attributes:
            name (str): Human-readable name for the key.
            status (None | str | Unset): Lifecycle state of the key. `ACTIVE` keys may be used to authenticate; `REVOKED`
                keys are rejected.
            key (None | str | Unset): The bearer token value. Returned in plaintext on the create response so the caller can
                capture it; subsequent reads return the same value for round-tripping.
            scopes (ApiKeyScopes | Unset): Scope restrictions applied to the key, as a JSON object mapping dimension names
                to arrays of allowed values. An empty object (the default) grants unrestricted access. The `environments`
                dimension lists the environment keys the key may operate in (for example `{"environments": ["production"]}`); a
                request's environment must be one of them. A dimension that is absent or set to an empty array is unrestricted
                in that dimension. Example: {'environments': ['production']}.
            created_by (None | str | Unset): UUID of the user who created the key.
            expires_at (datetime.datetime | None | Unset): Optional expiry timestamp. After this time, the key is rejected.
                Omit for keys that do not expire.
            last_used_at (datetime.datetime | None | Unset): When the key was most recently used to authenticate.
            created_at (datetime.datetime | None | Unset): When the key was created.
            updated_at (datetime.datetime | None | Unset): When the key was last modified.
    """

    name: str
    status: None | str | Unset = UNSET
    key: None | str | Unset = UNSET
    scopes: ApiKeyScopes | Unset = UNSET
    created_by: None | str | Unset = UNSET
    expires_at: datetime.datetime | None | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        scopes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes.to_dict()

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        expires_at: None | str | Unset
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if key is not UNSET:
            field_dict["key"] = key
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_key_scopes import ApiKeyScopes

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        _scopes = d.pop("scopes", UNSET)
        scopes: ApiKeyScopes | Unset
        if isinstance(_scopes, Unset):
            scopes = UNSET
        else:
            scopes = ApiKeyScopes.from_dict(_scopes)

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_expires_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = isoparse(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        api_key = cls(
            name=name,
            status=status,
            key=key,
            scopes=scopes,
            created_by=created_by,
            expires_at=expires_at,
            last_used_at=last_used_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        api_key.additional_properties = d
        return api_key

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
