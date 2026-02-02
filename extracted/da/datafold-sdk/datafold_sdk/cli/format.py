from typing import List, Optional

import attrs

def jsonify_error(table1: List[str], table2: List[str], dbt_model: Optional[str], error: str) -> "FailedDiff":
    return attrs.asdict(
        FailedDiff(
            status="failed",
            model=dbt_model,
            dataset1=table1,
            dataset2=table2,
            error=error,
        )
    )


@attrs.define(frozen=True)
class FailedDiff:
    status: str  # Literal ["failed"]
    model: str
    dataset1: List[str]
    dataset2: List[str]
    error: str

    version: str = "1.0.0"
    def __init__(self, status, model, dataset1, dataset2, error):
        super().__init__()
        self.status = status
        self.model = model
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.error = error
