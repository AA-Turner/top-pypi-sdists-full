from pydantic import BaseModel
from typing import Optional


class StructuralGeneratorConfig(BaseModel):
    data_path: str
    data_file_name: Optional[str] = None
    output_path: str

    @staticmethod
    def generate_example_config() -> dict:
        """Generates an example configuration dictionary."""
        return {
            "data_folder_path": "/path/to/your/data_folder",
            "data_file_name": "your_data_file.json",
            "output_path": "/path/to/output_folder",
        }
