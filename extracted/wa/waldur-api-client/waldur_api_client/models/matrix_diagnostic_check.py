from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.matrix_diagnostic_check_metrics import MatrixDiagnosticCheckMetrics


T = TypeVar("T", bound="MatrixDiagnosticCheck")


@_attrs_define
class MatrixDiagnosticCheck:
    """
    Attributes:
        name (str):
        label (str):
        ok (bool):
        detail (str):
        metrics (Union[Unset, MatrixDiagnosticCheckMetrics]): The check's numbers, for monitoring: {"round_trip_ms": 12}
            for appservice_ping, {"failed": 2} for history_exports and {"4xx": 3, "5xx": 0} for webhook_errors. Absent on
            other checks, and on appservice_ping when the ping failed.
    """

    name: str
    label: str
    ok: bool
    detail: str
    metrics: Union[Unset, "MatrixDiagnosticCheckMetrics"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        ok = self.ok

        detail = self.detail

        metrics: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "label": label,
                "ok": ok,
                "detail": detail,
            }
        )
        if metrics is not UNSET:
            field_dict["metrics"] = metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.matrix_diagnostic_check_metrics import MatrixDiagnosticCheckMetrics

        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        ok = d.pop("ok")

        detail = d.pop("detail")

        _metrics = d.pop("metrics", UNSET)
        metrics: Union[Unset, MatrixDiagnosticCheckMetrics]
        if isinstance(_metrics, Unset):
            metrics = UNSET
        else:
            metrics = MatrixDiagnosticCheckMetrics.from_dict(_metrics)

        matrix_diagnostic_check = cls(
            name=name,
            label=label,
            ok=ok,
            detail=detail,
            metrics=metrics,
        )

        matrix_diagnostic_check.additional_properties = d
        return matrix_diagnostic_check

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
