import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.email_config import EmailConfig
    from ..models.email_finding import EmailFinding


T = TypeVar("T", bound="EmailDiagnostics")


@_attrs_define
class EmailDiagnostics:
    """
    Attributes:
        status (str): Worst finding level: OK, WARNING or ERROR
        config (EmailConfig):
        findings (list['EmailFinding']):
        enabled_notification_count (int):
        total_notification_count (int):
        emails_sent_last_week (int):
        last_email_sent_at (Union[None, datetime.datetime]):
    """

    status: str
    config: "EmailConfig"
    findings: list["EmailFinding"]
    enabled_notification_count: int
    total_notification_count: int
    emails_sent_last_week: int
    last_email_sent_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        config = self.config.to_dict()

        findings = []
        for findings_item_data in self.findings:
            findings_item = findings_item_data.to_dict()
            findings.append(findings_item)

        enabled_notification_count = self.enabled_notification_count

        total_notification_count = self.total_notification_count

        emails_sent_last_week = self.emails_sent_last_week

        last_email_sent_at: Union[None, str]
        if isinstance(self.last_email_sent_at, datetime.datetime):
            last_email_sent_at = self.last_email_sent_at.isoformat()
        else:
            last_email_sent_at = self.last_email_sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "config": config,
                "findings": findings,
                "enabled_notification_count": enabled_notification_count,
                "total_notification_count": total_notification_count,
                "emails_sent_last_week": emails_sent_last_week,
                "last_email_sent_at": last_email_sent_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.email_config import EmailConfig
        from ..models.email_finding import EmailFinding

        d = dict(src_dict)
        status = d.pop("status")

        config = EmailConfig.from_dict(d.pop("config"))

        findings = []
        _findings = d.pop("findings")
        for findings_item_data in _findings:
            findings_item = EmailFinding.from_dict(findings_item_data)

            findings.append(findings_item)

        enabled_notification_count = d.pop("enabled_notification_count")

        total_notification_count = d.pop("total_notification_count")

        emails_sent_last_week = d.pop("emails_sent_last_week")

        def _parse_last_email_sent_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_email_sent_at_type_0 = isoparse(data)

                return last_email_sent_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_email_sent_at = _parse_last_email_sent_at(d.pop("last_email_sent_at"))

        email_diagnostics = cls(
            status=status,
            config=config,
            findings=findings,
            enabled_notification_count=enabled_notification_count,
            total_notification_count=total_notification_count,
            emails_sent_last_week=emails_sent_last_week,
            last_email_sent_at=last_email_sent_at,
        )

        email_diagnostics.additional_properties = d
        return email_diagnostics

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
