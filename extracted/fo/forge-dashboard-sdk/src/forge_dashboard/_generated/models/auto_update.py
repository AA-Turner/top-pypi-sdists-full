from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auto_update_source import AutoUpdateSource
from typing import cast

if TYPE_CHECKING:
  from ..models.auto_update_unavailable import AutoUpdateUnavailable





T = TypeVar("T", bound="AutoUpdate")



@_attrs_define
class AutoUpdate:
    """ Whether the dashboard brings this pull request's branch up to date by
    itself: the pull request's own choice when it has one
    (`POST /api/v1/pull-requests/auto-update`), else its repo's
    auto-update setting. Always present.

        Attributes:
            enabled (bool): What the background pass does with this pull request. Always
                false when `unavailable` is set.
            source (AutoUpdateSource): `repo` when the pull request follows its repo's setting,
                `pullRequest` when the user chose for this one.
            unavailable (AutoUpdateUnavailable | None): Set when the pass skips this pull request however it is switched,
                so a client shows the reason instead of a switch that does
                nothing. Null otherwise.
     """

    enabled: bool
    source: AutoUpdateSource
    unavailable: AutoUpdateUnavailable | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_update_unavailable import AutoUpdateUnavailable # noqa: PLC0415
        enabled = self.enabled

        source = self.source.value

        unavailable: dict[str, Any] | None
        if isinstance(self.unavailable, AutoUpdateUnavailable):
            unavailable = self.unavailable.to_dict()
        else:
            unavailable = self.unavailable


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "enabled": enabled,
            "source": source,
            "unavailable": unavailable,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auto_update_unavailable import AutoUpdateUnavailable # noqa: PLC0415
        d = dict(src_dict)
        enabled = d.pop("enabled")

        source = AutoUpdateSource(d.pop("source"))




        def _parse_unavailable(data: object) -> AutoUpdateUnavailable | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                unavailable_type_1 = AutoUpdateUnavailable.from_dict(data)



                return unavailable_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AutoUpdateUnavailable | None, data)

        unavailable = _parse_unavailable(d.pop("unavailable"))


        auto_update = cls(
            enabled=enabled,
            source=source,
            unavailable=unavailable,
        )


        auto_update.additional_properties = d
        return auto_update

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
