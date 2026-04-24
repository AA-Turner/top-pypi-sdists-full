#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import json
from pathlib import Path

from .source import PipelineDto, Source


class JsonFileSource(Source):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    def load(self) -> PipelineDto:
        with open(self._file_path, "r") as f:
            pipeline_json = json.load(f)
            return PipelineDto(
                pipeline_config=pipeline_json["pipelineConfig"],
                pipeline_rules=pipeline_json["pipelineRules"],
                library_definitions=pipeline_json["libraryDefinitions"],
            )
