import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_oidc_signing_status_response_200_signer_breaker import GetOidcSigningStatusResponse200SignerBreaker
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetOidcSigningStatusResponse200Signer")


@_attrs_define
class GetOidcSigningStatusResponse200Signer:
    """set when an external signer is configured

    Attributes:
        breaker (GetOidcSigningStatusResponse200SignerBreaker):
        max_rps (float):
        current_rps (float):
        last_refresh_success (Union[Unset, datetime.datetime]):
        last_refresh_error (Union[Unset, str]):
        keys_from_store (Union[Unset, bool]): the keys served are those stored by the last accepted listing, the signer
            has not answered this server yet
        tls_files_error (Union[Unset, str]): why the mTLS files on disk are not the ones in use
    """

    breaker: GetOidcSigningStatusResponse200SignerBreaker
    max_rps: float
    current_rps: float
    last_refresh_success: Union[Unset, datetime.datetime] = UNSET
    last_refresh_error: Union[Unset, str] = UNSET
    keys_from_store: Union[Unset, bool] = UNSET
    tls_files_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        breaker = self.breaker.value

        max_rps = self.max_rps
        current_rps = self.current_rps
        last_refresh_success: Union[Unset, str] = UNSET
        if not isinstance(self.last_refresh_success, Unset):
            last_refresh_success = self.last_refresh_success.isoformat()

        last_refresh_error = self.last_refresh_error
        keys_from_store = self.keys_from_store
        tls_files_error = self.tls_files_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "breaker": breaker,
                "max_rps": max_rps,
                "current_rps": current_rps,
            }
        )
        if last_refresh_success is not UNSET:
            field_dict["last_refresh_success"] = last_refresh_success
        if last_refresh_error is not UNSET:
            field_dict["last_refresh_error"] = last_refresh_error
        if keys_from_store is not UNSET:
            field_dict["keys_from_store"] = keys_from_store
        if tls_files_error is not UNSET:
            field_dict["tls_files_error"] = tls_files_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        breaker = GetOidcSigningStatusResponse200SignerBreaker(d.pop("breaker"))

        max_rps = d.pop("max_rps")

        current_rps = d.pop("current_rps")

        _last_refresh_success = d.pop("last_refresh_success", UNSET)
        last_refresh_success: Union[Unset, datetime.datetime]
        if isinstance(_last_refresh_success, Unset):
            last_refresh_success = UNSET
        else:
            last_refresh_success = isoparse(_last_refresh_success)

        last_refresh_error = d.pop("last_refresh_error", UNSET)

        keys_from_store = d.pop("keys_from_store", UNSET)

        tls_files_error = d.pop("tls_files_error", UNSET)

        get_oidc_signing_status_response_200_signer = cls(
            breaker=breaker,
            max_rps=max_rps,
            current_rps=current_rps,
            last_refresh_success=last_refresh_success,
            last_refresh_error=last_refresh_error,
            keys_from_store=keys_from_store,
            tls_files_error=tls_files_error,
        )

        get_oidc_signing_status_response_200_signer.additional_properties = d
        return get_oidc_signing_status_response_200_signer

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
