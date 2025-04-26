from dataclasses import dataclass


@dataclass
class DataExport:
    name: str
    title: str
    description: str


DATA_EXPORT_CATALOG = [
    DataExport(
        name="MONITORS",
        title="Monitors",
        description="All monitors with aggregated properties, excluding deleted monitors.",
    ),
    DataExport(
        name="ASSETS",
        title="Assets",
        description="All assets with aggregated properties, excluding deleted assets.",
    ),
    DataExport(
        name="ALERTS",
        title="Alerts",
        description="All alerts in the last 90 days with aggregated properties.",
    ),
    DataExport(
        name="EVENTS",
        title="Events",
        description="All events in the last 90 days with aggregated properties.",
    ),
]
