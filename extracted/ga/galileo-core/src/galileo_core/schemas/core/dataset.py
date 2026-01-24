from datetime import datetime
from io import BufferedReader
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Field, model_validator

from galileo_core.constants.dataset_format import DatasetFormat
from galileo_core.utils.dataset import parse_dataset


class BaseDatasetRequest(BaseModel):
    format: DatasetFormat = DatasetFormat.csv
    file_path: Path = Field(exclude=True)

    @model_validator(mode="before")
    def dataset_to_path(cls, values: Dict) -> Dict:
        if "file_path" in values:
            values["file_path"], values["format"] = parse_dataset(values["file_path"])
        return values

    @property
    def files(self) -> Dict[str, BufferedReader]:
        return dict(file=self.file_path.open("rb"))


class UploadDatasetRequest(BaseDatasetRequest):
    file_path: Path = Field(exclude=True)

    @property
    def params(self) -> Dict[str, str]:
        return dict(
            format=self.format.value,
        )


class Dataset(BaseModel):
    id: UUID4
    name: str
    num_rows: Optional[int]
    column_names: Optional[List[str]]
    project_count: int
    created_at: datetime
    updated_at: datetime
