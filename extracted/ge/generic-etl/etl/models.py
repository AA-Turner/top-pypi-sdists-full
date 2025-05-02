from dataclasses import dataclass, fields
from typing import Dict, List, Optional


@dataclass
class Pipeline:
    out_type: Optional[str] = None
    steps: Dict[str, dict] = None

    @classmethod
    def from_dict(cls, data: dict):
        class_fields = {f.name for f in fields(cls)}
        # retain order pls
        ks = set(data.keys()) - class_fields
        steps_ = {k: [] for k in ks}
        for key in steps_:
            steps_[key] = data[key]
        data["steps"] = steps_
        return cls(**{k: v for k, v in data.items() if k in class_fields})


@dataclass
class ETL:
    cycle: str = "daily"
    order: List[str] = None
    pipeline: List[dict] = None
    secrets: Optional[dict] = None
    meta_output: Optional[str] = None

    def __post_init__(self):
        self.pipeline = Pipeline.from_dict(self.pipeline)

    @classmethod
    def from_dict(cls, data: dict):
        data.pop("parameters")
        [
            data.pop(key)
            for key in ["FIRST_DAY_MONTH", "LAST_DAY_MONTH", "YEAR", "MONTH", "DAY"]
        ]

        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in class_fields})
