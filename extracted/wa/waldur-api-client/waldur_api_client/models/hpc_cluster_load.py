from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chart_spec import ChartSpec
    from ..models.hpc_maintenance_announcement import HpcMaintenanceAnnouncement
    from ..models.hpc_node import HpcNode
    from ..models.hpc_partition_load import HpcPartitionLoad
    from ..models.hpc_reservation import HpcReservation


T = TypeVar("T", bound="HpcClusterLoad")


@_attrs_define
class HpcClusterLoad:
    """
    Attributes:
        announcements (list['HpcMaintenanceAnnouncement']):
        nodes (list['HpcNode']):
        partitions (list['HpcPartitionLoad']):
        reservations (list['HpcReservation']):
        charts (list['ChartSpec']):
    """

    announcements: list["HpcMaintenanceAnnouncement"]
    nodes: list["HpcNode"]
    partitions: list["HpcPartitionLoad"]
    reservations: list["HpcReservation"]
    charts: list["ChartSpec"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        announcements = []
        for announcements_item_data in self.announcements:
            announcements_item = announcements_item_data.to_dict()
            announcements.append(announcements_item)

        nodes = []
        for nodes_item_data in self.nodes:
            nodes_item = nodes_item_data.to_dict()
            nodes.append(nodes_item)

        partitions = []
        for partitions_item_data in self.partitions:
            partitions_item = partitions_item_data.to_dict()
            partitions.append(partitions_item)

        reservations = []
        for reservations_item_data in self.reservations:
            reservations_item = reservations_item_data.to_dict()
            reservations.append(reservations_item)

        charts = []
        for charts_item_data in self.charts:
            charts_item = charts_item_data.to_dict()
            charts.append(charts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "announcements": announcements,
                "nodes": nodes,
                "partitions": partitions,
                "reservations": reservations,
                "charts": charts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_spec import ChartSpec
        from ..models.hpc_maintenance_announcement import HpcMaintenanceAnnouncement
        from ..models.hpc_node import HpcNode
        from ..models.hpc_partition_load import HpcPartitionLoad
        from ..models.hpc_reservation import HpcReservation

        d = dict(src_dict)
        announcements = []
        _announcements = d.pop("announcements")
        for announcements_item_data in _announcements:
            announcements_item = HpcMaintenanceAnnouncement.from_dict(announcements_item_data)

            announcements.append(announcements_item)

        nodes = []
        _nodes = d.pop("nodes")
        for nodes_item_data in _nodes:
            nodes_item = HpcNode.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        partitions = []
        _partitions = d.pop("partitions")
        for partitions_item_data in _partitions:
            partitions_item = HpcPartitionLoad.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        reservations = []
        _reservations = d.pop("reservations")
        for reservations_item_data in _reservations:
            reservations_item = HpcReservation.from_dict(reservations_item_data)

            reservations.append(reservations_item)

        charts = []
        _charts = d.pop("charts")
        for charts_item_data in _charts:
            charts_item = ChartSpec.from_dict(charts_item_data)

            charts.append(charts_item)

        hpc_cluster_load = cls(
            announcements=announcements,
            nodes=nodes,
            partitions=partitions,
            reservations=reservations,
            charts=charts,
        )

        hpc_cluster_load.additional_properties = d
        return hpc_cluster_load

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
