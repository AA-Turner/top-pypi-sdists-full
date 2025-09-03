from __future__ import annotations

import dataclasses
import enum
import json
import os
from dataclasses import dataclass
from typing import List

import smart_open

from bigeye_sdk.log import get_logger

# create logger
log = get_logger(__name__)


# Right now only works with snowflake.
class FileType(str, enum.Enum):
    JSON = "file_format = (type = 'JSON', field_delimiter = '|')"
    PSV = "file_format = (type = 'CSV', field_delimiter = '|', SKIP_HEADER = 1)"

    def get_file_extension(self):
        return self.name.lower()


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def create_subdir_if_not_exists(path, includes_file: bool = False):
    """
    Create a subdirectory if it doesn't exist

    :param path: The path to create; with or without a file name.
    :param includes_file: Whether to include a file.
    """
    subdir = path if not includes_file else os.path.dirname(path)
    if not os.path.exists(subdir):
        log.info(f"Creating path: {subdir}")
        os.makedirs(subdir)


@dataclass
class WriteDataResult:
    fq_table: str
    url: str
    format: FileType


def write_to_file(url: str, serialized_data: List[str]) -> str:
    log.info(f"Persisting file: {url}")
    with smart_open.open(url, "wb") as fout:
        for s in serialized_data:
            fout.write(s.encode())

    return url


def serialize_dataclass_to_json_file(url: str, datum: dataclass) -> str:
    """
    Serialize a given dataclass to a JSON file.

    :param url: The path to write the file.
    :param datum: The dataclass to serialize.

    :returns: str
    """
    return write_to_file(url, [json.dumps(datum, cls=EnhancedJSONEncoder)])


def serialize_list_to_json_file(url: str, data: list) -> str:
    """
    Serialize a list of dataclasses to a JSON file.

    :param url: The path to write the file.
    :param data: The list of dataclasses to serialize.

    :returns: str
    """
    log.info(f"writing file: {url}")
    return write_to_file(
        url,
        [
            f"{json.dumps(datum, cls=EnhancedJSONEncoder, indent=True)}\n\n"
            for datum in data
        ],
    )


# TODO Replace with serialize_list_to_json_file
def serialize_listdict_to_json_file(url: str, data: List[dict]) -> str:
    string_list = [f"{json.dumps(datum, default=str)}\n" for datum in data]
    return write_to_file(url, string_list)


def read_json_file(file_path: str):
    log.info(f"Loading file at {file_path}...")
    try:
        with open(file=file_path, mode="r") as fin:
            return json.loads(fin.read())
    except Exception as e:
        log.error(f"Error loading file {file_path}")
        log.error(e)
        return dict()
