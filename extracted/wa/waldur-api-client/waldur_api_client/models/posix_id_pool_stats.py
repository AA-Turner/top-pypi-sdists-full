from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.posix_id_pool_namespace_stats import PosixIdPoolNamespaceStats


T = TypeVar("T", bound="PosixIdPoolStats")


@_attrs_define
class PosixIdPoolStats:
    """
    Attributes:
        uid (Union['PosixIdPoolNamespaceStats', None]):
        gid (Union['PosixIdPoolNamespaceStats', None]):
        utilization_threshold (int):
    """

    uid: Union["PosixIdPoolNamespaceStats", None]
    gid: Union["PosixIdPoolNamespaceStats", None]
    utilization_threshold: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.posix_id_pool_namespace_stats import PosixIdPoolNamespaceStats

        uid: Union[None, dict[str, Any]]
        if isinstance(self.uid, PosixIdPoolNamespaceStats):
            uid = self.uid.to_dict()
        else:
            uid = self.uid

        gid: Union[None, dict[str, Any]]
        if isinstance(self.gid, PosixIdPoolNamespaceStats):
            gid = self.gid.to_dict()
        else:
            gid = self.gid

        utilization_threshold = self.utilization_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "gid": gid,
                "utilization_threshold": utilization_threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.posix_id_pool_namespace_stats import PosixIdPoolNamespaceStats

        d = dict(src_dict)

        def _parse_uid(data: object) -> Union["PosixIdPoolNamespaceStats", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                uid_type_1 = PosixIdPoolNamespaceStats.from_dict(data)

                return uid_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PosixIdPoolNamespaceStats", None], data)

        uid = _parse_uid(d.pop("uid"))

        def _parse_gid(data: object) -> Union["PosixIdPoolNamespaceStats", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gid_type_1 = PosixIdPoolNamespaceStats.from_dict(data)

                return gid_type_1
            except:  # noqa: E722
                pass
            return cast(Union["PosixIdPoolNamespaceStats", None], data)

        gid = _parse_gid(d.pop("gid"))

        utilization_threshold = d.pop("utilization_threshold")

        posix_id_pool_stats = cls(
            uid=uid,
            gid=gid,
            utilization_threshold=utilization_threshold,
        )

        posix_id_pool_stats.additional_properties = d
        return posix_id_pool_stats

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
