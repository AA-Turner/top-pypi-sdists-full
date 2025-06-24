import json
from typing import Dict, List, Union, Any
from pathlib import Path

class JSONLoader:
    @staticmethod
    def load_from_path(path: Union[Path, str]) -> Union[Dict[str, Any], List[Any]]:
        file_path = Path(path)

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def load_from_string(string: str) -> Dict:
        return json.loads(string)