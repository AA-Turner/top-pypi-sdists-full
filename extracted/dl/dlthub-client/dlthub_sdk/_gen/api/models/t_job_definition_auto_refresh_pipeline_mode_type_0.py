from enum import Enum


class TJobDefinitionAutoRefreshPipelineModeType0(str, Enum):
    DROP_DATA = "drop_data"
    DROP_RESOURCES = "drop_resources"
    DROP_SOURCES = "drop_sources"

    def __str__(self) -> str:
        return str(self.value)
