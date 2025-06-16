import os
from enum import Enum

from typing import Tuple

AIM_REPO_NAME = '__AIM_REPO_NAME__'
AIM_RUN_INDEXING_TIMEOUT = '__AIM_RUN_INDEXING_TIMEOUT_SECONDS__'
AIM_LOG_LEVEL_KEY = '__AIM_LOG_LEVEL__'
AIM_ENV_MODE_KEY = '__AIM_ENV_MODE__'


def get_aim_repo_name() -> str:
    return os.environ.get(AIM_REPO_NAME) or '.aim'


def get_data_version() -> Tuple[int, int]:
    return 2, 0


class KeyNames:
    INFO_PREFIX = 'info_'
    INDEX_PREFIX = 'index_'

    CONTAINER_TYPE = 'cont_type'
    SEQUENCE_TYPE = 'seq_type'
    VALUE_TYPE = 'val_type'
    OBJECT_CATEGORY = 'object_category'

    SEQUENCES = 'sequences'
    CONTEXTS = 'contexts'
    CONTAINERS = 'containers'

    ALLOWED_VALUE_TYPES = 'allowed_val_types'
    CONTAINER_TYPES_MAP = 'cont_types_map'
    SEQUENCE_TYPES_MAP = 'seq_types_map'
    SEQUENCE_TYPES = 'seq_types'
    VALUE_TYPES = 'val_types'


class ContainerOpenMode(Enum):
    READONLY = 1
    WRITE = 2
    FORCEWRITE = 3
    EDIT = 4
