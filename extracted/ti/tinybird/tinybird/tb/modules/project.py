import glob
import re
from pathlib import Path
from typing import Dict, List, Optional

from tinybird.datafile.common import Datafile
from tinybird.datafile.parse_datasource import parse_datasource
from tinybird.datafile.parse_pipe import parse_pipe


class Project:
    extensions = ("datasource", "pipe", "connection")

    def __init__(self, folder: str, workspace_name: str, max_depth: int = 2):
        self.folder = folder
        self.workspace_name = workspace_name
        self.max_depth = max_depth

    @property
    def path(self) -> Path:
        return Path(self.folder)

    @property
    def vendor_path(self) -> str:
        return f"{self.path}/vendor"

    @property
    def tests_path(self) -> str:
        return f"{self.path}/tests"

    def get_files(self, extension: str) -> List[str]:
        project_files: List[str] = []
        for level in range(self.max_depth):
            project_files.extend(glob.glob(f"{self.path}{'/*' * level}/*.{extension}", recursive=True))
        return project_files

    def has_deeper_level(self) -> bool:
        """Check if there are folders with depth greater than max_depth in project path.

        Returns:
            bool: True if there are folders deeper than max_depth, False otherwise
        """
        for obj in glob.glob(f"{self.path}{'/*' * (self.max_depth - 1)}/*", recursive=False):
            if Path(obj).is_dir():
                return True
        return False

    def get_project_files(self) -> List[str]:
        project_files: List[str] = []
        for extension in self.extensions:
            for project_file in self.get_files(extension):
                if self.vendor_path in project_file:
                    continue
                project_files.append(project_file)
        return project_files

    def get_fixture_files(self) -> List[str]:
        fixture_files: List[str] = []
        for extension in [
            "csv",
            "csv.gz",
            "ndjson",
            "ndjson.gz",
            "jsonl",
            "jsonl.gz",
            "json",
            "json.gz",
            "parquet",
            "parquet.gz",
        ]:
            for fixture_file in self.get_files(extension):
                if self.vendor_path in fixture_file:
                    continue
                fixture_files.append(fixture_file)
        return fixture_files

    def get_test_files(self) -> List[str]:
        test_files: List[str] = []
        for test_file in self.get_files("yaml"):
            if self.vendor_path in test_file or self.tests_path not in test_file:
                continue
            test_files.append(test_file)
        return test_files

    def get_secrets(self) -> dict[str, str]:
        """Load secrets from .env.local file in the project folder."""
        secrets: dict[str, str] = {}
        env_file_path = Path(self.folder) / ".env.local"

        if not env_file_path.exists():
            return secrets

        try:
            content = env_file_path.read_text()
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    secrets[key.strip()] = value.strip()
        except Exception:
            # If there's any error reading the file, return empty dict
            pass

        return secrets

    def get_resource_path(self, resource_name: str, resource_type: str) -> str:
        full_path = next(
            (p for p in self.get_project_files() if p.endswith("/" + resource_name + f".{resource_type}")), ""
        )
        if not full_path:
            return ""
        return Path(full_path).relative_to(self.path).as_posix()

    @property
    def datasources(self) -> List[str]:
        return sorted([Path(f).stem for f in self.get_datasource_files()])

    @property
    def pipes(self) -> List[str]:
        return sorted([Path(f).stem for f in self.get_pipe_files()])

    @property
    def connections(self) -> List[str]:
        return sorted([Path(f).stem for f in self.get_connection_files()])

    def get_datasource_files(self) -> List[str]:
        return self.get_files("datasource")

    def get_pipe_files(self) -> List[str]:
        return self.get_files("pipe")

    def get_connection_files(self) -> List[str]:
        return self.get_files("connection")

    def get_kafka_connection_files(self) -> List[str]:
        return [f for f in self.get_connection_files() if self.is_kafka_connection(Path(f).read_text())]

    def get_s3_connection_files(self) -> List[str]:
        return [f for f in self.get_connection_files() if self.is_s3_connection(Path(f).read_text())]

    def get_gcs_connection_files(self) -> List[str]:
        return [f for f in self.get_connection_files() if self.is_gcs_connection(Path(f).read_text())]

    def get_pipe_datafile(self, filename: str) -> Optional[Datafile]:
        try:
            return parse_pipe(filename).datafile
        except Exception:
            return None

    def get_datasource_datafile(self, filename: str) -> Optional[Datafile]:
        try:
            return parse_datasource(filename).datafile
        except Exception:
            return None

    def get_datafile(self, filename: str) -> Optional[Datafile]:
        if filename.endswith(".pipe"):
            return self.get_pipe_datafile(filename)
        elif filename.endswith(".datasource"):
            return self.get_datasource_datafile(filename)
        return None

    def get_project_datafiles(self) -> Dict[str, Datafile]:
        project_filenames = self.get_project_files()
        datafiles: Dict[str, Datafile] = {}
        for filename in project_filenames:
            if datafile := self.get_datafile(filename):
                datafiles[filename] = datafile
        return datafiles

    @staticmethod
    def get_pipe_type(path: str) -> str:
        try:
            content = Path(path).read_text()
            if re.search(r"TYPE endpoint", content, re.IGNORECASE):
                return "endpoint"
            elif re.search(r"TYPE materialized", content, re.IGNORECASE):
                return "materialization"
            elif re.search(r"TYPE copy", content, re.IGNORECASE):
                return "copy"
            elif re.search(r"TYPE sink", content, re.IGNORECASE):
                return "sink"
            return "pipe"
        except Exception:
            return "pipe"

    @staticmethod
    def is_kafka_connection(content: str) -> bool:
        return re.search(r"TYPE kafka", content, re.IGNORECASE) is not None

    @staticmethod
    def is_s3_connection(content: str) -> bool:
        return re.search(r"TYPE s3", content, re.IGNORECASE) is not None

    @staticmethod
    def is_gcs_connection(content: str) -> bool:
        return re.search(r"TYPE gcs", content, re.IGNORECASE) is not None

    @staticmethod
    def is_kafka_datasource(content: str) -> bool:
        return re.search(r"KAFKA_CONNECTION_NAME", content, re.IGNORECASE) is not None

    @staticmethod
    def is_s3_datasource(content: str) -> bool:
        return re.search(r"IMPORT_CONNECTION_NAME", content, re.IGNORECASE) is not None

    @staticmethod
    def is_gcs_datasource(content: str) -> bool:
        return re.search(r"IMPORT_CONNECTION_NAME", content, re.IGNORECASE) is not None
