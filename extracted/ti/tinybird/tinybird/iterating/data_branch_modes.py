from enum import Enum


class DataBranchMode(Enum):
    LAST_PARTITION = "last_partition"
    ALL_PARTITIONS = "all_partitions"


DATA_BRANCH_MODES = [a.value for a in DataBranchMode]
