from enum import StrEnum

class RunConfigFileClashErrorDtoCode(StrEnum):
    RUN_CONFIG_FILE_CLASH = "run_config_file_clash"

    def __str__(self) -> str:
        return str(self.value)
