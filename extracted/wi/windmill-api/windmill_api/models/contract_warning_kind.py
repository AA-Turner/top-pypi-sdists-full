from enum import Enum


class ContractWarningKind(str, Enum):
    MISSING_COLUMN = "missing_column"
    MISSING_DIMENSION_COLUMN = "missing_dimension_column"
    MISSING_LINEAGE_SOURCE = "missing_lineage_source"
    MISSING_MEASURE_COLUMN = "missing_measure_column"
    MISSING_RELATIONSHIP_COLUMN = "missing_relationship_column"
    NON_AGGREGATE_MEASURE = "non_aggregate_measure"
    RELATIONSHIP_TYPE_MISMATCH = "relationship_type_mismatch"
    SUPPRESSED = "suppressed"

    def __str__(self) -> str:
        return str(self.value)
