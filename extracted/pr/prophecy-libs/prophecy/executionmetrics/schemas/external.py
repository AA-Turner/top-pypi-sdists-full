from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import copy


@dataclass(frozen=True)
class InterimKey:
    """Key for interim storage."""

    subgraph: str
    component: str
    port: str
    runIdOpt: Optional[str] = None


@dataclass
class LInterimContent:
    """Interim content representation."""

    subgraph: str
    component: str
    port: str
    interimRows: List[Dict[str, Any]]
    schema: Optional[Any] = None
    runId: Optional[str] = None
    processId: Optional[str] = None
    numRecords: Optional[int] = None
    bytesProcessed: Optional[int] = None
    numPartitions: Optional[int] = None
    runConfig: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LInterimContent":
        return cls(
            subgraph=data["subgraph"],
            component=data["component"],
            port=data["port"],
            interimRows=data["data"],
            processId=data["processId"] if "processId" in data else None,
            numRecords=data["numRecords"] if "numRecords" in data else None,
            bytesProcessed=(
                data["bytesProcessed"] if "bytesProcessed" in data else None
            ),
            numPartitions=data["numPartitions"] if "numPartitions" in data else None,
        )

    def update(self, right: "LInterimContent") -> "LInterimContent":
        obj = copy.deepcopy(self)
        obj.numRecords = (obj.numRecords or 0) + (right.numRecords or 0)
        obj.bytesProcessed = (obj.bytesProcessed or 0) + (right.bytesProcessed or 0)
        obj.numPartitions = (obj.numPartitions or 0) + (right.numPartitions or 0)
        return obj


class LInterimContentOrdering:
    """Ordering for LInterimContent based on num_records."""

    @staticmethod
    def compare(x: LInterimContent, y: LInterimContent) -> int:
        """Compare two interim contents by number of records."""
        x_records = x.numRecords or 0
        y_records = y.numRecords or 0
        return x_records - y_records

    @classmethod
    def sort(cls, interims: List[LInterimContent]) -> List[LInterimContent]:
        """Sort interims by number of records."""
        return sorted(interims, key=lambda x: x.numRecords or 0)


@dataclass
class ComponentRunIdAndInterims:
    """Component run ID with associated interims."""

    uid: str
    run_id: Optional[str]
    interims: str


@dataclass
class MetricsTableNames:
    """Names for metrics tables."""

    pipeline_metrics: Optional[str] = None
    component_metrics: Optional[str] = None
    interims: Optional[str] = None

    def is_empty(self) -> bool:
        """Check if all table names are empty."""
        return not any([self.pipeline_metrics, self.component_metrics, self.interims])

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricsTableNames":
        return cls(
            pipeline_metrics=data.get("pipelineMetrics"),
            component_metrics=data.get("componentMetrics"),
            interims=data.get("interims"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipelineMetrics": self.pipeline_metrics,
            "componentMetrics": self.component_metrics,
            "interims": self.interims,
        }


@dataclass
class MetricsWriteDetails:
    """Names for metrics tables."""

    names: MetricsTableNames
    storage_format: Any
    is_partitioning_disabled: bool


class DatasetType:
    """Dataset type constants."""

    SOURCE = "Source"
    LOOKUP = "Lookup"
    TARGET = "Target"

    @classmethod
    def to_list_as_string(cls) -> str:
        """Get SQL-ready list of types."""
        return f"'{cls.SOURCE}', '{cls.LOOKUP}', '{cls.TARGET}'"
