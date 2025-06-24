import yaml
from pathlib import Path
from typing import Dict, Union

class YAMLLoader:
    @staticmethod
    def load_from_path(path: Union[Path, str]) -> Dict:
        file_path = Path(path)

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        with file_path.open("r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_from_string(string: str) -> Dict:
        return yaml.safe_load(string)