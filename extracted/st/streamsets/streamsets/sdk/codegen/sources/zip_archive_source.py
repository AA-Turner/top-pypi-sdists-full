#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import json
import zipfile
from pathlib import Path

from .source import PipelineDto, Source


class ZipArchiveSource(Source):
    def __init__(self, file_path: Path):
        self._file_path = file_path

    def load(self) -> PipelineDto:
        """Load pipeline data from a zip archive containing a single JSON file.

        Returns:
            PipelineDto: Pipeline data transfer object with config, rules, and library definitions.

        Raises:
            zipfile.BadZipFile: If the file is not a valid zip archive.
            ValueError: If the zip doesn't contain exactly one JSON file.
            KeyError: If the JSON is missing required fields.
            json.JSONDecodeError: If the JSON content is malformed.
        """
        with zipfile.ZipFile(self._file_path, 'r') as zip_file:
            file_list = zip_file.namelist()
            json_files = [f for f in file_list if f.endswith('.json')]

            if len(json_files) != 1:
                raise ValueError(f"Expected exactly 1 JSON file in zip archive, found {len(json_files)}")

            json_filename = json_files[0]
            with zip_file.open(json_filename) as json_file:
                pipeline_json = json.load(json_file)

            return PipelineDto(
                pipeline_config=pipeline_json["pipelineConfig"],
                pipeline_rules=pipeline_json["pipelineRules"],
                library_definitions=pipeline_json["libraryDefinitions"],
            )


# Made with Bob
