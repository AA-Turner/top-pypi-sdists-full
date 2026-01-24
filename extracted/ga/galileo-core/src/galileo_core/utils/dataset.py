import json
from collections import ChainMap
from csv import DictReader
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, Tuple, Union
from warnings import warn

from galileo_core.constants.dataset_format import DatasetFormat

JSONValue = Union[str, int, float, bool, None, Dict[str, "JSONValue"], List["JSONValue"]]

DatasetType = Union[Path, str, Dict[str, List[Any]], List[Dict[str, Any]]]


def process_dataset_value(value: Any) -> JSONValue:
    """Convert Python objects to values that can be serialized to JSON."""

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    if isinstance(value, (dict, list)):
        return json.dumps(value, default=str)

    return str(value)


def parse_dataset_dict(dataset: Dict[str, List[Any]]) -> List[Dict[str, JSONValue]]:
    key_rows = [[{key: process_dataset_value(value)} for value in values] for key, values in dataset.items()]
    return [dict(ChainMap(*key_row)) for key_row in zip(*key_rows)]


def parse_dataset_list(dataset: List[Dict[str, Any]]) -> List[Dict[str, JSONValue]]:
    return [dict((k, process_dataset_value(v)) for k, v in row.items()) for row in dataset]


def parse_dataset(dataset: DatasetType) -> Tuple[Path, DatasetFormat]:
    """
    Set the dataset path and format.

    If the dataset is a dictionary or list, it will be stored as a temporary file and
    the path to the temporary file will be returned. If the dataset is a path or string,
    the path will be returned. If the dataset is not a dictionary, list, path, or
    string, a ValueError will be raised.

    If the dataset is a dictionary or list then it will be stored as a JSONL file.

    Parameters
    ----------
    dataset : DatasetType
        Dataset as provided by the user.

    Returns
    -------
    Tuple[Path, DatasetFormat]
        Path to the dataset file and the dataset format.

    Raises
    ------
    ValueError
        If the dataset is not a dictionary, list, path, or string.
    ValueError
        If the dataset file is not a CSV or Feather file.
    FileNotFoundError
        If the dataset file does not exist.
    """
    # Set the dataset path.
    if isinstance(dataset, (dict, list)):
        dataset_rows = parse_dataset_dict(dataset) if isinstance(dataset, dict) else parse_dataset_list(dataset)
        with NamedTemporaryFile(mode="wt", suffix=f".{DatasetFormat.jsonl}", delete=False) as dataset_file:
            for row in dataset_rows:
                dataset_file.write(json.dumps(row, default=str) + "\n")
            dataset_path = Path(dataset_file.name)
    elif isinstance(dataset, Path):
        dataset_path = dataset
    elif isinstance(dataset, str):
        dataset_path = Path(dataset)
    else:
        raise ValueError(f"Invalid dataset type: '{type(dataset)}'.")
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file '{dataset_path}' does not exist.")

    # Set the dataset format.
    if dataset_path.suffix.endswith(DatasetFormat.csv):
        dataset_format = DatasetFormat.csv
        # Check if we have embedding columns.
        reader = DictReader(dataset_path.open("rt", errors="ignore"))
        for column in reader.fieldnames or []:
            if column.endswith("_embedding"):
                warn(
                    f"Column '{column}' appears to be an embedding column, please use "
                    "a feather file as dataset format instead."
                )
    elif dataset_path.suffix.endswith(DatasetFormat.jsonl):
        dataset_format = DatasetFormat.jsonl
    elif dataset_path.suffix.endswith(DatasetFormat.feather):
        dataset_format = DatasetFormat.feather
    else:
        raise ValueError(
            f"Invalid dataset file: '{dataset_path}'. Supported file types are '.csv', '.feather', and '.jsonl'."
        )
    return dataset_path, dataset_format
