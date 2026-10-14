from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EmailConfig")


@_attrs_define
class EmailConfig:
    """
    Attributes:
        backend (str): EMAIL_BACKEND class path
        host (str): EMAIL_HOST
        port (Union[None, int]): EMAIL_PORT
        host_user (str): EMAIL_HOST_USER
        has_password (bool): Whether EMAIL_HOST_PASSWORD is set
        use_tls (bool): EMAIL_USE_TLS
        use_ssl (bool): EMAIL_USE_SSL
        timeout (Union[None, int]): EMAIL_TIMEOUT in seconds
        default_from_email (str): DEFAULT_FROM_EMAIL
        default_reply_to_email (str): DEFAULT_REPLY_TO_EMAIL
        subject_prefix (str): EMAIL_SUBJECT_PREFIX
    """

    backend: str
    host: str
    port: Union[None, int]
    host_user: str
    has_password: bool
    use_tls: bool
    use_ssl: bool
    timeout: Union[None, int]
    default_from_email: str
    default_reply_to_email: str
    subject_prefix: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend = self.backend

        host = self.host

        port: Union[None, int]
        port = self.port

        host_user = self.host_user

        has_password = self.has_password

        use_tls = self.use_tls

        use_ssl = self.use_ssl

        timeout: Union[None, int]
        timeout = self.timeout

        default_from_email = self.default_from_email

        default_reply_to_email = self.default_reply_to_email

        subject_prefix = self.subject_prefix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend": backend,
                "host": host,
                "port": port,
                "host_user": host_user,
                "has_password": has_password,
                "use_tls": use_tls,
                "use_ssl": use_ssl,
                "timeout": timeout,
                "default_from_email": default_from_email,
                "default_reply_to_email": default_reply_to_email,
                "subject_prefix": subject_prefix,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend = d.pop("backend")

        host = d.pop("host")

        def _parse_port(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        port = _parse_port(d.pop("port"))

        host_user = d.pop("host_user")

        has_password = d.pop("has_password")

        use_tls = d.pop("use_tls")

        use_ssl = d.pop("use_ssl")

        def _parse_timeout(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        timeout = _parse_timeout(d.pop("timeout"))

        default_from_email = d.pop("default_from_email")

        default_reply_to_email = d.pop("default_reply_to_email")

        subject_prefix = d.pop("subject_prefix")

        email_config = cls(
            backend=backend,
            host=host,
            port=port,
            host_user=host_user,
            has_password=has_password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            timeout=timeout,
            default_from_email=default_from_email,
            default_reply_to_email=default_reply_to_email,
            subject_prefix=subject_prefix,
        )

        email_config.additional_properties = d
        return email_config

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
